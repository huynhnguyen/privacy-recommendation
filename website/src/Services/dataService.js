/* @flow */
import axios from 'axios'

const apiKey: string = '8d181bcb5e80a929053da01f6921e4a9'

export default {
  fetchMovies: ()=>{
    // const url = 'https://causality-recommending.herokuapp.com/movies';
    const url = "https://causality-recommending.herokuapp.com/movies";
    return axios.get(url).then(info => ({'ids': Object.keys(info.data), 'movies': Object.entries(info.data)}))
  },
  getRecommendMovie: (interacts, bestK=4)=>{
    const url = `https://causality-recommending.herokuapp.com/recommend?interacts=${JSON.stringify(interacts)}&bestk=${bestK}`;
    console.log({url});
    return axios.get(url).then(info => ({'movies': Object.entries(info.data.recommend)}))
  },
  getMovies: (category: string) => {
    const url = `https://api.themoviedb.org/3/movie/${category}?api_key=${apiKey}&language=en-US&page=1`
    return axios.get(url).then(info => info.data)
  },
  getSearch: (query: string) => {
    const url = `https://api.themoviedb.org/3/search/movie?query=${query}&api_key=${apiKey}`
    return axios.get(url).then(info => info.data)
  },
  getMovieById: (movieId: number) => {
    const url = `https://api.themoviedb.org/3/movie/${movieId}?api_key=${apiKey}&append_to_response=videos`
    return axios.get(url).then(info => info.data)
  },
  getMostVoted: () => {
    const url = `https://api.themoviedb.org/3/discover/movie?api_key=${apiKey}&language=en-US&sort_by=vote_average.asc&include_adult=true&include_video=false&page=1`
    return axios.get(url).then(info => info.data)
  }
}
