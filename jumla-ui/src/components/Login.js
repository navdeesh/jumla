import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';
import AppBar from 'material-ui/AppBar';
import RaisedButton from 'material-ui/RaisedButton';
import TextField from 'material-ui/TextField';
import React, { Component }  from 'react';
import axios from 'axios';
import { red100 } from 'material-ui/styles/colors';

class Login extends Component {
constructor(props){
  super(props);

  this.state={
  username:'',
  password:''
  }

  var login_this = this;

  this.routeChange = this.routeChange.bind(this);
 }

 routeChange() {
    let path = `/`;
    this.props.history.push(path);
}

 handleClick(event){

    var apiBaseUrl = "http://localhost:8000/jumla/";
    var self = this;

    var payload={
    "email":this.state.username,
    "password":this.state.password
    }

    axios.post(apiBaseUrl+'sign_in', payload)
    .then(function (response) {

    console.log(response);
    if(response.status == 200){
    console.log("reached here");
    console.log("Login successfull");
    console.log(self.props);
    self.props.history.push('/');
    }
   
    else if(response.data.code == 204){
    console.log("Username password do not match");
    alert("username password do not match")

    }
    else{
    console.log("Username does not exists");
    alert("Username does not exist");

    }
    })
    .catch(function (error) {
    console.log(error);
    });
    }

render() {
    return (
      <div class="center">
        <MuiThemeProvider>
          <div>
          <AppBar
             title="Jumla Login"
           />
           <TextField
             hintText="Enter your Username"
             floatingLabelText="Username"
             onChange = {(event,newValue) => this.setState({username:newValue})}
             />
           <br/>
             <TextField
               type="password"
               hintText="Enter your Password"
               floatingLabelText="Password"
               onChange = {(event,newValue) => this.setState({password:newValue})}
               />
             <br/>
             <RaisedButton label="Submit" primary={true} style={style} onClick={(event) => this.handleClick(event)}/>
         </div>
         </MuiThemeProvider>
      </div>
    );
  }
}

const style = {
 margin: 15,
};

export default Login;