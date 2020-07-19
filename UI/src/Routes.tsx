import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import SignIn from "./pages/signIn/SignIn";
import SignUp from "./pages/signUp/SignUp";

function Routes() {
  return (
    <Router>
      <Switch>
        <Route exact path="/" component={SignIn}/>
        <Route exact path="/signUp" component={SignUp}/>
      </Switch>
    </Router>
  );
}

export default Routes;
