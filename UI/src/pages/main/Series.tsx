import React from "react";
import styled from "styled-components";

interface SeriesProps {
  name: string;
}

const Series: React.FunctionComponent<SeriesProps> = (props) => {
  const { name } = props;
  return (
    <SeriesPost>
      <SeriesTitle>{name}</SeriesTitle>
    </SeriesPost>
  );
};

export default Series;

const SeriesPost = styled.div`
  width: 187px;
  height: 160px;
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
