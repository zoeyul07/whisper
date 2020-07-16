import React from "react";
import { Link } from "react-router-dom";

function SignIn(props: {}) {

  return (
    <div>
      <button>email</button>
      <button>kakao</button>
      <button>google</button>
      <Link to="/signUp">
        <button>소근과 함께하기</button>
      </Link>
    </div>);
}

export default SignIn;