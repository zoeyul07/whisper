import React, { useState } from "react";
import styled, { css } from "styled-components";

function UserInput() {
  const [userInput, setUserInput] = useState("");
  const [textAlign, setTextAlign] = useState("left");

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
        onChange={(e: <typeof e>) => setUserInput(e.target.value)}
        textAlign={textAlign}
      />
      {console.log(userInput)}
      {console.log(textAlign)}
    </UserInputWrapper>
  );
}

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
`;

const ButtonGroup = styled.div`
  display: flex;
  margin: 0 16px;
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
  /* text-align: left; */

  text-align: ${(props: string) => props.textAlign};

  ::placeholder {
    font-size: 20px;
  }
`;
