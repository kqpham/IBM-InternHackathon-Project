import React, { Component } from "react";
import logo from './logo.svg';
import SelectSearch from 'react-select-search';
import { Doughnut, Bar } from 'react-chartjs-2';
import './App.css';

class App extends Component {

  constructor ( props ) {
    super( props );

    this.change = this.change.bind( this );

    this.state = {
      apiData: {
        "transcript": [
          {
            "speaker": 0,
            "text": "this is highlight 1"
          },
          {
            "speaker": 1,
            "text": "this is another highlight"
          },
          {
            "speaker": 0,
            "text": "one last for good mesures"
          }
        ],
        "summary": [
          {
            "speaker": 0,
            "line": "this is highlight 1"
          },
          {
            "speaker": 1,
            "line": "this is another highlight"
          },
          {
            "speaker": 0,
            "line": "one last for good mesures"
          }
        ],
        "emotions": "[{\"speaker\": 0, \"sadness\": 0.09434833333333333, \"fear\": 0.053608666666666666, \"joy\": 0.367748, \"disgust\": 0.044539666666666665, \"anger\": 0.061689666666666663, \"lineCount\": 3}, {\"speaker\": 1, \"sadness\": 0.049097333333333326, \"fear\": 0.037758999999999994, \"joy\": 0.5206746666666667, \"disgust\": 0.020779666666666665, \"anger\": 0.06652566666666666, \"lineCount\": 3}]",
        "participation": {
          0: 0.5,
          1: 0.5
        }
      },
      files: {
        "files": [ "Sample Meeting", "Meeting with Watson AI Expert", "Test" ]
      },
      selected: false
    };
  };

  componentDidMount() {
    fetch( "http://9.24.158.86:5000/" )
      .then( res => res.json() )
      .then( filesList => this.setState( { files: { files: filesList } } ) );
  }

  getFiles() {
    var files = [];
    this.state.files.files.map( function ( file ) {
      file = file.substring( 8, file.length - 4 );
      files.push( { name: file, value: file } )
      return files;
    } );
    return files;
  }

