//Import the functions for fetching tmdb information
import {fetchMovie,searchMovieByTitle, getMovieByTitle, fetchTrendingMovies,fetchTopRatedMovies,fetchTopRatedMoviesPage} from './tmdbFetchFunctions.js';

//This functions creates one movie item 
//The arguments are the movie data since it need the backdrop path
//Its also a divId, wich is the unique identifier for the video  
function createMovieDiv(movieData, divId){
        const resultGrid = document.getElementById('result-grid');  //get the grid
        let movieListItem = document.createElement('div'); //for each movie list create a div
        movieListItem.innerHTML =`
            <div class = "movie-item-container">
                <div class = "movie-item">
                     <img class= "backdrop_image" src = "https://image.tmdb.org/t/p/original/${movieData.backdrop_path}">   
                     <h1 class="title">${movieData.title} </h1>
                     <div class = "hover-video" id="player${divId}"></div>     
                </div>
            </div> `;
        resultGrid.appendChild(movieListItem); //add it to the grid
}

//This function sends a search query to a server
//The server responds with the an object that contains the youtube videos ID
async function searchYouTube(serchQuery){  //search for the movie trailer and return the video id
    try {
        const response = await fetch(`http://localhost:3000/searchYouTube?searchQuery=${encodeURIComponent(serchQuery)}`); //get it from the server
        const object  =  await response.json();  //make it a json
        return object.videoId; //return the videoId
     } catch (error) {
        return null;
    }
}

//This function create a yotube video players and returns it
//Its passed the divId wich corresponds to the identifier of the unique player div
//Its also passed the youtube id of the youtube video we are creating the palyer for
//When the player is loaded the function onPlayerReady is triggered 
async function createPlayer(divId ,youtubeId) {  
    return new YT.Player(`player${divId}`, {   //return a new player 
        videoId: youtubeId,
        playerVars: {
            'controls': 0, // Hide video controls
            'modestbranding': 1, // Use modest branding
            'showinfo': 0, // Hide video title and uploader info (deprecated, but still works in some cases)
            'rel': 0, // Disable related videos at the end
            'start': 10, // make it start 2 seconds in
            'mute': 1, // Mute the video
            'origin': 'http://localhost:5501',
        }, 
        events: {
            'onReady': onPlayerReady.bind(null, divId)   //when the video is ready 
        }
    });
}

//This function enables the autoplay when a cursor enters the youtube player
//It also adds to the list of watchedTrailers everytime cursor enters the youtube player
function onPlayerReady(divId, event) {   
    const player = event.target; //get the player itself 
    const playerDiv = document.getElementById(`player${divId}`); //get the player div 
    playerDiv.addEventListener('mouseenter', function () {  //when the mouse enters the div
      player.playVideo(); // Start playing the video
      /*************  here we assume that the divId is the tmdbId **************/
      if (!allLikedMovies.includes(divId)) {  //if not already in the watched trailer array
        allLikedMovies.push(divId);  // add it to the watched trailers
      }
    });
    playerDiv.addEventListener('mouseleave', function () {  // when the mouse exits the div 
        player.pauseVideo(); // Pause the video when the mouse exits
    });
}

//This function displays a single movie using its tmdbID
async function displayMovieUsingTmdbId(tmdbId){
    var movieData = await fetchMovie(tmdbId);   // get the movie data from tmdbId
    createMovieDiv(movieData,tmdbId); // create the div with the image
    var searchQuery = `${movieData.title} ${movieData.release_date.substring(0, 4)} trailer`; //make the search query the movie title followed by its release year
    var youtubeId = await searchYouTube(searchQuery); //get the youtube id of the trailer
    createPlayer(tmdbId, youtubeId) //create the youtube player
}

//This function displays a single movie using it movie data
async function displayMovieUsingMovieData(movieData){   
    createMovieDiv(movieData,movieData.id); // create the div with the image
    var searchQuery = `${movieData.title} ${movieData.release_date.substring(0, 4)} trailer`; //make the search query the movie title followed by its release year
    var youtubeId = await searchYouTube(searchQuery); //get the youtube id of the trailer
    createPlayer(movieData.id, youtubeId) //create the youtube player
}

// This function displays multiple movies using there tmdbIDs
async function displayMoviesUsingTmdbIds(ids){
    for (const id of ids) {   //for each id 
        await displayMovieUsingTmdbId(id); // display the movie usings its TmdbId
    } 
}

