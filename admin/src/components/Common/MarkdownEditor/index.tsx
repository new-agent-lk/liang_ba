import React from 'react';
import MDSelect from '@uiw/react-md-editor';
import { Form } from 'antd';

interface MarkdownEditorProps {
  value?: string;
  onChange?: (value: string | undefined) => void;
  height?: number;
  placeholder?: string;
}

// 独立的 MarkdownEditor 组件
const MarkdownEditor: React.FC<MarkdownEditorProps> = ({
  value,
  onChange,
  height = 400,
  placeholder = '请输入 Markdown 内容...',
}) => {
  return (
    <div data-color-mode="light">
      <MDSelect
        value={value}
        onChange={onChange}
        height={height}
        placeholder={placeholder}
        preview="edit"
        hideToolbar={false}
        tabIndex={-1}
        previewOptions={{
          style: {
            padding: '16px',
            backgroundColor: '#fff',
            border: '1px solid #d9d9d9',
            borderRadius: '8px',
            marginTop: '8px',
          },
        }}
      />
    </div>
  );
};

// Form.Item 包装的 MarkdownEditor
interface MarkdownFormItemProps {
  name?: string;
  label?: string;
  required?: boolean;
  height?: number;
  placeholder?: string;
}

const MarkdownFormItem: React.FC<MarkdownFormItemProps> = ({
  name,
  label,
  required,
  height = 400,
  placeholder,
}) => {
  return (
    <Form.Item
      name={name}
      label={label}
      valuePropName="value"
      getValueFromEvent={(value: string | undefined) => value || ''}
      rules={required ? [{ required: true, message: `请输入${label}` }] : []}
    >
      <MarkdownEditor height={height} placeholder={placeholder} />
    </Form.Item>
  );
};

export { MarkdownEditor, MarkdownFormItem };
export default MarkdownEditor;
