import { put } from 'redux-saga/effects';
import AuthActions from '../redux/AuthRedux';

export function* login () {
  try {
    yield put(AuthActions.loginSuccess(true));
    console.log('success');
  } catch (err) {
    console.error(err);
  }
}