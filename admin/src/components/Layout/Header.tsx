import React from "react";
import { Layout, Dropdown, Avatar, Button, Grid, theme } from "antd";
import {
  UserOutlined,
  LogoutOutlined,
  MenuFoldOutlined,
  MenuUnfoldOutlined,
} from "@ant-design/icons";
import { useNavigate } from "react-router-dom";
import { useAuthStore } from "@/store/useAuthStore";
import { useMenuStore } from "@/store/useMenuStore";

const { Header: AntHeader } = Layout;

const Header: React.FC = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();
  const { collapsed, toggleCollapsed, openMobileMenu } = useMenuStore();
  const screens = Grid.useBreakpoint();
  const isMobile = !screens.lg;
  const {
    token: { colorBgContainer },
  } = theme.useToken();

  const handleMenuClick = ({ key }: { key: string }) => {
    if (key === "logout") {
      logout();
    } else if (key === "profile") {
      navigate("/system/profile");
    }
  };

  const menuItems = [
    {
      key: "profile",
      icon: <UserOutlined />,
      label: "个人中心",
    },
    {
      key: "logout",
      icon: <LogoutOutlined />,
      label: "退出登录",
    },
  ];

  return (
    <AntHeader
      className="admin-header"
      style={{ background: colorBgContainer }}
    >
      <div className="admin-header__left">
        <Button
          type="text"
          icon={
            isMobile
              ? <MenuUnfoldOutlined />
              : collapsed
                ? <MenuUnfoldOutlined />
                : <MenuFoldOutlined />
          }
          onClick={isMobile ? openMobileMenu : toggleCollapsed}
          style={{ fontSize: 16 }}
        />
        <div className="admin-header__title">
          <strong>{isMobile ? "量霸控制台" : "量霸科技后台管理"}</strong>
          <span>{isMobile ? "移动端视图" : "企业运营与研究管理平台"}</span>
        </div>
      </div>
      <Dropdown menu={{ items: menuItems, onClick: handleMenuClick }}>
        <div className="admin-header__user">
          <Avatar
            icon={<UserOutlined />}
            style={{ backgroundColor: "#1890ff" }}
          />
          {!isMobile && <span>{user?.username || "管理员"}</span>}
        </div>
      </Dropdown>
    </AntHeader>
  );
};

export default Header;
