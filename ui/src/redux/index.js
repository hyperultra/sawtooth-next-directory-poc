import { combineReducers } from 'redux';
import { reducer as AuthReducer } from './AuthRedux';

const reducers = combineReducers({
  auth: AuthReducer
});

export default reducers;