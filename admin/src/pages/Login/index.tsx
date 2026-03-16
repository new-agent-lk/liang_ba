import React, { useState } from "react";
import {
  Form,
  Input,
  Button,
  Card,
  Typography,
  message,
  Space,
  Tag,
} from "antd";
import {
  UserOutlined,
  LockOutlined,
  SafetyCertificateOutlined,
  StockOutlined,
  ReadOutlined,
} from "@ant-design/icons";
import { useNavigate } from "react-router-dom";
import { useAuth } from "@/hooks/useAuth";

const { Title, Text, Paragraph } = Typography;

const Login: React.FC = () => {
  const navigate = useNavigate();
  const { login } = useAuth();
  const [loading, setLoading] = useState(false);

  const onFinish = async (values: { username: string; password: string }) => {
    setLoading(true);
    try {
      const result = await login(values);
      if (result.success) {
        navigate("/dashboard");
      } else {
        message.error("用户名或密码错误");
      }
    } catch (error) {
      message.error("登录失败，请稍后重试");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-page__glow login-page__glow--left" />
      <div className="login-page__glow login-page__glow--right" />
      <div className="login-shell">
        <section className="login-brand">
          <Tag className="login-brand__tag" bordered={false}>
            Liang Ba Enterprise Console
          </Tag>
          <Title level={1} className="login-brand__title">
            统一管理内容、招聘与量化研究流程
          </Title>
          <Paragraph className="login-brand__desc">
            登录后进入企业控制台，集中处理后台账号、内容发布、研究报告与 FactorHub 分析任务。桌面端强调信息层次，移动端保留精简入口和核心说明。
          </Paragraph>
          <div className="login-brand__feature-list">
            <div className="login-brand__feature">
              <SafetyCertificateOutlined />
              <div>
                <strong>权限与账号控制</strong>
                <span>统一管理后台用户、角色与审计入口</span>
              </div>
            </div>
            <div className="login-brand__feature">
              <ReadOutlined />
              <div>
                <strong>研究报告管理</strong>
                <span>跟踪策略输出、回测结果与内容发布</span>
              </div>
            </div>
            <div className="login-brand__feature">
              <StockOutlined />
              <div>
                <strong>量化分析平台</strong>
                <span>连接因子分析、数据获取与策略验证</span>
              </div>
            </div>
          </div>
        </section>

        <Card bordered={false} className="login-card">
          <div className="login-card__header">
            <div className="login-card__badge">LB</div>
            <div>
              <Text className="login-card__eyebrow">Welcome Back</Text>
              <Title level={3}>登录后台管理系统</Title>
              <Text type="secondary">请输入账户信息以继续访问控制台</Text>
            </div>
          </div>
          <Form
            name="login"
            initialValues={{ username: "", password: "" }}
            onFinish={onFinish}
            size="large"
            layout="vertical"
            className="login-form"
          >
            <Form.Item
              name="username"
              label="用户名"
              rules={[
                { required: true, message: "请输入用户名" },
                { min: 3, message: "用户名至少3个字符" },
              ]}
            >
              <Input
                prefix={<UserOutlined />}
                placeholder="请输入用户名"
                allowClear
              />
            </Form.Item>
            <Form.Item
              name="password"
              label="密码"
              rules={[
                { required: true, message: "请输入密码" },
                { min: 6, message: "密码至少6个字符" },
              ]}
            >
              <Input.Password prefix={<LockOutlined />} placeholder="请输入密码" />
            </Form.Item>
            <Form.Item>
              <Button
                type="primary"
                htmlType="submit"
                loading={loading}
                className="login-form__submit"
              >
                登录
              </Button>
            </Form.Item>
          </Form>
          <Space split={<span className="login-card__dot" />} className="login-card__footer">
            <Text type="secondary">JWT 鉴权</Text>
            <Text type="secondary">企业控制台</Text>
            <Text type="secondary">移动端已适配</Text>
          </Space>
        </Card>
      </div>
    </div>
  );
};

export default Login;
