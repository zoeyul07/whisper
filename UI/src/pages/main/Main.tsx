import React, { useState } from "react";
import { Link } from "react-router-dom";
import styled from "styled-components";
import { MenuOutlined } from "@ant-design/icons";
import Button from "./Button";
import ColumnPost from "./ColumnPost";
import Series from "./Series";

function Main() {
  const [seriesTitle, setseriesTitle] = useState<string>("");

  const inputHandler = () => {
    console.log("AA");
  };

  return (
    <Container>
      <MainNav>
        <MenuOutlined />
        <Title>소근</Title>
      </MainNav>
      <Banner>
        <BannerTitle>
          당신의 오늘은 어땠나요?
          <br />
          소근에게 알려주세요
        </BannerTitle>
      </Banner>
      <PostContainer>
        <Button buttonName={"MORE"} buttonText={"더 보기"} />
        <Posts>
          <ColumnPost />
          <RowContainer>
            <Row>
              <RowPost></RowPost>
              <RowPost></RowPost>
            </Row>
            <Row>
              <RowPost></RowPost>
              <RowPost></RowPost>
            </Row>
          </RowContainer>
          <ColumnPost />
        </Posts>
      </PostContainer>
      <MyTitle>당신의 일주일</MyTitle>
      <MyPostContainer>
        <Button buttonName={"WRITE"} buttonText={"글쓰기"} />
        <MyPostRow>
          <MyPosts></MyPosts>
          <MyPosts></MyPosts>
          <MyPosts></MyPosts>
          <MyPosts></MyPosts>
        </MyPostRow>
        <MyPostRow>
          <MyPosts></MyPosts>
          <MyPosts></MyPosts>
          <MyPosts></MyPosts>
          <MyPosts></MyPosts>
        </MyPostRow>
      </MyPostContainer>
      <SeriesTitle>다른 이야기들</SeriesTitle>
      <SeriesContainer>
        <CreateArea>
          <TitleInput />
          <Button isEnable={true} buttonName={"CREATE"} buttonText={"만들기"} />
          {/* <CreateButton onClick={inputHandler}>만들기</CreateButton> */}
        </CreateArea>
        <SeriesArea>
          {/* <SeriesBox>
            <Series />
            <Series />
            <Series />
            <Series />
          </SeriesBox> */}
        </SeriesArea>
      </SeriesContainer>
    </Container>
  );
}

export default Main;

const Container = styled.div`
  margin: 0;
  padding: 0;
`;

const MainNav = styled.div`
  width: 50%;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: space-between;
`;

const Title = styled.div`
  font-size: 20px;
`;

const Banner = styled.div`
  width: 100%;
  height: 410px;
  background-color: coral;
`;

const BannerTitle = styled.div`
  padding: 270px 0 0 46px;
  font-size: 32px;
  line-height: 1.6;
  color: #ffffff;
`;

const PostContainer = styled.div`
  margin-top: 160px;
  padding: 0 64px;
`;

const Posts = styled.div`
  width: 100%;
  height: 460px;
  display: flex;
`;

const RowContainer = styled.div`
  display: flex;
  flex-direction: column;
  width: 60%;
  height: 100%;
`;

const Row = styled.div`
  display: flex;
  height: 100%;
  /* flex-wrap: wrap; */
`;

const RowPost = styled.div`
  display: flex;
  flex-wrap: wrap;
  width: 50%;
  height: 100%;
  background-color: rgba(245, 103, 103, 0.2);
  border: 1px solid #ececec;
`;

const MyTitle = styled.div`
  font-size: 60px;
  font-weight: 600;
  text-align: center;
  color: #1b2437;
  margin: 160px 0 200px 0;
`;

const MyPostContainer = styled.div`
  margin: 0 44px 0 64px;
  width: 90%;
  height: 830px;
`;

const MyPostRow = styled.div`
  display: flex;
  margin-bottom: 30px;
`;

const MyPosts = styled.div`
  width: 25%;
  height: 400px;
  margin-right: 20px;
  box-shadow: 0 2px 6px 0 rgba(47, 83, 151, 0.1);
`;

const SeriesTitle = styled.div`
  font-size: 60px;
  font-weight: 600;
  text-align: center;
  color: #1b2437;
  margin: 160px 0 200px 0;
`;

const SeriesContainer = styled.div`
  margin: 0 220px;
`;

const CreateArea = styled.div`
  width: 100%;
  display: flex;
  justify-content: flex-end;
  opacity: 0.7;
`;

const TitleInput = styled.input`
  width: 600px;
  height: 30px;
  margin-right: 20px;
`;

// const CreateButton = styled.button`
//   width: 90px;
//   height: 36px;
//   border-radius: 20px;
//   margin-bottom: 20px;
//   background-color: #ffffff;
//   display: flex;
//   align-items: center;
//   justify-content: center;
//   border: 1px solid #686565;
//   font-size: 12px;
//   color: #252529;
// `;

const SeriesArea = styled.div`
  width: 100%;
  height: 300px;
  background-color: wheat;
`;

const SeriesBox = styled.div`
  display: flex;
  align-items: center;
`;
