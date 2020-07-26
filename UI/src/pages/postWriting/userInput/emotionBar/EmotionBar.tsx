import React, { useState } from "react";
import styled from "styled-components";

import Emotion from "../../../../components/emotion/Emotion";

const EmotionBar: React.FC = () => {
  const emotionProps = {
    width: "auto",
    height: "auto",
    emotion: "",
  };

  const [num, setNum] = useState<string>("");

  const handleSubmit = (id: any): void => {
    console.log("id", id);
    setNum(id);
  };

  return (
    <EmotionBarWrapper>
      {console.log("num", num)}
      <Emotion
        width={emotionProps.width}
        height={emotionProps.height}
        emotion={emotionProps.emotion}
        id="1"
        color={num === "1" ? "blue" : ""}
        cc={handleSubmit}
      />
      <Emotion
        width={emotionProps.width}
        height={emotionProps.height}
        emotion={emotionProps.emotion}
        id="2"
        color={num === "2" ? "blue" : ""}
        cc={handleSubmit}
      />
      <Emotion
        width={emotionProps.width}
        height={emotionProps.height}
        emotion={emotionProps.emotion}
        id="3"
        color={num === "3" ? "blue" : ""}
        cc={handleSubmit}
      />
      <Emotion
        width={emotionProps.width}
        height={emotionProps.height}
        emotion={emotionProps.emotion}
        id="4"
        color={num === "4" ? "blue" : ""}
        cc={handleSubmit}
      />
      <Emotion
        width={emotionProps.width}
        height={emotionProps.height}
        emotion={emotionProps.emotion}
        id="5"
        color={num === "5" ? "blue" : ""}
        cc={handleSubmit}
      />
      <Emotion
        width={emotionProps.width}
        height={emotionProps.height}
        emotion={emotionProps.emotion}
        id="6"
        color={num === "6" ? "blue" : ""}
        cc={handleSubmit}
      />
      <Emotion
        width={emotionProps.width}
        height={emotionProps.height}
        emotion={emotionProps.emotion}
        id="7"
        color={num === "7" ? "blue" : ""}
        cc={handleSubmit}
      />
      <Emotion
        width={emotionProps.width}
        height={emotionProps.height}
        emotion={emotionProps.emotion}
        id="8"
        color={num === "8" ? "blue" : ""}
        cc={handleSubmit}
      />
      <Emotion
        width={emotionProps.width}
        height={emotionProps.height}
        emotion={emotionProps.emotion}
        id="9"
        color={num === "9" ? "blue" : ""}
        cc={handleSubmit}
      />
      <Emotion
        width={emotionProps.width}
        height={emotionProps.height}
        emotion={emotionProps.emotion}
        id="10"
        color={num === "10" ? "blue" : ""}
        cc={handleSubmit}
      />
    </EmotionBarWrapper>
  );
};

export default EmotionBar;

const EmotionBarWrapper = styled.div`
  display: flex;
  height: 128px;
  margin: 16px 8px;
  align-items: center;
  justify-content: center;
  background-color: #f2f2f2;
`;
