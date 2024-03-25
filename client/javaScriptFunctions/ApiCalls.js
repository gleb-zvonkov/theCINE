//const domain = 'http://127.0.0.1';    //this is what needs to be changed when running locally vs on google engine machine
const domain = 'http://' + window.location.hostname;

//this function get movie name for the starting page using the python flask server
//GET requests are generally considered idempotent (repeating the same request multiple times has the same effect as making the request once)
//This is not true for our get request, maybe it should be a post request? 
export async function getStartPageMovies() {    //pass the it the array of liked movies and previously recommended movies
    const apiUrl = `${domain}:5001/start_page`;   //the URL of the local api
    try {
        const response = await fetch(apiUrl, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
        });
        const data = await response.json();
        return data;
    } catch (error) {
        return null;
    }
}


export async function getRecommendedMoviesViaMethod(timeSpentData, method, timeoutDuration = 30000) { 
    const apiUrl = `${domain}:5001/${method}`;   //method names
    const controller = new AbortController();
    const signal = controller.signal;
    const timeoutId = setTimeout(() => {  // Setup a timeout to abort the fetch request if it takes too long
        controller.abort();
    }, timeoutDuration);
    try {   
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            credentials: 'include',
            body: JSON.stringify({ timeSpentData }),
            signal: signal // Pass the signal to the fetch request
        });
        clearTimeout(timeoutId); // Clear the timeout since the request completed within the timeout duration
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error occurred:', error);
        return null;
    }
}


//This function sends a search query to a server
//The server responds with the an object that contains the youtube videos ID
export async function searchYouTube(serchQuery){  //search for the movie trailer and return the video id
    try {
        const response = await fetch(`${domain}:3000/searchYouTube?searchQuery=${encodeURIComponent(serchQuery)}`); //get it from the server
        const object  =  await response.json();  //make it a json
        return object.videoId; //return the videoId
     } catch (error) {
        return null;
    }
}


export function sendTimeSpentDataToServer(clickedButton, timeSpentData, screenClick, youtubeClick, googleClick, streamingClick) {
    const apiUrl = `${domain}:5001/time_data`; // the URL of the local API
    let data = new FormData();   //used to construct a set of key/value pairs
    let method = clickedButton ? clickedButton.id : "default";   //if button is not clicked make it default

    data.append('recommendationMethod', JSON.stringify(method));

    data.append('timeSpentData', JSON.stringify(timeSpentData));

    data.append('clickData', JSON.stringify({
        screenClick,
        youtubeClick,
        googleClick,
        streamingClick
    }));

    let beaconSent = navigator.sendBeacon(apiUrl, data);
    if (beaconSent) {
        timeSpentData = [];
    } 
}