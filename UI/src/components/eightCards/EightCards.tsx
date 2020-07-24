import React from "react";
import styled from "styled-components";

import Card from "../card/Card";

interface WrapperProps {
  width: string;
  height: string;
}

const EightCards: React.FC<WrapperProps> = ({ width, height }) => {
  const data = {
    text: "세상의 모든 진심은 한결같음으로 증명된다.",
    imgUrl: "",
  };

  const cardWidth = width.slice(0, -2) + "px";

  return (
    <EightCardsWrapper width={width} height={height}>
      <Card width={"auto"} height={"auto"} data={{ ...data }} />
      <Card width={"auto"} height={"auto"} data={{ ...data }} />
      <Card width={"auto"} height={"auto"} data={{ ...data }} />
      <Card width={"auto"} height={"auto"} data={{ ...data }} />
      <Card width={"auto"} height={"auto"} data={{ ...data }} />
      <Card width={"auto"} height={"auto"} data={{ ...data }} />
      <Card width={"auto"} height={"auto"} data={{ ...data }} />
      <Card width={"auto"} height={"auto"} data={{ ...data }} />
    </EightCardsWrapper>
  );
};

export default EightCards;

const EightCardsWrapper = styled.div<WrapperProps>`
  display: grid;
  margin: 160px auto;
  grid-gap: 25px;
  grid-template-rows: repeat(2, 1fr);
  grid-template-columns: repeat(4, 1fr);
  width: ${({ width }) => width};
  height: ${({ height }) => height};
`;
