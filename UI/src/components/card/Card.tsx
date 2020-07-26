import React from "react";
import styled from "styled-components";

interface CardProps {
  width: string;
  height: string;
  data: {
    text: string;
    imgUrl: string;
  };
}

interface CardIconProps {
  readonly imgUrl: string;
}

interface CardWrapProps {
  readonly width: string;
  readonly height: string;
}

const Card: React.FC<CardProps> = ({ width, height, data }) => {
  return (
    <CardWrap width={width} height={height}>
      {/* <CardIcon imgUrl={data.imgUrl} /> */}
      <CardIcon imgUrl={process.env.PUBLIC_URL + "/images/happy.png"} />
      <CardText>{data.text}</CardText>
    </CardWrap>
  );
};

export default Card;

const CardWrap = styled.div<CardWrapProps>`
  width: ${({ width }) => width};
  height: ${({ height }) => height};
  border: 1px solid #8f8f8f;
  border-radius: 3px;
  box-shadow: 0 2px 6px 0 rgba(47, 83, 151, 0.1);
  background-color: #ffffff;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
`;

//img는 어떤방식으로 로드 할건지. img 형태, icon 형태?
const CardIcon = styled.div<CardIconProps>`
  width: 80px;
  height: 76px;
  opacity: 0.7;
  background-image: url(${({ imgUrl }) => imgUrl});
  background-size: 80px 76px;
  background-position: center;
  margin-bottom: 50px;
`;

const CardText = styled.div`
  line-height: 32px;
  font-family: "AppleSDGothicNeo-SemiBold";
  font-size: 18px;
  /* font-weight: 600; */
  text-align: center;
  color: #1b2437;
`;
