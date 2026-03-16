import React from "react";
import { Outlet } from "react-router-dom";
import { Grid, Layout as AntLayout } from "antd";
import Sidebar from "./Sidebar";
import Header from "./Header";

const { Content } = AntLayout;

const AdminLayout: React.FC = () => {
  const screens = Grid.useBreakpoint();
  const isMobile = !screens.lg;

  return (
    <AntLayout className="admin-shell">
      <Sidebar mobile={isMobile} />
      <AntLayout className="admin-main">
        <Header />
        <Content
          className="admin-content"
          style={{
            margin: isMobile ? "16px" : "24px",
          }}
        >
          <Outlet />
        </Content>
      </AntLayout>
    </AntLayout>
  );
};

export default AdminLayout;