  getPieData() {
    var speakers = [];
    var data = [];
    for( var i = 0; i < Object.keys( this.state.apiData.participation ).length; i++ ) {
      speakers.push( 'Speaker ' + i )
      data.push( this.state.apiData.participation[ i ] * 100 );
    }
    return (
      {
        labels: speakers,
        datasets: [ {
          label: '% Participation',
          data: data,
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)'
          ],
          borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)'
          ],
          borderWidth: 2
        } ]
      }
    );
  }

  getBarData() {
    var data = [ 0, 0, 0, 0, 0 ];
    var emotionList = [
      "sadness",
      "joy",
      "fear",
      "disgust",
      "anger"
    ];
    for( var i = 0; i < Object.keys( this.state.apiData.emotions ).length; i++ ) {
      for( var j = 1; j < 6; j++ ) {
        data[ j - 1 ] += this.state.apiData.emotions[ i ][ emotionList[ j ] ] * 100
      }
    }
    return (
      {
        labels: emotionList,
        datasets: [ {
          label: 'Overall Sentiment',
          data: data,
          backgroundColor: [
            'rgba(255, 99, 132, 0.2)',
            'rgba(54, 162, 235, 0.2)',
            'rgba(255, 206, 86, 0.2)',
            'rgba(75, 192, 192, 0.2)',
            'rgba(153, 102, 255, 0.2)'
          ],
          borderColor: [
            'rgba(255, 99, 132, 1)',
            'rgba(54, 162, 235, 1)',
            'rgba(255, 206, 86, 1)',
            'rgba(75, 192, 192, 1)',
            'rgba(153, 102, 255, 1)'
          ],
          borderWidth: 2
        } ]
      }
    );
  }


  change( event ) {
    const sendName = event.name + '.wav';
    fetch( "http://9.24.158.86:5000/results", {
      method: 'POST',
      body: JSON.stringify( { filename: sendName } ),
      headers: { 'Content-Type': 'application/json' },
    } )
      .then( res => res.json() )
      .then( data => {
        data.emotions = JSON.parse( data.emotions )
        this.setState( { selected: true, apiData: data } )
      } );
  }

  renderUserStats() {
    if( typeof ( this.state.apiData.emotions ) != 'object' ) {
      this.state.apiData.emotions = JSON.parse( this.state.apiData.emotions );
    }
    return ( this.state.apiData.emotions.map( speaker => (
      <div key={ speaker.speaker } className="perUserContainer">
        <h1>Speaker { speaker.speaker }</h1>
        <ul>
          <li>Spoke a total of { speaker.lineCount } times</li>
          <li>Sadness: { ( speaker.sadness * 100 ).toFixed( 1 ) }%</li>
          <li>Anger: { ( speaker.anger * 100 ).toFixed( 1 ) }%</li>
          <li>Joy: { ( speaker.joy * 100 ).toFixed( 1 ) }%</li>
          <li>Disgust: { ( speaker.disgust * 100 ).toFixed( 1 ) }%</li>
          <li>Fear: { ( speaker.fear * 100 ).toFixed( 1 ) }%</li>
        </ul>
      </div>
    ) ) );
  }

  render() {
    const searchOptions = this.getFiles();

    const pie_data = this.getPieData();

    const bar_data = this.getBarData();

    const renderUserStats = this.renderUserStats();

    const renderSummary = this.state.apiData.summary.map( sum => (
      <div key={ sum.line }>
        <div><b>Speaker { sum.speaker }:</b></div><br />
        { sum.line }
        <br />
        <br />
      </div>
    ) );

    const renderTranscript = this.state.apiData.transcript.map( line => (
      <div key={ line.text }>
        <div><b>Speaker { line.speaker }:</b></div><br />
        { line.text }
        <br />
        <br />
      </div>
    ) );

    if( !this.state.selected ) {
      return (
        <div className="App" >
          <div className="navbar">
            <div className="branding">
              <img src={ logo } className="logo" alt="logo" />
              <div className="app-name">MeetAI</div>
            </div>
            <SelectSearch options={ searchOptions } name="meeting" placeholder="Select your meeting" onChange={ this.change } />
            <button className="btn" type="button"><span>Add+</span></button>
          </div>
          <div className="footer">
            MeetAI was created for the IBM Intern Hackathon 2019. Made with ❤ in Ottawa. Created by David Voicu, Robin Luo, Kevin Pham, Walid Bounouar, and Kamil Sarbinowski.
      </div>
        </div >
      );
    }

    return (
      <div className="App" >
        <div className="navbar">
          <div className="branding">
            <img src={ logo } className="logo" alt="logo" />
            <div className="app-name">MeetAI</div>
          </div>
          <SelectSearch options={ searchOptions } name="meeting" placeholder="Select your meeting" onChange={ this.change } />
          <button className="btn" type="button"><span>Add+</span></button>
        </div>

        <div className="data-container">
          <div className="col-left">
            <div className="summaryContainer">
              <h1>Summary</h1>
              <div className="summary">
                { renderSummary }
              </div>
            </div>
            <div className="transcriptContainer">
              <h1>Transcript</h1>
              <div className="summary">{ renderTranscript }</div>
            </div>
          </div>
          <div className="col-mid">
            { renderUserStats }
          </div>
          <div className="col-right">
            <div className="graphsContainer">
              <h1>Participation</h1>
              <Doughnut data={ pie_data } />
            </div>
            <div className="graphsContainer">
              <h1>Emotions</h1>
              <Bar data={ bar_data } />
            </div>
          </div>
        </div>
        <div className="footer">
          MeetAI was created for the IBM Intern Hackathon 2019. Made with ❤ in Ottawa. Created by David Voicu, Robin Luo, Kevin Pham, Walid Bounouar, and Kamil Sarbinowski.
      </div>
      </div >
    );
  };
}

export default App;
