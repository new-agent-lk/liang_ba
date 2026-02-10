import React from "react";
import {
  Card,
  Row,
  Col,
  Statistic,
  List,
  Tag,
  Typography,
  Space,
  Divider,
} from "antd";
import {
  BarChartOutlined,
  LineChartOutlined,
  ThunderboltOutlined,
  SettingOutlined,
  DatabaseOutlined,
  CheckCircleOutlined,
  ClockCircleOutlined,
} from "@ant-design/icons";
import { useNavigate } from "react-router-dom";

const { Title, Text } = Typography;

const FactorHubIndex: React.FC = () => {
  const navigate = useNavigate();
  const stats = {
    totalFactors: 25,
    computedToday: 156,
    activeModels: 8,
    backtestRuns: 24,
  };

  const features = [
    {
      icon: <DatabaseOutlined style={{ fontSize: 32, color: "#1890ff" }} />,
      title: "数据管理",
      description: "集成AKShare获取A股市场数据，支持股票池选择、日期范围配置",
      route: "/factor-hub/data",
      color: "#1890ff",
    },
    {
      icon: <SettingOutlined style={{ fontSize: 32, color: "#52c41a" }} />,
      title: "因子管理",
      description: "内置25+技术指标因子，支持自定义因子编写和批量计算",
      route: "/factor-hub/factors",
      color: "#52c41a",
    },
    {
      icon: <LineChartOutlined style={{ fontSize: 32, color: "#722ed1" }} />,
      title: "因子分析",
      description: "IC/IR分析、分层回测、相关性矩阵等专业分析工具",
      route: "/factor-hub/analysis",
      color: "#722ed1",
    },
    {
      icon: <BarChartOutlined style={{ fontSize: 32, color: "#fa8c16" }} />,
      title: "策略回测",
      description: "事件驱动回测引擎，支持多种策略和绩效指标评估",
      route: "/factor-hub/backtest",
      color: "#fa8c16",
    },
    {
      icon: <ThunderboltOutlined style={{ fontSize: 32, color: "#eb2f96" }} />,
      title: "因子挖掘",
      description: "遗传算法挖掘新因子，机器学习辅助因子合成",
      route: "/factor-hub/mining",
      color: "#eb2f96",
    },
  ];

  const recentActivity = [
    { action: "MA20因子计算完成", time: "2分钟前", status: "success" },
    { action: "沪深300数据更新", time: "15分钟前", status: "success" },
    { action: "动量因子回测完成", time: "30分钟前", status: "success" },
    { action: "新因子RSI已添加", time: "1小时前", status: "info" },
  ];

  return (
    <div style={{ padding: 24 }}>
      <div style={{ marginBottom: 24 }}>
        <Title level={2} style={{ margin: 0 }}>
          量化因子分析平台
        </Title>
        <Text type="secondary">基于FactorHub的量化投资研究工具</Text>
      </div>

      {/* 统计卡片 */}
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="可用因子"
              value={stats.totalFactors}
              prefix={<SettingOutlined />}
              suffix="个"
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="今日计算"
              value={stats.computedToday}
              prefix={<DatabaseOutlined />}
              suffix="次"
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="活跃模型"
              value={stats.activeModels}
              prefix={<ThunderboltOutlined />}
              suffix="个"
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="回测次数"
              value={stats.backtestRuns}
              prefix={<BarChartOutlined />}
              suffix="次"
            />
          </Card>
        </Col>
      </Row>

      {/* 功能模块 */}
      <Title level={4} style={{ marginBottom: 16 }}>
        功能模块
      </Title>
      <Row gutter={[16, 16]}>
        {features.map((feature, index) => (
          <Col span={8} key={index}>
            <Card
              hoverable
              onClick={() => navigate(feature.route)}
              style={{ height: "100%" }}
            >
              <Space
                direction="vertical"
                size="small"
                style={{ width: "100%" }}
              >
                {feature.icon}
                <Title level={5} style={{ margin: 0 }}>
                  {feature.title}
                </Title>
                <Text type="secondary">{feature.description}</Text>
              </Space>
            </Card>
          </Col>
        ))}
      </Row>

      <Divider />

      {/* 最近活动 */}
      <Row gutter={24}>
        <Col span={12}>
          <Title level={4}>快速开始</Title>
          <Card size="small">
            <List
              size="small"
              dataSource={[
                "1. 进入「数据管理」获取股票数据",
                "2. 在「因子管理」选择要计算的因子",
                "3. 使用「因子分析」评估因子有效性",
                "4. 通过「策略回测」验证投资策略",
              ]}
              renderItem={(item, index) => (
                <List.Item>
                  <Space>
                    <Tag color="blue">{index + 1}</Tag>
                    <Text>{item}</Text>
                  </Space>
                </List.Item>
              )}
            />
          </Card>
        </Col>
        <Col span={12}>
          <Title level={4}>最近活动</Title>
          <Card size="small">
            <List
              size="small"
              dataSource={recentActivity}
              renderItem={(item) => (
                <List.Item>
                  <Space>
                    {item.status === "success" ? (
                      <CheckCircleOutlined style={{ color: "#52c41a" }} />
                    ) : (
                      <ClockCircleOutlined style={{ color: "#1890ff" }} />
                    )}
                    <Text>{item.action}</Text>
                    <Text type="secondary" style={{ fontSize: 12 }}>
                      {item.time}
                    </Text>
                  </Space>
                </List.Item>
              )}
            />
          </Card>
        </Col>
      </Row>

      <Divider />

      {/* 因子类型 */}
      <Title level={4}>支持的因子类型</Title>
      <Space wrap>
        <Tag color="blue">技术指标</Tag>
        <Tag color="green">动量因子</Tag>
        <Tag color="orange">波动率</Tag>
        <Tag color="purple">成交量</Tag>
        <Tag color="red">估值因子</Tag>
        <Tag color="cyan">基本面</Tag>
        <Tag color="gold">情绪因子</Tag>
      </Space>
    </div>
  );
};

export default FactorHubIndex;
