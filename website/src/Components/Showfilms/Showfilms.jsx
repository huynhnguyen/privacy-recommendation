import React, { Component } from 'react'
import CardTemplate from '../CardTemplate/CardTemplate'
import Api from '../../Services/dataService.js'
import { Row, Col, Button } from 'antd'
import uuidv4 from 'uuid/v4'
import './Showfilms.css'
import genRandomArray from './noiseGenerator';

export default class Showfilms extends Component {
  constructor (props) {
    super(props)
    this.state = {
      allMovies: [],
      privacyThreshold: 0.5,
      recommendedInteracts: [],
      recommendedNoiseInteracts: [],
      allIds: [],
      interacts: [],
      noiseInteracts: [],
    }
  }

  handleApiCall (props) {
    if (props.match.params.query) {
      
      Api.getSearch(props.match.params.query)
          .then(data => {
            this.setState({
              results: data.results
            })
          })
    } else {
      Api.fetchMovies().then(data=>{
        this.setState({allMovies: data.movies, allIds: data.ids})
      })
      // Api.getMovies(props.category)
      //     .then(data => {
      //       this.setState({
      //         results: data.results
      //       })
      //     })
    }
  }

  componentWillReceiveProps (nextProps) {
    this.handleApiCall(nextProps)
  }

  componentDidMount () {
    this.handleApiCall(this.props)
  }

  render () {
    return (
      <div>
        <Row>
          <Col span={12} offset={6}>
            <h1 className='title'>{ this.props.currentPage } </h1>
            For each interaction between users and contents, there is two records is generated: real interacts and generated interacts.
            As the time user hits recommendation button, both records will be send to server to get recommend content (movies).
            As client side, user know which records is correct and only show the recommendation on real reactions.
            As server side, since server has no knowledge about the records, both of them are stored on database and user for training recommendation.
            To understand how we do recommendation algorithm with noise data. Refer to our article: https://medium.com/@nguyenhuynh200188/we-know-what-you-need-but-we-do-not-see-your-data-6fd7674a1caf
          </Col>
        </Row>
        <Row>
          <Col span={12} offset={6}>
              <h1 className='title'> Recommend  </h1>
              <h2> Noise interacts: { JSON.stringify(this.state.interacts) } </h2>
              <h2> Real interacts: { JSON.stringify(this.state.noiseInteracts) } </h2>
          </Col>
        </Row>
        <Row>
          <button onClick={e=>{
                  let {interacts, noiseInteracts}=this.state;
                  Api.getRecommendMovie(interacts).then(data=>{
                    this.setState({'recommendedInteracts': data.movies});
                  })
                  Api.getRecommendMovie(noiseInteracts).then(data=>{
                    this.setState({'recommendedNoiseInteracts': data.movies});
                  })
              }}>recommend me the next movies</button>
        </Row>
        <Row gutter={24}>  
          <h2> recommendation based on real interacts </h2>
          {
            this.state.recommendedInteracts.map((film,idx) => {
              return (
                <Col className='gutter-row' span={5} offset={1} key={uuidv4()}>
                  <div className='film'>
                    {JSON.stringify(film[1])}
                  </div>
                </Col>
              )
            })
          }
        </Row>
        <Row gutter={24}>
          <h2> recommendation based on noise interacts </h2>
          {
            this.state.recommendedNoiseInteracts.map((film,idx) => {
              return (
                <Col className='gutter-row' span={5} offset={1} key={uuidv4()}>
                  <div className='film'>
                    movie: {JSON.stringify(film[1])}
                  </div>
                </Col>
              )
            })
          }
        </Row>
        
        <Row gutter={24}>
          <h1 className='title'>select movies</h1>
          {
            this.state.allMovies.map((film,idx) => {
              return (
                <Col className='gutter-row' span={5} offset={1} key={uuidv4()}>
                  <div className='film' onClick={(event)=>{
                    let realInteracts = [...this.state.interacts, parseInt(film[0])];
                    let noiseInteracts = [...this.state.noiseInteracts, parseInt(film[0])]
                    let max = this.state.allMovies.length
                    let genInteracts = genRandomArray(noiseInteracts, max, this.state.privacyThreshold);
                    console.log({realInteracts, genInteracts, max});
                    this.setState({'interacts': realInteracts, 'noiseInteracts': genInteracts });
                  }}>
                    <b>movie Id: {film[0]}</b>
                    <br/>
                    movie: {JSON.stringify(film[1])}
                  </div>
                  
                  {/* <CardTemplate
                    name={film.title}
                    date={film.release_date}
                    vote={film.vote_average}
                    image={film.poster_path}
                    id={film.id}
                  /> */}
                </Col>
              )
            })
          }
        </Row>
      </div>
    )
  }
}
