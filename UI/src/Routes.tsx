import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import SignIn from "./pages/signIn/SignIn";
import SignUp from "./pages/signUp/SignUp";
import EmailSignUp from "./pages/signUp/EmailSignUp";

function Routes() {
  return (
    <Router>
      <Switch>
        <Route exact path="/" component={SignIn}/>
        <Route exact path="/signUp" component={SignUp}/>
        <Route exact path="/signUp/email" component={EmailSignUp}/>
      </Switch>
    </Router>
  );
}

export default Routes;
