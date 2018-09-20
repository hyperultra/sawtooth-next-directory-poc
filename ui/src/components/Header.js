import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import logo from '../logo.svg';

export default class Header extends Component {
  render() {
    return (
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <h1 className="App-title">Welcome to React</h1>
        <Link to="/login">Login</Link>
      </header>
    )
  }
}