const domain = 'http://127.0.0.1';    //this is what needs to be changed when running locally vs on google engine machine

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

//This function gets recommende movies using the python flask server
export async function getRecommendedMovies(allLikedMovies) {    //pass the it the array of liked movies and previously recommended movies
    const apiUrl = `${domain}:5001/recommendations`;   //the URL of the local api
    try {   
        const requestData = {   //create the request data that contains the two arrays
            allLikedMovies: allLikedMovies
        };
        const response = await fetch(apiUrl, {   //use fetch API 
            method: 'POST',  //make a POST request
            headers: {
                'Content-Type': 'application/json',   //the type of content is json
            },
            credentials: 'include',
            body: JSON.stringify(requestData),  //make the request data a json
        });
        const data = await response.json(); // parse the json response, it is an array containing tmdb ids
        return data; // return the data
    } catch (error) {   //If an error occurs during the above process, return null
        return null;
    }
}

export async function getCollaborativeRecommendedMovies(timeSpentData) {    //pass the it the array of liked movies and previously recommended movies
    const apiUrl = `${domain}:5001/collaborative_recommendations`;   //the URL of the local api
    try {   
        const response = await fetch(apiUrl, {   //use fetch API 
            method: 'POST',  //make a POST request
            headers: {
                'Content-Type': 'application/json',   //the type of content is json
            },
            credentials: 'include',
            body: JSON.stringify({timeSpentData}),  //make the request data a json
        });
        const data = await response.json(); // parse the json response, it is an array containing tmdb ids
        return data; // return the data
    } catch (error) {   //If an error occurs during the above process, return null
        return null;
    }
}

//This sends the time spent data to server
export async function sendTimeSpentDataToServer(timeSpentData) {    //pass the it the array of liked movies and previously recommended movies
    const apiUrl = `${domain}:5001/time_data`;   //the URL of the local api
    try {   
        return await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ timeSpentData }),
        });
        
    } catch (error) {   //If an error occurs during the above process, return null
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