import React from "react";
import { Form, Input, Button, Select, DatePicker, Space } from "antd";
import { SearchOutlined, ReloadOutlined } from "@ant-design/icons";

const { RangePicker } = DatePicker;

interface SearchFormProps {
  form: any;
  onSearch: (values: any) => void;
  onReset: () => void;
  fields: SearchField[];
}

interface SearchField {
  name: string;
  label: string;
  type: "input" | "select" | "dateRange";
  placeholder?: string;
  options?: { label: string; value: any }[];
}

const SearchForm: React.FC<SearchFormProps> = ({
  form,
  onSearch,
  onReset,
  fields,
}) => {
  const handleFinish = (values: any) => {
    onSearch(values);
  };

  const handleReset = () => {
    form.resetFields();
    onReset();
  };

  const renderField = (field: SearchField) => {
    switch (field.type) {
      case "input":
        return (
          <Form.Item
            key={field.name as string}
            name={field.name}
            label={field.label}
          >
            <Input placeholder={field.placeholder} allowClear />
          </Form.Item>
        );
      case "select":
        return (
          <Form.Item
            key={field.name as string}
            name={field.name}
            label={field.label}
          >
            <Select
              placeholder={field.placeholder}
              allowClear
              options={field.options}
              style={{ width: 150 }}
            />
          </Form.Item>
        );
      case "dateRange":
        return (
          <Form.Item
            key={field.name as string}
            name={field.name}
            label={field.label}
          >
            <RangePicker />
          </Form.Item>
        );
      default:
        return null;
    }
  };

  return (
    <Form form={form} layout="inline" onFinish={handleFinish}>
      {fields.map(renderField)}
      <Form.Item>
        <Space>
          <Button type="primary" htmlType="submit" icon={<SearchOutlined />}>
            搜索
          </Button>
          <Button onClick={handleReset} icon={<ReloadOutlined />}>
            重置
          </Button>
        </Space>
      </Form.Item>
    </Form>
  );
};

export default SearchForm;
