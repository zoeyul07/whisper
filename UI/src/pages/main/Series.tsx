import React from "react";
import styled from "styled-components";

function Series() {
  return (
    <SeriesPost>
      <SeriesTitle>월요일</SeriesTitle>
    </SeriesPost>
  );
}

export default Series;

const SeriesPost = styled.div`
  width: 250px;
  height: 220px;
  border: solid 1px #686565;
  opacity: 0.7;
  display: flex;
  align-items: center;
  justify-content: center;
`;

const SeriesTitle = styled.div`
  font-size: 18px;
  color: #686565;
`;