//this function get movie name for the starting page using the python flask server
//GET requests are generally considered idempotent (repeating the same request multiple times has the same effect as making the request once)
//This is not true for our get request, maybe it should be a post request? 
async function getStartPageMovies() {    //pass the it the array of liked movies and previously recommended movies
    const apiUrl = 'http://127.0.0.1:5000/start_page';   //the URL of the local api
    try {
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        });
        const data = await response.json();
        return data;
    } catch (error) {
        return null;
    }
}

//This function gets recommende movies using the python flask server
async function getRecommendedMovies(allLikedMovies, allRecommendedMovies) {    //pass the it the array of liked movies and previously recommended movies
    const apiUrl = 'http://127.0.0.1:5000/my_api';   //the URL of the local api
    try {   
        const requestData = {   //create the request data that contains the two arrays
            allLikedMovies: allLikedMovies,   
            allRecommendedMovies: allRecommendedMovies,
        };
        const response = await fetch(apiUrl, {   //use fetch API 
            method: 'POST',  //make a POST request
            headers: {
                'Content-Type': 'application/json',   //the type of content is json
            },
            body: JSON.stringify(requestData),  //make the request data a json
        });
        const data = await response.json(); // parse the json response, it is an array containing tmdb ids
        return data; // return the data
    } catch (error) {   //If an error occurs during the above process, return null
        return null;
    }
}



/*****************************************************************************/
/* Below are functions that dispaly the starting page and recommended movies */
/*****************************************************************************/


var allLikedMovies = [];  //array that contains the tmdb id of the movies for witch the trailer was watched
var allRecommendedMovies = [];  //array the contains all the recommende movies

async function displayMoviesRecommended(){

     let moviesRecommended = await getRecommendedMovies(allLikedMovies, allRecommendedMovies);  // get reccommended movies using the flask server
      
      console.log("The movie recommended functions was called");
      console.log("The liked movies are: ");
      console.log(allLikedMovies);
      console.log("the previosuly recommende movies are: ");
      console.log(allRecommendedMovies);
      console.log("the newly recommended movies are: ")
      console.log(moviesRecommended);

     allRecommendedMovies = allRecommendedMovies.concat(moviesRecommended);  // push movies recommended to the list of all movies so we dont recommend them again
     await displayMoviesUsingTmdbIds(moviesRecommended); //display the recommended movies
   
}


async function main(){
    let starPageMovies = await getStartPageMovies();
    console.log(starPageMovies)

    try {
        const parsedObject = JSON.parse(starPageMovies);
        if (parsedObject && typeof parsedObject === 'object') {
            console.log("starPageMovies is a JSON-like object:", parsedObject);
        } else {
            console.error("starPageMovies is not a JSON-like object");
        }
    } catch (error) {
        console.error("starPageMovies is not a valid JSON string");
    }

    try {
        const parsedObject = JSON.parse(starPageMovies);
    
        if (Array.isArray(parsedObject) && parsedObject.length > 0) {
            const firstObject = parsedObject[0];
            console.log("The first object in starPageMovies:", firstObject);
        } else {
            console.error("parsedObject is either not an array or is an empty array:", parsedObject);
        }
    } catch (error) {
        console.error("Error parsing starPageMovies as JSON:", error);
    }

    const parsedObject = JSON.parse(starPageMovies);
    console.log("got here")

    for (let i = 0; i < parsedObject.length; i++) {
        let data = parsedObject[i];
        console.log("--------")
         console.log(parsedObject[i])
        console.log("--------")
        //allRecommendedMovies.push(data.id);
       displayMovieUsingMovieData(data);
    }
}

let hasMainExecuted = false;

if (!hasMainExecuted) {
    main();
    hasMainExecuted = true;
}


var throttleTimer; //Keep track of the throttle timer
const throttle = (callback, time) => {  //limits how often a callback can be called
  if (throttleTimer) return; //If throttle timer is already set, retun immediately
  throttleTimer = true; //otherwise set it to to true
  setTimeout(() => { // afte the specified time 
    callback();  //call the call back function
    throttleTimer = false;  //reset the throttletimer to false to allow callback
  }, time);
};


const handleInfiniteScroll = () => { //function to handle infinite scrolling
    throttle(() => {  //use throttle function to limit frequency of call back execution
        const endOfPage = window.innerHeight + window.pageYOffset >= document.body.offsetHeight - 500;  //calculate if its the end of the page
        //window.innerHeight represents the visible part of of the webpage
        //window.pageYOffset represents the number of pixels that the document is currently scrolled
        //document.body.offsetHeight represents the total height of the entire document 
        if (endOfPage) {  // if end of page
          displayMoviesRecommended(); //display the movies recommended
        }
      }, 5000); //Set a 5000ms throttle time
  };


window.addEventListener("scroll", handleInfiniteScroll); //sroll event to handle infinite scroll function







