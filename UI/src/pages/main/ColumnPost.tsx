import React from "react";
import styled from "styled-components";
import imoticon from "./imoticon.png";
import heart from "./Heart.svg";

interface ColumnPostProps {
  name: string;
  username: string;
}

const ColumnPost: React.FunctionComponent<ColumnPostProps> = (props) => {
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

export default ColumnPost;

const Post = styled.div`
  width: 20%;
  height: 100%;
  background-color: rgba(255, 252, 67, 0.2);
  border: 1px solid #ececec;
`;

const Heart = styled.svg`
  width: 24px;
  height: 24px;
`;

const Imoticon = styled.div`
  width: 84px;
  height: 80px;
  margin: 70px auto 0 auto;
  background-image: url(${imoticon});
  background-size: cover;
  opacity: 70%;
`;

const Content = styled.div``;

const Username = styled.div``;
