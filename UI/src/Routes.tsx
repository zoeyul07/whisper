import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import GlobalStyle from "./Config";
import SignIn from "./pages/signIn/SignIn";
import SignUp from "./pages/signUp/SignUp";
import postWriting from "./pages/postWriting/PostWriting";
import Main from "./pages/main/Main";

function Routes() {
  return (
    <Router>
      <GlobalStyle />
      <Switch>
        <Route exact path="/" component={SignIn} />
        <Route exact path="/signUp" component={SignUp} />
        <Route exact path="/post/writing" component={postWriting} />
        <Route exact path="/main" component={Main} />
      </Switch>
    </Router>
  );
}

export default Routes;
