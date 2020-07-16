import React from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import Kakao from "kakaojs";

function SignUp() {
  /*
  const kakaoLogin = async () => {
    Kakao.Auth.login({
      success: function (res: object) {
        try {
          const response = await axios.post(`진아님 api`, {
            nickname: "nickname",
          })
          if(response.status === 200) {
            console.log(response);
          }
        } catch (e) {
          console.log(e.response);
        }
            if (res.message === "회원가입 필요") {
              return (
                console.log("info.id: ", res.info.id),
                props.socialId(res.info.id),
                props.history.push("/social/signUp")
              );
            } else {
              return (
                localStorage.setItem("token", res.token),
                props.history.push("/")
              );
            });
      },
      fail: function (err) {
        console.log(err);
        notify(err);
      },
    });
  };
  */

  return (
    <div>
      <Link to="signUp/Email">
        <button>이메일</button>
      </Link>
      <button>카카오</button>
      <button>구글</button>
    </div>
  );
}

export default SignUp;
