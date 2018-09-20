import React, { Component } from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom'
import ProtectedRoute from './ProtectedRoute'; 
import App from '../containers/app/App';
import Login from '../containers/login/Login';
import Home from '../containers/home/Home';

export default class Navigation extends Component {
  render() {
    return (
      <Router>
        <Switch>
          <ProtectedRoute exact path="/" component={App}/>
          <ProtectedRoute exact path="/home" component={Home}/>
          <Route exact path="/login" component={Login}/>
        </Switch>
      </Router>
    )
  }
}