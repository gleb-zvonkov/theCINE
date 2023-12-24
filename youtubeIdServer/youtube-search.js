/*
This sets up a web server using the Express framework in Node.js
The server exposes a single endpoint /searchYoutube for handling GET Requests
Get request are intended to be made with a searchQuery parameter
The server performs a youtube search for videos using the searchQuery
It extracts the youtube video id from the top result
It send back that youtube video id

For example, a request and respone looks like: 
http://localhost:3000/searchYouTube?searchQuery=%22Thor%202011%22
{"videoId":"16xn0r7HM1U"} 
*/


const express = require('express'); // this is a web application framework for Node.js
const axios = require('axios'); // promise based HTTP client for makeing HTTP request
const cors = require("cors"); //Cross Origin Resource Sharing middleware for Express
const app = express(); //create an instance of express
const port = 3000;  //the port number for server

//Setup the middleware
app.use(express.json());  //parse incroming json request
app.use(
  cors({
    origin: "http://127.0.0.1:5501",   // allow requests from this origin 
  })
)

app.get('/searchYouTube', async (req, res) => {   // searchYoutube is endpoint of route for Get Request
  try {
    const searchQuery = req.query.searchQuery; //extract the movieName from the query string
    if (!searchQuery) { // if therese is no movie name 
      return res.status(400).json({ error: 'searchQuery parameter is required' }); // return an error message
    }

    const searchUrl = `https://www.youtube.com/results?search_query=${encodeURIComponent(searchQuery)}`;  // construct the Youtube search URL with encode movieName
    const response = await axios.get(searchUrl);  //make a get request to the url using axious
    const html = response.data; //get the html from the response

    // very hacky way of getting the youtube video id
    const matchIndex = html.indexOf('"videoRenderer"');   //find the index of video render this is close to the youtube video id
    const videoId = html.substring(matchIndex + 28, matchIndex + 39); //get the youtube video id

    res.json({ videoId }); //send the videoId as json response

  } catch (error) { // handle errors
    console.error('Error:', error);  //print error to the console
    res.status(500).json({ error: 'Internal server error' }); //send a 500 Interal error response
  }
});

app.listen(port, () => {   //start the server and listen on specified port
  console.log(`Server is running on port ${port}`); // print a message to signify that server is running
});
