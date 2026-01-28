import React from 'react';
import { Layout, Menu, theme } from 'antd';
import { useLocation, useNavigate } from 'react-router-dom';
import { useMenuStore } from '@/store/useMenuStore';
import { MENU_CONFIG } from '@/utils/constants';
import * as Icons from '@ant-design/icons';

const { Sider } = Layout;

const Sidebar: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { collapsed } = useMenuStore();
  const {
    token: { colorBgContainer },
  } = theme.useToken();

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

  const selectedKeys = findSelectedKey(location.pathname, MENU_CONFIG);

  return (
    <Sider
      trigger={null}
      collapsible
      collapsed={collapsed}
      style={{
        overflow: 'auto',
        height: '100vh',
        position: 'fixed',
        left: 0,
        top: 0,
        bottom: 0,
        background: colorBgContainer,
      }}
    >
      <div
        style={{
          height: 32,
          margin: 16,
          background: 'rgba(255, 255, 255, 0.2)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          fontWeight: 'bold',
          fontSize: collapsed ? 12 : 16,
        }}
      >
        {collapsed ? '量霸' : '量霸科技后台管理'}
      </div>
      <Menu
        theme="light"
        mode="inline"
        selectedKeys={selectedKeys}
        defaultOpenKeys={selectedKeys.slice(0, -1)}
        items={getMenuItems(MENU_CONFIG)}
        style={{ borderRight: 0 }}
      />
    </Sider>
  );
};

export default Sidebar;
