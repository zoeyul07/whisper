import React from "react";
import styled from "styled-components";

import { SmileOutlined } from "@ant-design/icons";

interface WrapperProps {
  width: string;
  height: string;
  emotion?: string;
}

const Emotion: React.FC<WrapperProps> = ({ width, height, emotion }) => {
  return (
    <EmotionWrapper width={width} height={height}>
      <SmileOutlined style={{ fontSize: `85px` }} />
      <Text>{emotion}</Text>
    </EmotionWrapper>
  );
};

export default Emotion;

const EmotionWrapper = styled.div<WrapperProps>`
  display: flex;
  flex-direction: column;
  justify-content: space-around;
  text-align: center;
  width: ${({ width }) => width};
  height: ${({ height }) => height};
  padding: 5px 20px;
  /* border: 1px solid blue; */
`;

const Text = styled.span`
  /* margin: 10px; */
  font-family: "AppleSDGothicNeo-Light";
  font-size: 16px;
  letter-spacing: 0.46px;
  color: "#6b6c6f";
`;
