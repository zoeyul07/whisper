import React from "react";
import styled from "styled-components";

interface MyPostProps {
  name: string;
  username: string;
}

const MyPost: React.FunctionComponent<MyPostProps> = (props) => {
  const { name, username } = props;
  return (
    <Container>
      <Imoticon>{name}</Imoticon>
      <Text>{username}</Text>
    </Container>
  );
};

export default MyPost;

const Container = styled.div`
  width: 290px;
  height: 400px;
  margin: 0 20px 30px 0;
  box-shadow: 0 2px 6px 0 rgba(47, 83, 151, 0.1);
  /* display: flex; */
`;

const Imoticon = styled.p`
  /* width: 165px;
  height: 64px; */
  font-size: 18px;
  font-weight: 600;
  line-height: 1.78;
  text-align: center;
  color: #1b2437;
`;

const Text = styled.div``;
