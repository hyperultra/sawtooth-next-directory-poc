import { all, takeLatest } from 'redux-saga/effects'
import { login } from './AuthSaga';
import { AuthTypes } from '../redux/AuthRedux';

export default function* root() {
  yield all([
    takeLatest(AuthTypes.LOGIN_REQUEST, login)
  ]);
}