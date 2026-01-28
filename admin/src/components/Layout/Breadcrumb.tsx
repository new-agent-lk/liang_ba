import React from 'react';
import { Breadcrumb as AntBreadcrumb, ConfigProvider } from 'antd';
import { useLocation, Link } from 'react-router-dom';
import { MENU_CONFIG } from '@/utils/constants';

const Breadcrumb: React.FC = () => {
  const location = useLocation();

  const findBreadcrumbs = (path: string, items: any[], current: string[] = []): string[] => {
    for (const item of items) {
      if (item.key === path) {
        return [...current, item.label];
      }
      if (item.children) {
        const found = findBreadcrumbs(path, item.children, [...current, item.label]);
        if (found.length > 0) {
          return found;
        }
      }
    }
    return [];
  };

  const breadcrumbs = findBreadcrumbs(location.pathname, MENU_CONFIG);

  return (
    <ConfigProvider
      theme={{
        components: {
          Breadcrumb: {
            itemColor: '#666',
            lastItemColor: '#333',
            separatorColor: '#ccc',
          },
        },
      }}
    >
      <AntBreadcrumb
        style={{ margin: '16px 0' }}
        items={breadcrumbs.map((label, index) => ({
          title:
            index === breadcrumbs.length - 1 ? (
              label
            ) : (
              <Link to={MENU_CONFIG.find((item) => item.label === breadcrumbs[index])?.key || '#'}>
                {label}
              </Link>
            ),
        }))}
      />
    </ConfigProvider>
  );
};

export default Breadcrumb;
