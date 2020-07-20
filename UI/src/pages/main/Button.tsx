import React from "react";
import styled from "styled-components";

interface Buttonprops {
  buttonName: "MORE" | "WRITE" | "CREATE";
  isEnable?: boolean;
  buttonText: string;
  onClick?: () => void;
}

interface ButtonLayoutProps {
  buttonName: string;
}

const Button: React.FunctionComponent<Buttonprops> = (props) => {
  return (
    <ButtonArea>
      <ButtonLayout buttonName={props.buttonName} onClick={props.onClick}>
        {props.buttonText}
      </ButtonLayout>
    </ButtonArea>
  );
};

const ButtonArea = styled.div`
  display: flex;
  justify-content: flex-end;
`;

const ButtonLayout = styled.button<ButtonLayoutProps>`
  width: 90px;
  height: 36px;
  border-radius: 20px;
  margin-bottom: 20px;
  background-color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 1px solid #686565;
  font-size: 12px;
  color: #252529;
  opacity: 0.7;
`;

export default Button;
