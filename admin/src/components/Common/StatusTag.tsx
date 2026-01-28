import React from 'react';
import { Tag } from 'antd';

interface StatusTagProps {
  status: boolean | string | number;
  trueText?: string;
  falseText?: string;
  trueColor?: string;
  falseColor?: string;
}

const StatusTag: React.FC<StatusTagProps> = ({
  status,
  trueText = '启用',
  falseText = '禁用',
  trueColor = 'green',
  falseColor = 'red',
}) => {
  const isActive = Boolean(status);

  return (
    <Tag color={isActive ? trueColor : falseColor}>
      {isActive ? trueText : falseText}
    </Tag>
  );
};

export default StatusTag;
