import React, { useState } from 'react';
import { Card, Form, Input, Button, Switch, message, Tabs } from 'antd';

const Settings: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);

  const handleSubmit = async () => {
    setLoading(true);
    try {
      // Save settings API call
      message.success('设置保存成功');
    } catch (error) {
      message.error('保存失败');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <Card title="系统设置" bordered={false}>
        <Tabs
          items={[
            {
              key: 'general',
              label: '常规设置',
              children: (
                <Form
                  form={form}
                  layout="vertical"
                  onFinish={handleSubmit}
                  style={{ maxWidth: 600 }}
                >
                  <Form.Item
                    name="site_name"
                    label="网站名称"
                    initialValue="量霸科技"
                  >
                    <Input placeholder="请输入网站名称" />
                  </Form.Item>
                  <Form.Item
                    name="site_description"
                    label="网站描述"
                  >
                    <Input.TextArea rows={3} placeholder="请输入网站描述" />
                  </Form.Item>
                  <Form.Item
                    name="contact_email"
                    label="联系邮箱"
                    initialValue="contact@liangba.com"
                  >
                    <Input placeholder="请输入联系邮箱" />
                  </Form.Item>
                  <Form.Item
                    name="contact_phone"
                    label="联系电话"
                  >
                    <Input placeholder="请输入联系电话" />
                  </Form.Item>
                  <Form.Item>
                    <Button type="primary" htmlType="submit" loading={loading}>
                      保存设置
                    </Button>
                  </Form.Item>
                </Form>
              ),
            },
            {
              key: 'seo',
              label: 'SEO 设置',
              children: (
                <Form
                  form={form}
                  layout="vertical"
                  onFinish={handleSubmit}
                  style={{ maxWidth: 600 }}
                >
                  <Form.Item name="meta_keywords" label="关键词">
                    <Input.TextArea rows={3} placeholder="请输入关键词，用逗号分隔" />
                  </Form.Item>
                  <Form.Item name="meta_description" label="描述">
                    <Input.TextArea rows={3} placeholder="请输入页面描述" />
                  </Form.Item>
                  <Form.Item>
                    <Button type="primary" htmlType="submit" loading={loading}>
                      保存设置
                    </Button>
                  </Form.Item>
                </Form>
              ),
            },
            {
              key: 'security',
              label: '安全设置',
              children: (
                <Form
                  form={form}
                  layout="vertical"
                  onFinish={handleSubmit}
                  style={{ maxWidth: 600 }}
                >
                  <Form.Item name="login_captcha" label="登录验证码" valuePropName="checked">
                    <Switch checkedChildren="启用" unCheckedChildren="禁用" />
                  </Form.Item>
                  <Form.Item name="login_limit" label="登录失败锁定" valuePropName="checked">
                    <Switch checkedChildren="启用" unCheckedChildren="禁用" />
                  </Form.Item>
                  <Form.Item name="session_timeout" label="会话超时(分钟)">
                    <Input type="number" placeholder="请输入会话超时时间" />
                  </Form.Item>
                  <Form.Item>
                    <Button type="primary" htmlType="submit" loading={loading}>
                      保存设置
                    </Button>
                  </Form.Item>
                </Form>
              ),
            },
          ]}
        />
      </Card>
    </div>
  );
};

export default Settings;
