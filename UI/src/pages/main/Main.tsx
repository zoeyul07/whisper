import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import styled from "styled-components";
import { MenuOutlined } from "@ant-design/icons";
import Button from "./Button";
import ColumnPost from "./ColumnPost";
import Series from "./Series";
import axios from "axios";
import background from "./bg.jpg";
import MyPost from "./MyPost";

function Main() {
  const [seriesTitle, setSeriesTitle] = useState<string>("");
  const [myPosts, setMyPosts] = useState([]);
  const [series, setSeries] = useState([]);
  const [others, setOthers] = useState([]);

  const createTitle = (e: any) => {
    setSeriesTitle(e.target.value);
    console.log(seriesTitle);
  };

  const inputHandler = (e: any) => {
    console.log("title", seriesTitle);
  };

  // useEffect(() => {
  //   const getOthers = async () => {
  //     try {
  //       const response = await axios.get(
  //         `${"http://172.30.1.11:5000/"}diary?offset=0&limit=6`
  //       );
  //       if (response.status === 200) {
  //         console.log(response.data);
  //         setOthers(response.data);
  //       }
  //     } catch (e) {
  //       console.log(e.response);
  //     }
  //   };
  //   getOthers();
  // }, []); // 일주일 내 글 가져오기

  useEffect(() => {
    const getThisWeek = async () => {
      try {
        const response = await axios.get(
          `https://jsonplaceholder.typicode.com/users`
        );
        if (response.status === 200) {
          console.log(response.data);
          setMyPosts(response.data);
        }
      } catch (e) {
        console.log(e.response);
      }
    };
    getThisWeek();
  }, []); // 일주일 내 글 가져오기

  useEffect(() => {
    const getSeries = async () => {
      try {
        const response = await axios.get(
          `https://jsonplaceholder.typicode.com/users`
        );
        if (response.status === 200) {
          if (response.data.length === 10) {
            //setSeries("당신의 이야기를 만들어보세요.");
            console.log("aaaa");
          }
          console.log(response.data);
          setSeries(response.data);
        }
      } catch (e) {
        console.log(e.response);
      }
    };
    getSeries();
  }, []); // 시리즈 목록 가져오기

  return (
    <Container>
      <MainNav>
        <MenuOutlined />
        <Title>소근</Title>
      </MainNav>
      <Banner>
        {/* <BannerImg src={background} alt="bannerImg" /> */}
        <BannerTitle>
          당신의 오늘은 어땠나요?
          <br />
          소근에게 알려주세요
        </BannerTitle>
      </Banner>
      <PostContainer>
        <Button buttonName={"MORE"} buttonText={"더 보기"} />
        <Posts>
          {others.map((data: any, id: number) => {
            if (data.id === 1) {
              return <ColumnPost name={data.name} username={data.username} />;
            }
          })}

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
        </Posts>
      </PostContainer>
      <MyTitle>당신의 일주일</MyTitle>
      <MyPostContainer>
        <Button buttonName={"WRITE"} buttonText={"글쓰기"} />
        <MyPostRow>
          {myPosts.map((data: any, id: number) => {
            return <MyPost name={data.name} username={data.username} />;
          })}
        </MyPostRow>
      </MyPostContainer>
      <SeriesTitle>다른 이야기들</SeriesTitle>
      <SeriesContainer>
        <CreateArea>
          <TitleInput onChange={(e) => createTitle(e)} />
          {/* <Button isEnable={true} buttonName={"CREATE"} buttonText={"만들기"} /> */}
          <CreateButton onClick={inputHandler}>만들기</CreateButton>
        </CreateArea>
        <SeriesArea>
          <SeriesBox>
            {series.map((data: any, id: number) => {
              return <Series name={data.name} />;
            })}
          </SeriesBox>
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
  background-image: url(${background});
  background-size: cover;
  background-position-y: center;
  display: flex;
  justify-content: center;
  align-items: center;
`;

const BannerTitle = styled.h2`
  //padding: 270px 0 0 46px;
  font-size: 16px;
  line-height: 1.2;
  text-align: center;
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
  /* width: 90%; */
  width: 1260px;
  height: 830px;
`;

const MyPostRow = styled.div`
  display: flex;
  flex-wrap: wrap;
  margin-bottom: 30px;
`;

// const MyPosts = styled.div`
//   width: 25%;
//   height: 400px;
//   margin-right: 20px;
//   box-shadow: 0 2px 6px 0 rgba(47, 83, 151, 0.1);
// `;

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

const CreateButton = styled.button`
  width: 90px;
  height: 36px;
  border-radius: 20px;
  margin-bottom: 20px;
  background-color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #686565;
  font-size: 12px;
  color: #252529;
  opacity: 0.7;
`;

const SeriesArea = styled.div`
  width: 100%;
  height: 300px;
  //background-color: wheat;
`;

const SeriesBox = styled.div`
  display: flex;
  flex-wrap: wrap;
  align-items: center;
`;
