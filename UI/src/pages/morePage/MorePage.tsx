import React from "react";
import styled from "styled-components";

import Card from "../../components/card/Card";

const MorePage: React.FC = () => {
  const data = {
    text: "",
    imgUrl: "",
  };

  return (
    <MorePageWrapper>
      <Banner></Banner>
      <MainCardsContainer>
        <Card
          width="630px"
          height=""
          data={{
            ...{
              text: "세상의 모든 진심은 한결같음으로 증명된다.",
              imgUrl: "",
            },
          }}
        />
        <Card
          width="630px"
          height=""
          data={{
            ...{
              text: "진심과 거짓 사이.",
              imgUrl: "",
            },
          }}
        />
      </MainCardsContainer>
    </MorePageWrapper>
  );
};

export default MorePage;

const MorePageWrapper = styled.div`
  /* width: 1440px; */
  height: 1560px;
  background-color: #ffffff;
`;

const Banner = styled.div`
  display: flex;
  justify-content: space-around;
  /* width: 1440px; */
  height: 190px;
  padding: 2em 0;
  background-color: #f8f8f4;
`;

const MainCardsContainer = styled.div`
  display: flex;
  justify-content: space-between;
  margin: 80px auto;
  width: 1302px;
  height: 690px;
`;
