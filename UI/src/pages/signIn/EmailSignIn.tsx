import React, { useState } from "react";
import axios from "axios";
import { Row, Col } from "antd";
import "antd/dist/antd.css";
import styled from "styled-components";

function EmailSignIn() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const EmailCheck = (e: string) => {
    const emailRule = /^[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*@[0-9a-zA-Z]([-_\.]?[0-9a-zA-Z])*\.[a-zA-Z]{2,3}$/i;

    if (emailRule.test(e) === false) {
      console.log("이메일 형식이 정확한지 다시 한번 확인해 주세요.");
    } else {
      setEmail(e);
      console.log("성공");
    }
  }; //이메일 형식 확인

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

  const EmailLogin = async () => {
    try {
      let res = await axios.post(`${""}user/sign-in`, {
        email: email,
        password: password,
      });
      console.log(res);
    } catch (e) {
      console.log(e);
    }
  }; //이메일 로그인

  return (
    <Row style={{ height: "100%" }}>
      <Col span={12} />
      <Col span={12} style={{ backgroundColor: "#f8f8f4" }}>
        <SiteName>소근</SiteName>
        <Right>
          <Title>로그인</Title>
          <div>
            <InputTitle>메일</InputTitle>
            <InputBox onChange={(e) => EmailCheck(e.target.value)} />
          </div>
          <div>
            <InputTitle>비밀번호</InputTitle>
            <InputBox onChange={(e) => passwordCheck(e.target.value)} />
          </div>
          <div style={{ width: "351px" }}>
            <LoginButton onClick={EmailLogin}>Login</LoginButton>
          </div>
        </Right>
      </Col>
    </Row>
  );
}

const Right = styled.div`
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  font-family: AppleSDGothicNeo;
  font-stretch: normal;
  font-style: normal;
  line-height: normal;
  width: 100%;
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

const LoginButton = styled.button`
  width: 160px;
  height: 40px;
  border-radius: 20px;
  background-color: #faa02a;
  color: #ffffff;
  margin-top: 31px;
`;

export default EmailSignIn;
