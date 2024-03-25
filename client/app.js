//Import the functions for fetching tmdb information
import {fetchMovie, searchMovieByTitle, getMovieByTitle, fetchTrendingMovies, fetchTopRatedMovies,fetchTopRatedMoviesPage, getStreamingService} from './javaScriptFunctions/tmdbFetchFunctions.js';
import{getStartPageMovies, searchYouTube, getRecommendedMoviesViaMethod, sendTimeSpentDataToServer} from './javaScriptFunctions/ApiCalls.js';


/************************************************************************************/
//below is the function for keeping track of the mdoel selected

var clickedButton;
document.addEventListener('DOMContentLoaded', function() {
    var buttons = document.querySelectorAll('button');
    buttons.forEach(function(button) {
        button.addEventListener('click', function() {
            // Remove 'clicked' class from all buttons
            buttons.forEach(function(btn) {
                btn.classList.remove('clicked');
            });
            // Add 'clicked' class to the clicked button
            this.classList.add('clicked');

            clickedButton = this;
        });
    });
});

/************************************************************************************/



/************************************************************************************/
//below are function for creating the div with backdrop image, title, star rating 

//This functions creates one movie item 
//The arguments are the movie data since it need the backdrop path
//Its also a divId, wich is the unique identifier for the video  
async function createMovieDiv(movieData, divId){
        const resultGrid = document.getElementById('result-grid');  //get the grid
        let movieListItem = document.createElement('div'); //for each movie list create a div
        const providerData = await getStreamingServiceImage(movieData.id);

        movieListItem.innerHTML =`
            <div class = "movie-item-container">
                <div class = "movie-item">
                     
                    <img class="backdrop_image" src="${movieData.backdrop_path ? `https://image.tmdb.org/t/p/original/${movieData.backdrop_path}` : 'otherImages/default.jpg'}"> 
                     
                     <h1 class="title">${movieData.title} </h1>
                     <h2 class="stars">  </h2>


                     <div class = "links" id="link${divId}">
                        <a href="https://www.google.com/search?q=${movieData.title} ${movieData.release_date.substring(0, 4)}" target="_blank"> 
                            <img class="google-link" src="otherImages/google-white-logo.png" >
                        </a>
                        <a href="${providerData.websiteUrl}" target="_blank">
                            ${providerData.imageUrl ? `<img class="provider-image" src="${providerData.imageUrl}" >` : ''}  
                        </a>
                        <img class="youtube-link" src="otherImages/youtube.png" >
                     </div>

                     
                     <div class = "hover-video" id="player${divId}"></div>  
                    <div class ="mouse-move" id="mouse${divId}"> </div> 
                      
                </div>
            </div> `;
      
        addStarRating(movieData.vote_average, movieListItem.querySelector('.stars') );
        resultGrid.appendChild(movieListItem); //add it to the grid
}


async function getStreamingServiceImage(tmdbid) {
    const providerName = await getStreamingService(tmdbid);
    const providerImageMap = {
        'Netflix': {
            imageUrl: 'StreamingServiceLogos/netflix.png',
            websiteUrl: 'https://www.netflix.com/'
        },
        'Crave': {
            imageUrl: 'StreamingServiceLogos/crave.png',
            websiteUrl: 'https://www.crave.ca/'
        },
        'Amazon Prime Video': {
            imageUrl: 'StreamingServiceLogos/prime.png',
            websiteUrl: 'https://www.primevideo.com/'
        },
        'Disney Plus': {
            imageUrl: 'StreamingServiceLogos/disney.png',
            websiteUrl: 'https://www.disneyplus.com/'
        },
        'Criterion Channel': {
            imageUrl: 'StreamingServiceLogos/criterion.png',
            websiteUrl: 'https://www.criterionchannel.com/'
        },
        'Apple TV Plus': {
            imageUrl: 'StreamingServiceLogos/apple.png',
            websiteUrl: 'https://tv.apple.com/'
        },
        'Paramount Plus': {
            imageUrl: 'StreamingServiceLogos/paramount.png',
            websiteUrl: 'https://www.paramountplus.com/'
        }
    };
    const providerData = providerImageMap[providerName] || { imageUrl: '', websiteUrl: '' };
    return providerData;
}


//This function adds intakes a rating and a div
//From the rating it creates a number of star and places them on the div
function addStarRating(rating, starsDiv){
    const rawRating = (rating / 10) * 4;
    const roundedRating = Math.round(rawRating * 2) / 2;
    starsDiv.innerHTML = '';
    for (let i = 0; i < 4; i++) {
        if (i < Math.floor(roundedRating)) { // Full star
            starsDiv.innerHTML += '★';
        } else if (i === Math.floor(roundedRating) && roundedRating % 1 >= 0.5) { // Half star
            starsDiv.innerHTML += '☆'; // Half star 
        } 
    } 
}
/************************************************************************************/

 


/************************************************************************************/
//below are function for creating the youtube player 

//This function create a yotube video players and returns it
//Its passed the divId wich corresponds to the identifier of the unique player div
//Its also passed the youtube id of the youtube video we are creating the palyer for
//When the player is loaded the function onPlayerReady is triggered 
//This explained how YT.player works: https://developers.google.com/youtube/player_parameters 
async function createPlayer(divId ,youtubeId) {  
    return new YT.Player(`player${divId}`, {   //return a new player 
        videoId: youtubeId,
        playerVars: {
            'controls': 0, // Hide video controls
            'rel': 0, // Disable related videos at the end
            'start': 10, // make it start 2 seconds in
            'mute': 0, // Mute the video
            'origin': 'http://localhost:5501',
        }, 
        events: {
            'onReady': onPlayerReady.bind(null, divId)   //when the video is ready 
        }
    });
}

//This function enables the autoplay when a cursor enters the youtube player
//It also adds to the list of watchedTrailers everytime cursor enters the youtube player
//This function modifies the global allLikedMovies 
let screenClick = 0;
let youtubeClick =0;
let googleClick = 0;
let streamingClick = 0;
var allLikedMovies = [];  //array that contains the tmdb id of the movies for witch the trailer was watched
var timeSpentData = []; 
var firstClick = true;

function isDescendant(parent, child) {
    let node = child.parentNode;
    while (node != null) {
        if (node === parent) {
            return true;
        }
        node = node.parentNode;
    }
    return false;
}


const hideElement = (element) => {
    element.style.display = 'none';
};

const showElementWithDelay = (element, delay) => {
    element.style.display = 'block';
    clearTimeout(element.timeoutId);
    element.timeoutId = setTimeout(() => hideElement(element), delay);
};

function onPlayerReady(divId, event) {
    const delayTime = 3500;
    let timeoutId;
    let mouseEnterTime; // Variable to store the time when mouse enters the div
    const player = event.target; // Get the player itself
    const playerDiv = document.getElementById(`player${divId}`); // Get the player div
    const container = playerDiv.parentNode;  //The container of the iframe
    const videoOverlay= document.getElementById(`mouse${divId}`);
    const linksDiv = document.getElementById(`link${divId}`);
    const googleLink = linksDiv.querySelector('.google-link');
    const providerImage = linksDiv.querySelector('.provider-image');
    const youtubeLink = linksDiv.querySelector('.youtube-link');

    googleLink.addEventListener('click', () => { googleClick++; });
    providerImage?.addEventListener('click', () => streamingClick++);
    youtubeLink.addEventListener('click', () => {youtubeClick++;});

    videoOverlay.addEventListener('mouseenter', function () {
        showElementWithDelay(linksDiv, delayTime);
        mouseEnterTime = new Date().getTime(); // Record the time when the mouse enters the div
        player.playVideo(); // Start playing the video
        if (!allLikedMovies.includes(divId)) { // If not already in the watched trailer array
            allLikedMovies.push(divId); // Add it to the watched trailers
        }
    });

    container.addEventListener('mouseleave', function (event) {
        if (event.relatedTarget && !isDescendant(container, event.relatedTarget)) {  //only if its not in the container
        player.pauseVideo(); // Pause the video when the mouse exits   
        }
        if (mouseEnterTime) {   //check there is a valid time entered
            const mouseExitTime = new Date().getTime(); // Get the time when the mouse exits the div
            const timeSpentInDiv = mouseExitTime - mouseEnterTime; // Calculate the time spent in the div
            const existingDataIndex = timeSpentData.findIndex(data => data.divId === divId); // Check if the divId already exists in timeSpentData
            if (existingDataIndex !== -1) { // If divId already exists
                timeSpentData[existingDataIndex].timeSpent += timeSpentInDiv; //accumulate the time spent
            } else {  // If divId doesn't exist
                timeSpentData.push({  //Add new entry
                    divId: divId,
                    timeSpent: timeSpentInDiv
                });
            }
        } //end if
    });

    document.addEventListener("mouseleave", function() {  //if user leaves the tab, pause the video
        player.pauseVideo();
    });


    videoOverlay.addEventListener('click', function(event) { //when video is clicked we make it full screen
        if (firstClick) {    //if its the first time its clicked
            player.playVideo();  //play the video 
            firstClick = false; // Set firstClick to false after the first click
        } else{
            var requestFullScreen = playerDiv.requestFullScreen || playerDiv.mozRequestFullScreen || playerDiv.webkitRequestFullScreen; //get full screen 
            if (requestFullScreen) {  //if avaible 
                playerDiv.style.cssText = '';  //remove all the css 
                requestFullScreen.bind(playerDiv)(); //bind it 
            }
        }
        screenClick++; //increment the screen clock
    });

    container.addEventListener('mousemove', function (event) {  //when the mouse moves we show the link
        showElementWithDelay(linksDiv, delayTime);
    });

}
/************************************************************************************/




/************************************************************************************/
//Below are functions for creating multiple divs and youtube players 

//This function displays a single movie using its tmdbID
async function displayMovieUsingTmdbId(tmdbId){
    var movieData = await fetchMovie(tmdbId);   // get the movie data from tmdbId
    await createMovieDiv(movieData,tmdbId); // create the div with the image
    var searchQuery = `${movieData.title} ${movieData.release_date.substring(0, 4)} trailer`; //make the search query the movie title followed by its release year
    var youtubeId = await searchYouTube(searchQuery); //get the youtube id of the trailer
    createPlayer(tmdbId, youtubeId) //create the youtube player
    //Add streaming service info 
}

//This function displays a single movie using it movie data
async function displayMovieUsingMovieData(movieData){   
    await createMovieDiv(movieData,movieData.id); // create the div with the image
    var searchQuery = `${movieData.title} ${movieData.release_date.substring(0, 4)} trailer`; //make the search query the movie title followed by its release year
    var youtubeId = await searchYouTube(searchQuery); //get the youtube id of the trailer
    createPlayer(movieData.id, youtubeId) //create the youtube player
}

//This function displays multiple movies using there data
async function displayMoviesUsingMovieData(moviesData){
    const parsedObject = JSON.parse(moviesData);
    for (let i = 0; i < parsedObject.length; i++) {
        let data = parsedObject[i];
        displayMovieUsingMovieData(data);
    }
}

// This function displays multiple movies using there tmdbIDs
async function displayMoviesUsingTmdbIds(ids){
    for (const id of ids) {   //for each id 
        await displayMovieUsingTmdbId(id); // display the movie usings its TmdbId
    } 
}
/************************************************************************************/





/*****************************************************************************/
/* Below are functions that cause the starting page and recommended movies functions to be called  */

async function displayMoviesRecommended(){

    let method = "graphBased"; // Default method
    if (clickedButton && clickedButton.id !== undefined) {
        method = clickedButton.id;
    }

    let moviesRecommended = await getRecommendedMoviesViaMethod(timeSpentData, method);   
     await displayMoviesUsingTmdbIds(moviesRecommended); //display the recommended movies
}

async function main(){
    let starPageMovies = await getStartPageMovies();
    displayMoviesUsingMovieData(starPageMovies); 
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

/*****************************************************************************/




/*****************************************************************************/
/* Below are functions that cause the analytic data to be sent   */

//send time data when user leaves website 
// https://developer.mozilla.org/en-US/docs/Web/API/Navigator/sendBeacon
document.addEventListener('visibilitychange', function () {
    if (document.visibilityState === "hidden") {
        sendTimeSpentDataToServer(clickedButton, timeSpentData, screenClick, youtubeClick, googleClick, streamingClick)
    }
});

/*****************************************************************************/






