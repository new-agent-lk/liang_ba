import React from "react";
import { Drawer, Layout, Menu, theme } from "antd";
import { useLocation, useNavigate } from "react-router-dom";
import { useMenuStore } from "@/store/useMenuStore";
import { MENU_CONFIG } from "@/utils/constants";
import { filterMenuItems } from "@/utils/access";
import { useAuthStore } from "@/store/useAuthStore";
import * as Icons from "@ant-design/icons";

const { Sider } = Layout;

interface SidebarProps {
  mobile?: boolean;
}

const Sidebar: React.FC<SidebarProps> = ({ mobile = false }) => {
  const location = useLocation();
  const navigate = useNavigate();
  const { collapsed, mobileOpen, closeMobileMenu } = useMenuStore();
  const user = useAuthStore((state) => state.user);
  const {
    token: { colorBgContainer },
  } = theme.useToken();
  const visibleMenuConfig = filterMenuItems(MENU_CONFIG, user);

  const getIcon = (iconName: string) => {
    const IconComponent = (Icons as any)[iconName];
    return IconComponent ? <IconComponent /> : null;
  };

  const getMenuItems = (items: any[]): any[] => {
    return items.map((item) => ({
      key: item.key,
      icon: item.icon ? getIcon(item.icon) : null,
      label: item.label,
      children: item.children ? getMenuItems(item.children) : undefined,
      onClick: () => !item.children && navigate(item.key),
    }));
  };

  // Find the selected key based on current path
  const findSelectedKey = (path: string, items: any[]): string[] => {
    for (const item of items) {
      if (item.key === path) {
        return [item.key];
      }
      if (item.children) {
        const found = findSelectedKey(path, item.children);
        if (found.length > 0) {
          return [item.key, ...found];
        }
      }
    }
    return [];
  };

  const selectedKeys = findSelectedKey(location.pathname, visibleMenuConfig);
  const openKeys = selectedKeys.slice(0, -1);

  const menuContent = (
    <>
      <div
        className={`admin-sidebar-brand ${collapsed && !mobile ? "is-collapsed" : ""}`}
      >
        <div className="admin-sidebar-brand__mark">LB</div>
        {(!collapsed || mobile) && (
          <div className="admin-sidebar-brand__text">
            <strong>量霸科技</strong>
            <span>Enterprise Console</span>
          </div>
        )}
      </div>
      <Menu
        theme="light"
        mode="inline"
        selectedKeys={selectedKeys}
        defaultOpenKeys={openKeys}
        items={getMenuItems(visibleMenuConfig)}
        style={{ borderRight: 0, background: "transparent" }}
        onClick={() => {
          if (mobile) {
            closeMobileMenu();
          }
        }}
      />
    </>
  );

  if (mobile) {
    return (
      <Drawer
        placement="left"
        open={mobileOpen}
        onClose={closeMobileMenu}
        bodyStyle={{ padding: 12, background: "#f4f7fb" }}
        width={280}
        closable={false}
      >
        {menuContent}
      </Drawer>
    );
  }

  return (
    <Sider
      trigger={null}
      collapsible
      collapsed={collapsed}
      width={248}
      className="admin-sidebar"
      style={{ background: colorBgContainer }}
    >
      {menuContent}
    </Sider>
  );
};

export default Sidebar;
