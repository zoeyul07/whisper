import React from "react";
import styled from "styled-components";

function PostWriting() {
  return (
    <PostWritingWrapper>
      <Banner>
        <Title>당신의 오늘</Title>
        <SubTitle>오늘 무슨 일이 있었는지 생각해보세요</SubTitle>
      </Banner>
      <UserInput></UserInput>
    </PostWritingWrapper>
  );
}

export default PostWriting;

const PostWritingWrapper = styled.div`
  width: 1440px;
  height: 1560px;
  background-color: #ffffff;
`;

const Banner = styled.div`
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  width: 1440px;
  height: 214px;
  padding: 2em 0;
  background-color: #f8f8f4;
`;

const Title = styled.p`
  margin: 0;
  width: 100%;
  /* height: 72px; */
  font-family: AppleSDGothicNeo;
  font-size: 60px;
  font-weight: 600;
  font-stretch: normal;
  font-style: normal;
  line-height: normal;
  letter-spacing: normal;
  text-align: center;
  color: #1b2437;
`;

const SubTitle = styled.p`
  margin: 0;
  width: 100%;
  /* height: 43px; */
  font-family: AppleSDGothicNeo;
  font-size: 36px;
  font-weight: 300;
  font-stretch: normal;
  font-style: normal;
  line-height: normal;
  letter-spacing: normal;
  text-align: center;
  color: #1b2437;
`;

const UserInput = styled.div`
  margin: 5em;
  /* width: 1323px; */
  height: 851px;
  background-color: #d8d8d8;
`;
