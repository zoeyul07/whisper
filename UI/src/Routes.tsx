import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import GlobalStyle from "./Config";

import SignIn from "./pages/signIn/SignIn";
import SignUp from "./pages/signUp/SignUp";
import postWriting from "./pages/postWriting/PostWriting";
import Main from "./pages/main/Main";
import EmailSignIn from "./pages/signIn/EmailSignIn";

function Routes() {
  return (
    <Router>
      <GlobalStyle />
      <Switch>
        <Route exact path="/" component={SignIn} />
        <Route exact path="/signUp" component={SignUp} />
        <Route exact path="/post/writing" component={postWriting} />
        <Route exact path="/main" component={Main} />
        <Route exact path="/emailSignIn" component={EmailSignIn} />
      </Switch>
    </Router>
  );
}

export default Routes;
