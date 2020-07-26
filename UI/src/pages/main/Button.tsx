import React from "react";
import styled from "styled-components";

interface ButtonProps {
  buttonName: "MORE" | "WRITE" | "CREATE";
  isEnable?: boolean;
  buttonText: string;
  onClick?: () => void;
}

interface ButtonLayoutProps {
  buttonName: string;
}

const Button: React.FunctionComponent<ButtonProps> = (props) => {
  const { buttonName, onClick, buttonText } = props;
  return (
    <ButtonArea>
      <ButtonLayout buttonName={buttonName} onClick={onClick}>
        {buttonText}
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
