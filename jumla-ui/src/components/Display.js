import React, { Component } from 'react';
import { Link } from 'react-router';
import Nav from './Nav';
import { isLoggedIn } from '../utils/AuthService';
import { CloudinaryContext, Transformation, Video } from 'cloudinary-react';
import axios from 'axios';
import SearchField from "react-search-field";
import YouTube from 'react-youtube';

class Display extends Component {

  constructor(props) {
    super(props);

    this.state = { 
        videos: [], 
        res:[] 
    };

    this.onChange = this.onChange.bind(this);
    this.getVideos = this.getVideos.bind(this);
    this.apiBaseUrl = "http://localhost:8000/jumla/";

  }

  getVideos() {
    axios.get('http://res.cloudinary.com/unicodeveloper/video/list/miniflix.json')
          .then(res => {
            console.log(res.data.resources);
            this.setState({res: res.data.resources});
            this.setState({ videos: res.data.resources.splice(0,12)});
    });

   axios.get('http://localhost:8000/jumla/get_content')
        .then(res => {
          console.log(res);
        })
  }

  componentDidMount() {
    this.getVideos();
  }


  onChange() {
    console.log(this);
    axios.get('http://res.cloudinary.com/unicodeveloper/video/list/miniflix.json')
    .then(res => {
      console.log(res.data.resources);
      this.setState({res: res.data.resources});
      this.setState({ videos: res.data.resources.splice(0,3)});
});
  }

  render() {

    const { videos }  = this.state;

    const self = this;

    const opts = {
      height: '390',
      width: '640',
      playerVars: { 
        autoplay: 1
      }
    };

    return (
      <div>
        <Nav />
        <h3 className="text-center"> Latest Videos on Jumla </h3>
          <SearchField
           placeholder="Search..."
           onChange={this.onChange}
           searchText=""
           classNames="test-class"
           fewer = {this.getfewerVideos}
          />
        <hr/>

        <YouTube
          videoId='2g811Eo7K8U'                 // defaults -> null
          opts={obj}                        // defaults -> {}
          onReady={func}                    // defaults -> noop
          onPlay={func}                     // defaults -> noop
          onPause={func}                    // defaults -> noop
          onEnd={func}                      // defaults -> noop
          onError={func}                    // defaults -> noop
          onStateChange={func}              // defaults -> noop
          onPlaybackRateChange={func}       // defaults -> noop
          onPlaybackQualityChange={func}    // defaults -> noop
        />
        <div className="col-sm-12">
          <CloudinaryContext cloudName="unicodeveloper">
            { videos.map((data, index) => (
                <div className="col-sm-4" key={index}>
                  <div className="embed-responsive embed-responsive-4by3">
                    <Video publicId={data.public_id} width="300" height="300" controls></Video>
                  </div>
                  <div> Movie : {data.public_id} </div>
                </div>
              ))
            }
          </CloudinaryContext>
        </div>
      </div>
    );
  }
}

export default Display;
