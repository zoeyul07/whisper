import React, { useState } from "react";
import axios from "axios";
import { Row, Col } from "antd";
import "antd/dist/antd.css";
import styled from "styled-components";

function SignUp() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [nickname, setNickname] = useState("");
  const [checkNickname, setCheckNickname] = useState(false);
  const [checkEmail, setCheckEmail] = useState(false);

  const EmailCheck = (e: string) => {
    const emailRule = /^[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$/i;

    if (emailRule.test(e) === false) {
      console.log("이메일 형식이 정확한지 다시 한번 확인해 주세요.");
    } else {
      setEmail(e);
      console.log("성공");
    }
  }; //이메일 형식 확인

  const duplicateEmailCheck = async () => {
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
  }; //이메일 중복 체크(이메일 중복 체크는 회원가입 버튼 누를 때 되도록 수정)

  const passwordCheck = (e: string) => {
    setPassword(e);
    const passwordRule = /^.*(?=^.{8,20}$)(?=.*\d)(?=.*[a-zA-Z])(?=.*[!@#$%^&+=]).*$/;

    if (passwordRule.test(e) === false) {
      console.log("비밀번호는 영어, 특수문자, 숫자 포함 8~20자여야 합니다.");
    } else {
      setPassword(e);
      console.log("성공");
    }
  }; //비밀번호 형식 확인

  const nickNameCheck = async (e: string) => {
    const nickNameRule = /(?=^.{1,10})/;

    if (nickNameRule.test(e) === false) {
      console.log("닉네임은 1자이상 10자 이하여야 합니다");
    } else {
      setNickname(e);
      console.log("성공");
      setCheckNickname(true);
    } // 닉네임 형식 확인

    if (checkNickname === true) {
      try {
        let res = await axios.post(`${""}user/check-nickname`, {
          nickname: nickname,
        });
        if (res.status === 200) {
          console.log(res);
        }
      } catch (e) {
        console.log(e);
      }
    } // 닉네임 중복 확인
  }; //닉네임 형식 및 중복 확인

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
    //인증하기 추가 코드 필요합니다.
  }; //백으로 유저 정보 보내기

  return (
    <Row style={{ height: "100%" }}>
      <Col span={12} />
      <Col span={12} style={{ backgroundColor: "#f8f8f4" }}>
        <SiteName>소근</SiteName>
        <Right>
          <Title>회원가입</Title>
          <div>
            <InputTitle>메일</InputTitle>
            <InputBox onChange={(e) => EmailCheck(e.target.value)} />
          </div>
          <div>
            <InputTitle>비밀번호</InputTitle>
            <InputBox onChange={(e) => passwordCheck(e.target.value)} />
          </div>
          <div>
            <InputTitle>비밀번호 확인</InputTitle>
            <InputBox onChange={(e) => setConfirm(e.target.value)} />
          </div>
          <div>
            <InputTitle>닉네임</InputTitle>
            <InputBox onChange={(e) => nickNameCheck(e.target.value)} />
          </div>
          <div>
            <SignUpButton onClick={register}>Register</SignUpButton>
            <LoginButton>Login</LoginButton>
          </div>
        </Right>
        <CheckBox onClick={duplicateEmailCheck}>중복체크</CheckBox>
      </Col>
    </Row>
  );
}

const Right = styled.div`
  position: absolute;
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: AppleSDGothicNeo;
  font-stretch: normal;
  font-style: normal;
  line-height: normal;
`;

const SiteName = styled.p`
  margin: 58px 0 0 50px;
  font-family: AppleSDGothicNeo;
  font-size: 18px;
  font-weight: 600;
  letter-spacing: 0.51px;
  color: #6b6c6f;
`;

const Title = styled.p`
  width: 351px;
  margin: 233px 0 3px 0;
  font-size: 24px;
  font-weight: 600;
  letter-spacing: 0.69px;
  color: #252529;
`;

const InputTitle = styled.p`
  margin: 20px 0 11px 0;
  font-size: 12px;
  font-weight: 600;
  letter-spacing: 0.34px;
  color: #6b6c6f;
`;

const InputBox = styled.input`
  width: 351px;
  height: 38px;
  opacity: 0.7;
  border-radius: 4px;
  border: solid 1px #686565;
  background-color: #f8f8f4;
`;

const CheckBox = styled.button`
  width: 90px;
  height: 36px;
  border-radius: 20px;
  border: solid 1px #686565;
  background-color: rgba(255, 255, 255, 0);
  font-size: 12px;
  font-weight: 300;
  letter-spacing: 0.34px;
  color: #252529;
  text-align: center;
  line-height: 36px;
  position: relative;
`;

const SignUpButton = styled.button`
  width: 160px;
  height: 40px;
  border-radius: 20px;
  border: solid 2px #686565;
  background-color: rgba(255, 255, 255, 0);
  margin: 31px 30px 0 0;
`;

const LoginButton = styled.button`
  width: 160px;
  height: 40px;
  border-radius: 20px;
  background-color: #faa02a;
  color: #ffffff;
  margin-top: 31px;
`;

export default SignUp;
