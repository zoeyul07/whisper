import React from "react";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import GlobalStyle from "./Config";
<<<<<<< HEAD
import SignIn from "./pages/signIn/SignIn";
import SignUp from "./pages/signUp/SignUp";
import postWriting from "./pages/postWriting/PostWriting";
import Main from "./pages/main/Main";
=======
import SignIn from "./pages/SignIn/SignIn";
import SignUp from "./pages/SignUp/SignUp";
import postWriting from "./pages/PostWriting/PostWriting";
import EmailSignIn from "./pages/SignIn/EmailSignIn";
>>>>>>> e32ea0b31366866a0746c3760c288b2441b8b593

function Routes() {
  return (
    <Router>
      <GlobalStyle />
      <Switch>
        <Route exact path="/" component={SignIn} />
        <Route exact path="/signUp" component={SignUp} />
        <Route exact path="/post/writing" component={postWriting} />
<<<<<<< HEAD
        <Route exact path="/main" component={Main} />
=======
        <Route exact path="/emailSignIn" component={EmailSignIn} />
>>>>>>> e32ea0b31366866a0746c3760c288b2441b8b593
      </Switch>
    </Router>
  );
}

export default Routes;
