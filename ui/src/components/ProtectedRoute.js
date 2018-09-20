import React from 'react';
import { Redirect, Route } from 'react-router-dom';
import { connect } from 'react-redux';
import { AuthSelectors } from '../redux/AuthRedux';

const ProtectedRoute = ({ isAllowed, ...props }) => 
  props.isAuthenticated 
  ? <Route {...props}/> 
  : <Redirect to="/login"/>;

const mapStateToProps = (state) => {
  return {
    isAuthenticated: AuthSelectors.isAuthenticated(state)
  }
}

export default connect(mapStateToProps)(ProtectedRoute);