//This functions gets movie data using its tmdbID
//https://developer.themoviedb.org/reference/movie-details  
export async function fetchMovie(tmdbId){
    const options = {     
        method: 'GET',
        headers: {
          accept: 'application/json',
          Authorization: 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZDIwYzY4ZDMxNmRkMjM0NGVkOWI5ZjRmNDNkMzIyYiIsInN1YiI6IjY1MDc1ODFhM2NkMTJjMDE0ZWJmN2U2YiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.URBinN5yI5YymjjRmdSmr4nEHXkQfsMFqToTyv9QTt0'
        }
      };
      const res = await fetch(`https://api.themoviedb.org/3/movie/${tmdbId}?language=en-US`, options);
      const data = await res.json();   // make it a json 
      return data
} 

//This functions search for a movie given its name, it returns a list of search results 
//https://developer.themoviedb.org/reference/search-movie 
export async function searchMovieByTitle(movieName){
    const options = {
      method: 'GET',
      headers: {
        accept: 'application/json',
        Authorization: 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZDIwYzY4ZDMxNmRkMjM0NGVkOWI5ZjRmNDNkMzIyYiIsInN1YiI6IjY1MDc1ODFhM2NkMTJjMDE0ZWJmN2U2YiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.URBinN5yI5YymjjRmdSmr4nEHXkQfsMFqToTyv9QTt0'
      }
    };
    const res = await fetch(`https://api.themoviedb.org/3/search/movie?query=${movieName}&include_adult=false&language=en-US&page=1`, options);
    const data = await res.json();   // make it a json 
    return data
}

//This functions search for a movie given its name, it returns only the first result
//https://developer.themoviedb.org/reference/search-movie 
export async function getMovieByTitle(movieName){
  const options = {
    method: 'GET',
    headers: {
      accept: 'application/json',
      Authorization: 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZDIwYzY4ZDMxNmRkMjM0NGVkOWI5ZjRmNDNkMzIyYiIsInN1YiI6IjY1MDc1ODFhM2NkMTJjMDE0ZWJmN2U2YiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.URBinN5yI5YymjjRmdSmr4nEHXkQfsMFqToTyv9QTt0'
    }
  };
  const res = await fetch(`https://api.themoviedb.org/3/search/movie?query=${movieName}&include_adult=false&language=en-US&page=1`, options);
  const data = await res.json();   // make it a json 
  return data.results[0] 
}


//This function get the top trending movies on tmdb
//https://developer.themoviedb.org/reference/trending-movies 
export async function fetchTrendingMovies(){
    const options = {     
        method: 'GET',
        headers: {
          accept: 'application/json',
          Authorization: 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZDIwYzY4ZDMxNmRkMjM0NGVkOWI5ZjRmNDNkMzIyYiIsInN1YiI6IjY1MDc1ODFhM2NkMTJjMDE0ZWJmN2U2YiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.URBinN5yI5YymjjRmdSmr4nEHXkQfsMFqToTyv9QTt0'
        }
      };
      const res = await fetch(`https://api.themoviedb.org/3/trending/movie/day?language=en-US`, options);
      const data = await res.json();   // make it a json 
      return data.results
}

//This function get the top rated movies on tmdb
//https://developer.themoviedb.org/reference/movie-top-rated-list 
export async function fetchTopRatedMovies(){
    const options = {     
        method: 'GET',
        headers: {
          accept: 'application/json',
          Authorization: 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZDIwYzY4ZDMxNmRkMjM0NGVkOWI5ZjRmNDNkMzIyYiIsInN1YiI6IjY1MDc1ODFhM2NkMTJjMDE0ZWJmN2U2YiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.URBinN5yI5YymjjRmdSmr4nEHXkQfsMFqToTyv9QTt0'
        }
      };
      const res = await fetch(`https://api.themoviedb.org/3/movie/top_rated?language=en-US&page=1`, options);
      const data = await res.json();   // make it a json 
      return data.results
}

//This function get a particular page of the top rated movies on tmdb 
//https://developer.themoviedb.org/reference/movie-top-rated-list 
export async function fetchTopRatedMoviesPage(page){
    const options = {     
        method: 'GET',
        headers: {
          accept: 'application/json',
          Authorization: 'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIzZDIwYzY4ZDMxNmRkMjM0NGVkOWI5ZjRmNDNkMzIyYiIsInN1YiI6IjY1MDc1ODFhM2NkMTJjMDE0ZWJmN2U2YiIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.URBinN5yI5YymjjRmdSmr4nEHXkQfsMFqToTyv9QTt0'
        }
      };
      const res = await fetch(`https://api.themoviedb.org/3/movie/top_rated?language=en-US&page=${page}`, options);
      const data = await res.json();   // make it a json 
      return data.results
}