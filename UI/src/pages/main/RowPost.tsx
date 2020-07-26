import React from "react";
import styled from "styled-components";
import imoticon from "./imoticon.png";
//import heart from "./Heart.svg";

interface RowPostProps {
  name: string;
  username: string;
}

const RowPost: React.FunctionComponent<RowPostProps> = (props) => {
  const { name, username } = props;
  return (
    <Post>
      <Heart></Heart>
      <Imoticon></Imoticon>
      <Content>{name}</Content>
      <Username>{username}</Username>
    </Post>
  );
};

export default RowPost;

const Post = styled.div`
  width: 290px;
  height: 400px;
  margin: 0 20px 30px 0;
  box-shadow: 0 2px 6px 0 rgba(47, 83, 151, 0.1);
`;

const Heart = styled.svg`
  width: 24px;
  height: 24px;
`;

const Imoticon = styled.p`
  width: 84px;
  height: 80px;
  margin: 70px auto 0 auto;
  background-image: url(${imoticon});
  background-size: cover;
  opacity: 70%;
`;

const Content = styled.div``;

const Username = styled.div``;
