import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import GlobalStyle from "./Config";
import SignIn from "./pages/SignIn/SignIn";
import SignUp from "./pages/SignUp/SignUp";
import postWriting from "./pages/PostWriting/PostWriting";
import EmailSignIn from "./pages/SignIn/EmailSignIn";

function Routes() {
  return (
    <Router>
      <GlobalStyle />
      <Switch>
        <Route exact path="/" component={SignIn} />
        <Route exact path="/signUp" component={SignUp} />
        <Route exact path="/post/writing" component={postWriting} />
        <Route exact path="/emailSignIn" component={EmailSignIn} />
      </Switch>
    </Router>
  );
}

export default Routes;
