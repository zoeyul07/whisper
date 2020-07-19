import React from "react";
import { Link } from "react-router-dom";
import axios from "axios";
import Kakao from "kakaojs";
import { GoogleLogin } from "react-google-login";

declare global {
  interface Window {
    Kakao: any;
  }
}

function SignIn(props: {}) {
  const KakaoLogin = () => {
    Kakao.init('418bd12c3a35441d58e113ac8cd7b654');
    Kakao.Auth.login({
      success: async function(authObj: any) {
        console.log(authObj);
        try {
          let res = await axios.post(`${""}user/kakao`, {
            headers: {
              Authorization: authObj.access_token,
            },
            data: {
              "nickname": "nickname",
            }
          })
          console.log(res);
        } catch (e) {
          console.log(e)
        }
      },
      fail: function(err: any) {
        console.log(err);
      },
    });
  } //카카오 소셜 로그인

  const responseGoogle = async(response: any) => {
    console.log(response);
    try {
      let res =  await axios.post(`${""}user/goolge`, {
        headers: {
          Authorization: response.tokenObj.access_token,
        },
        data: {
          "nickname": "nicknmae",
        }
      })
      console.log(res);
    } catch (e) {
      console.log(e);
    }
  }

  return (
    <div>
      <button>email</button>
      <button onClick={KakaoLogin}>kakao</button>
      <GoogleLogin
        clientId="999952350863-tuacfmh4cjfangjkn58pbnio6boa7non.apps.googleusercontent.com"
        buttonText="Login"
        onSuccess={responseGoogle}
        onFailure={responseGoogle}
        cookiePolicy={'single_host_origin'}
      />
      <Link to="/signUp">
        <button>소근과 함께하기</button>
      </Link>
    </div>);
}

export default SignIn;