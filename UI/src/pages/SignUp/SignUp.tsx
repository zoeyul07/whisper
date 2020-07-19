import React, { useState } from "react";
import axios from "axios";

function SignUp() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [nickname, setNickname] = useState("");
  const [checkNickname, setCheckNickname] = useState(false);
  const [checkEmail, setCheckEmail] = useState(false);

  const EmailCheck = (e: string) => {
    const emailRule = /^[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$/i;

    if(emailRule.test(e) === false) {
      console.log("이메일 형식이 정확한지 다시 한번 확인해 주세요.")
    } else {
      setEmail(e);
      console.log("성공")
    }
  } //이메일 형식 확인

  const duplicateEmailCheck = async() => {
    try {
      const response = await axios.post(`${"서율님 api"}user/check-email`, {
        "email": email,
      });
      if(response.status === 200) {
        console.log(response);
        setCheckEmail(true);
      }
    } catch (e) {
      console.log(e.response);
    }
  } //이메일 중복 체크(이메일 중복 체크는 회원가입 버튼 누를 때 되도록 수정)

  const passwordCheck = (e: string) => {
    setPassword(e);
    const passwordRule = /^.*(?=^.{8,20}$)(?=.*\d)(?=.*[a-zA-Z])(?=.*[!@#$%^&+=]).*$/;

    if(passwordRule.test(e) === false) {
      console.log("비밀번호는 영어, 특수문자, 숫자 포함 8~20자여야 합니다.")
    } else {
      setPassword(e);
      console.log("성공");
    }
  } //비밀번호 형식 확인

  const nickNameCheck = async(e: string) => {
    const nickNameRule = /(?=^.{1,10})/;

    if(nickNameRule.test(e) === false) {
      console.log("닉네임은 1자이상 10자 이하여야 합니다");
    } else {
      setNickname(e);
      console.log("성공");
      setCheckNickname(true);
    }

    if(checkNickname === true) {
      try {
        let res = await axios.post(`${""}user/check-nickname`, {
          "nickname": nickname,
        });
        if(res.status === 200) {
          console.log(res);
        }
      } catch (e) {
        console.log(e)
      }
    }
  } //닉네임 형식 확인

  const register = async() => {
    if(password === confirm && checkEmail === true) {
      try {
        const response = await axios.post(`${"서율님 api"}user/sign-up`, {
          "email": email,
          "password": password,
          "nickname": nickname,
        });
        if(response.status === 200) {
          console.log(response);
        }
      } catch (e) {
        console.log(e.response);
      }
    }
    //인증하기 추가 코드 필요합니다.
  } //백으로 유저 정보 보내기

  return (
    <div>
      <div>
        <span>메일</span>
        <input onChange={(e)=>EmailCheck(e.target.value)}/>
        <button onClick={duplicateEmailCheck}>이메일 중복체크</button>
      </div>
      <div>
        <span>비밀번호</span>
        <input onChange={(e)=>passwordCheck(e.target.value)}/>
      </div>
      <div>
        <span>비밀번호 확인</span>
        <input onChange={(e)=>setConfirm(e.target.value)}/>
      </div>
      <div>
        <span>닉네임</span>
        <input onChange={(e)=>nickNameCheck(e.target.value)}/>
      </div>
      <div>
        <button onClick={register}>Register</button>
        <button>Login</button>
      </div>
    </div>
  );
}

export default SignUp;