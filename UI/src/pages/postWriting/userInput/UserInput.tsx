import React, { useState } from "react";
import styled, { css } from "styled-components";

interface InputProps {
  textAlign: string;
}

interface SizeProps {
  width: string;
  height: string;
}

const UserInput: React.FC = () => {
  const [userInput, setUserInput] = useState("");
  const [textAlign, setTextAlign] = useState("left");

  const width = "97%";

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setUserInput(e.target.value);
  };

  return (
    <UserInputWrapper>
      <ControlBar>
        <ButtonGroup>
          <ButtonBold />
          <ButtonItalic />
          <ButtonUnderline />
        </ButtonGroup>
        <ButtonGroup>
          <ButtonAlignLeft onClick={() => setTextAlign("left")} />
          <ButtonAlignCenter onClick={() => setTextAlign("center")} />
          <ButtonAlignRight onClick={() => setTextAlign("right")} />
        </ButtonGroup>
      </ControlBar>

      <InputBox
        placeholder="당신의 이야기를 적어보세요..."
        value={userInput}
        onChange={(e) => handleInputChange(e)}
        textAlign={textAlign}
      />
      <WriteToday width="97%" height="50px">
        <Today>오늘의 한 줄</Today>
        <TodayInput />
      </WriteToday>
      {console.log(userInput)}
      {console.log(textAlign)}
    </UserInputWrapper>
  );
};

export default UserInput;

const UserInputWrapper = styled.div`
  margin: 5em auto;
  width: 1323px;
  height: 851px;
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

const InputBox = styled.textarea`
  width: 97%;
  height: 780px;
  margin: 1.5em 1em;
  padding: 1.8em 2em;
  border: 1px solid #828282;
  resize: none;
  font-size: 20px;
  text-align: ${(props: InputProps) => props.textAlign};

  ::placeholder {
    font-size: 20px;
  }
`;

const WriteToday = styled.div<SizeProps>`
  display: flex;
  vertical-align: center;
  justify-content: space-around;
  width: ${({ width }) => width};
  height: ${({ height }) => height};
  margin: 1.5em auto;
`;

const Today = styled.span`
  margin: auto 0;
  font-size: 24px;
  letter-spacing: 0.69px;
  color: #6b6c6f;
  font-family: "AppleSDGothicNeo-Medium";
`;

const TodayInput = styled.input`
  width: 83%;
  height: max-height;
  border: 1px solid #686565;
  border-radius: 4px;
  opacity: 0.7;
`;
