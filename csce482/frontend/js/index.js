// Framework stuff
import * as Sentry from '@sentry/browser';
import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter, Route, Switch, Redirect } from "react-router-dom";
import { routeCodes } from "./config/routes";
// Styles
import { createMuiTheme, ThemeProvider } from '@material-ui/core/styles';
import './bootstrap-includes';
import '../sass/style.scss';
import '../css/styles.css';
// Custom components/utils, etc.
import App from "./components/App";
import About from './components/about/About';

const theme = createMuiTheme({
  palette: {
    primary: {
      light: '#A00000',
      main: '#800000',
      dark: '#500000',
      contrastText: '#fff',
    },
    secondary: {
      light: '#A00000',
      main: '#800000',
      dark: '#500000',
      contrastText: '#fff',
    },
  },
});

Sentry.init({
    dsn: window.SENTRY_DSN,
    release: window.COMMIT_SHA,
});

ReactDOM.render(
  <ThemeProvider theme={theme}>
    <BrowserRouter>
      <Switch>
        <Route path={routeCodes.ABOUT} component={About} />
        <Route path={routeCodes.HOME} component={App} />
      </Switch>
    </BrowserRouter>
  </ThemeProvider>
  , document.getElementById('react-app')
);
