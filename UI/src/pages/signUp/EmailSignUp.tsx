import React, { useState } from "react";
import axios from "axios";

function SignUp() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [nickname, setNickname] = useState("");
  const [checkEmail, setCheckEmail] = useState(false);

  const register = async () => {
    if (password === confirm && checkEmail === true) {
      try {
        const response = await axios.post(`${"서율님 api"}user/sign-up`, {
          email: email,
          password: password,
          nickname: nickname,
        });
        if (response.status === 200) {
          console.log(response);
        }
      } catch (e) {
        console.log(e.response);
      }
    }
  }; //백으로 유저 정보 보내기

  const duplicateCheck = async () => {
    try {
      const response = await axios.post(`${"서율님 api"}user/check-email`, {
        email: email,
      });
      if (response.status === 200) {
        console.log(response);
        setCheckEmail(true);
      }
    } catch (e) {
      console.log(e.response);
    }
  }; //이메일 중복 체크

  const certification = () => {}; //인증하기

  return (
    <div>
      <div>
        <span>메일</span>
        <input onChange={(e) => setEmail(e.target.value)} />
        <button onClick={duplicateCheck}>이메일 중복체크</button>
        <button onClick={certification}>인증하기</button>
      </div>
      <div>
        <span>비밀번호</span>
        <input onChange={(e) => setPassword(e.target.value)} />
      </div>
      <div>
        <span>비밀번호 확인</span>
        <input onChange={(e) => setConfirm(e.target.value)} />
      </div>
      <div>
        <span>닉네임</span>
        <input onChange={(e) => setNickname(e.target.value)} />
      </div>
      <div>
        <button onClick={register}>Register</button>
        <button>Login</button>
      </div>
    </div>
  );
}

export default SignUp;
