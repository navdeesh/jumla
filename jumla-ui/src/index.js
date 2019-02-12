import React from 'react';
import ReactDOM from 'react-dom';
import Display from './components/Display';
import Callback from './components/Callback';
import registerServiceWorker from './registerServiceWorker';
import { Router, Route, browserHistory } from 'react-router';
import { requireAuth } from './utils/AuthService';
import Login from './components/Login';

const Root = () => {
  return (
    <div className="container">
      <Router history={browserHistory}>
        <Route path="/" component={Display}/>
        <Route path="/Login" component={Login}/>
      </Router>
    </div>
  )
}

ReactDOM.render(<Root />, document.getElementById('root'));
registerServiceWorker();