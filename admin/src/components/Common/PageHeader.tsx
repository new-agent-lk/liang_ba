import React, { ReactNode } from 'react';
import { Card, Typography, Button } from 'antd';
import { PlusOutlined } from '@ant-design/icons';

const { Title } = Typography;

interface PageHeaderProps {
  title: string;
  description?: string;
  showAddButton?: boolean;
  addButtonText?: string;
  onAdd?: () => void;
  actions?: ReactNode[];
}

const PageHeader: React.FC<PageHeaderProps> = ({
  title,
  description,
  showAddButton,
  addButtonText = '新增',
  onAdd,
  actions,
}) => {
  const handleAdd = () => {
    if (onAdd) {
      onAdd();
    }
  };

  return (
    <Card bordered={false} style={{ marginBottom: 16 }}>
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
        }}
      >
        <div>
          <Title level={4} style={{ margin: 0 }}>
            {title}
          </Title>
          {description && (
            <Typography.Text type="secondary">{description}</Typography.Text>
          )}
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          {actions}
          {showAddButton && (
            <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
              {addButtonText}
            </Button>
          )}
        </div>
      </div>
    </Card>
  );
};

export default PageHeader;
