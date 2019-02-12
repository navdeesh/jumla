import React, { Component } from 'react';
import { Link } from 'react-router';
import { login, logout, isLoggedIn } from '../utils/AuthService';
import '../App.css';

class Nav extends Component {

  render() {
    return (
      <nav className="navbar navbar-default">
        <div className="navbar-header">
          <Link className="navbar-brand" to="/">Jumla</Link>
        </div>
        <ul className="nav navbar-nav">
          <li>
            <Link to="/">All Videos</Link>
          </li>
          <li>
            <Link to = "/"> Subscriptions </Link>
          </li>
        </ul>
      
      </nav>
    );
  }
}

export default Nav;
