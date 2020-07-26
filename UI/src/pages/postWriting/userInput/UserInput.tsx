import React, { useState } from "react";
import styled, { css } from "styled-components";

interface UserStoryProps {
  fontStyle?: string;
  textAlign: string;
}

interface BoxSizeProps {
  width: string;
  height: string;
}

const UserInput: React.FC = () => {
  const [userStory, setUserStory] = useState("");
  const [textAlign, setTextAlign] = useState("left");
  const [fontStyle, setFontStyle] = useState("");

  const [userSentence, setUserSentence] = useState("");

  const handleButtonClick = () => {
    console.log("PostButton 클릭");
  };

  return (
    <UserInputWrapper>
      <ControlBar>
        <ButtonGroup>
          <ButtonBold onClick={() => setFontStyle("bold")} />
          <ButtonItalic onClick={() => setFontStyle("italic")} />
          <ButtonUnderline onClick={() => setFontStyle("underline")} />
        </ButtonGroup>
        <ButtonGroup>
          <ButtonAlignLeft onClick={() => setTextAlign("left")} />
          <ButtonAlignCenter onClick={() => setTextAlign("center")} />
          <ButtonAlignRight onClick={() => setTextAlign("right")} />
        </ButtonGroup>
      </ControlBar>

      <StoryInput
        placeholder="당신의 이야기를 적어보세요..."
        value={userStory}
        onChange={(e: React.ChangeEvent<HTMLTextAreaElement>) =>
          setUserStory(e.target.value)
        }
        fontStyle={fontStyle}
        textAlign={textAlign}
      />
      <WriteTodayWrapper width="97%" height="">
        <WriteToday width="100%" height="50px">
          <Today>오늘의 한 줄</Today>
          <TodayInput
            value={userSentence}
            onChange={(e: React.ChangeEvent<HTMLInputElement>) =>
              setUserSentence(e.target.value)
            }
          />
        </WriteToday>
        <PostButton onClick={handleButtonClick}>이야기 하기</PostButton>
      </WriteTodayWrapper>
      {console.log(userStory)}
      {console.log(textAlign)}
      {console.log(userSentence)}
    </UserInputWrapper>
  );
};

export default UserInput;

const UserInputWrapper = styled.div`
  margin: 5em auto;
  width: 1323px;
  /* height: 851px; */
  /* background-color: #d8d8d8; */
  /* border: 1px solid #686565; */
`;

const ControlBar = styled.div`
  display: flex;
  height: 64px;
  margin: 16px 8px;
  align-items: center;
  background-color: #f2f2f2;
`;

const Button = css`
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid black;
  margin: 0 7px;
`;

const ButtonGroup = styled.div`
  display: flex;
  margin: 0 16px;

  /* :first-child {
    margin-right: 20px;
  } */
`;

const ButtonBold = styled.button`
  ${Button};
`;
const ButtonItalic = styled.button`
  ${Button};
`;
const ButtonUnderline = styled.button`
  ${Button};
`;

const ButtonAlignLeft = styled.button`
  ${Button};
`;
const ButtonAlignCenter = styled.button`
  ${Button};
`;
const ButtonAlignRight = styled.button`
  ${Button};
`;

/** font-weight: bold;
 *  font-style: italic;
 *  text-decoration: underline;
 */

const StoryInput = styled.textarea<UserStoryProps>`
  width: 97%;
  height: 780px;
  margin: 1.5em 1em;
  padding: 1.8em 2em;
  border: 1px solid #828282;
  resize: none;
  font-size: 20px;
  font-weight: ${({ fontStyle }) => fontStyle};
  font-style: ${({ fontStyle }) => fontStyle};
  text-decoration: ${({ fontStyle }) => fontStyle};
  text-align: ${({ textAlign }) => textAlign};

  ::placeholder {
    font-size: 20px;
    opacity: 0.7;
  }
`;

const WriteTodayWrapper = styled.div<BoxSizeProps>`
  display: flex;
  flex-direction: column;
  vertical-align: center;
  justify-content: space-around;
  width: ${({ width }) => width};
  height: ${({ height }) => height};
  margin: 1.5em auto;
`;

const WriteToday = styled.div<BoxSizeProps>`
  display: flex;
  flex-direction: row;
  vertical-align: center;
  justify-content: space-around;
  width: ${({ width }) => width};
  height: ${({ height }) => height};
`;

const Today = styled.span`
  margin: auto 0;
  font-size: 24px;
  letter-spacing: 0.69px;
  color: #6b6c6f;
  font-family: "AppleSDGothicNeo-Medium";
`;

const TodayInput = styled.input`
  width: 87%;
  padding: 0 10px;
  font-size: 21px;
  height: max-height;
  border: 1px solid #686565;
  border-radius: 4px;
  opacity: 0.7;
`;

const PostButton = styled.button`
  margin: 2em 0.5em;
  width: 200px;
  height: 60px;
  font-size: 24px;
  letter-spacing: 0.69px;
  color: #f2f2f2;
  font-family: "AppleSDGothicNeo-Bold";
  background-color: #faa02a;
  border-radius: 30px;
  align-self: flex-end;
`;
