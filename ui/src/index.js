import React from 'react';
import ReactDOM from 'react-dom';
import { applyMiddleware, compose, createStore } from 'redux';
import { Provider } from 'react-redux';
import createSagaMiddleware from 'redux-saga';
import sagas from './sagas';
import reducers from './redux';
import Navigation from './components/Navigation';
import registerServiceWorker from './registerServiceWorker';
import './index.css';

const sagaMiddleware = createSagaMiddleware();
const store = createStore(reducers, compose(applyMiddleware(sagaMiddleware)));
sagaMiddleware.run(sagas);

ReactDOM.render(
  <Provider store={store}><Navigation/></Provider>,
  document.getElementById('root')
);

registerServiceWorker();
