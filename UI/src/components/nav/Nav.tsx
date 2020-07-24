import React from "react";
import styled from "styled-components";

import { MenuOutlined } from "@ant-design/icons";

interface HeightProps {
  readonly height: string;
}

const Nav: React.FC = () => {
  const height = "120px";

  return (
    <>
      <NavWrapper height={height}>
        <MenuOutlined
          style={{
            position: "absolute",
            top: "38px",
            left: "60px",
            fontSize: "42px",
          }}
        />
        <Title height={height}>소근</Title>
      </NavWrapper>
    </>
  );
};

export default Nav;

const NavWrapper = styled.div<HeightProps>`
  height: ${({ height }) => height};
  text-align: center;
  background-color: #ffffff;
`;

const Title = styled.span<HeightProps>`
  line-height: ${({ height }) => height};
  font-family: "AppleSDGothicNeo-SemiBold";
  font-size: 24px;
  text-align: center;
  letter-spacing: 0;
`;

const MenuButton = styled.div``;
