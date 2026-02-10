import React from "react";
import { Outlet } from "react-router-dom";
import { Layout as AntLayout } from "antd";
import Sidebar from "./Sidebar";
import Header from "./Header";

const { Content } = AntLayout;

const AdminLayout: React.FC = () => {
  return (
    <AntLayout style={{ minHeight: "100vh" }}>
      <Sidebar />
      <AntLayout style={{ marginLeft: 0 }}>
        <Header />
        <Content
          style={{ margin: "24px", background: "#fff", borderRadius: 8 }}
        >
          <Outlet />
        </Content>
      </AntLayout>
    </AntLayout>
  );
};

export default AdminLayout;
