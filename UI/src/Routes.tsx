import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import GlobalStyle from "./Config";
import SignIn from "./pages/signIn/SignIn";
import SignUp from "./pages/signUp/SignUp";
import EmailSignUp from "./pages/signUp/EmailSignUp";
import PostWriting from "./pages/postWriting/PostWriting";
import MorePage from "./pages/morePage/MorePage";

function Routes() {
  return (
    <Router>
      <GlobalStyle />
      <Switch>
        <Route exact path="/" component={SignIn} />
        <Route exact path="/signUp" component={SignUp} />
        <Route exact path="/signUp/email" component={EmailSignUp} />
        <Route exact path="/post/writing" component={PostWriting} />
        <Route exact path="/more" component={MorePage} />
      </Switch>
    </Router>
  );
}

export default Routes;
