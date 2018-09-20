import { createReducer, createActions } from 'reduxsauce';
import Immutable from 'seamless-immutable';

const { Types, Creators } = createActions({
  loginRequest: ['email', 'passsord'],
  loginSuccess: ['isAuthenticated']
});

export const AuthTypes = Types;
export default Creators;

export const INITIAL_STATE = Immutable({
  isAuthenticated: null,
  fetching: null,
  error: null,
  // ...
});

export const AuthSelectors = {
  isAuthenticated: (state) => {
    return state.auth.isAuthenticated;
  }
};

export const request = (state) => state.merge({ fetching: true });
export const success = (state) => state.merge({ fetching: false });

export const reducer = createReducer(INITIAL_STATE, {
  [Types.LOGIN_REQUEST]: request,
  [Types.LOGIN_SUCCESS]: success,
  // ...
})