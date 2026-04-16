import React, { useEffect, useState } from "react";
import {
  Row,
  Col,
  Card,
  Statistic,
  Table,
  Typography,
  Spin,
  Button,
  Space,
  Tag,
} from "antd";
import {
  UserOutlined,
  TeamOutlined,
  FileSearchOutlined,
  ArrowUpOutlined,
  RiseOutlined,
  ReadOutlined,
  RocketOutlined,
  SafetyCertificateOutlined,
} from "@ant-design/icons";
import { useNavigate } from "react-router-dom";
import { getDashboardStats } from "@/api/dashboard";
import { DashboardStats } from "@/types";
import LineChart from "@/components/Charts/LineChart";
import BarChart from "@/components/Charts/BarChart";

const { Title, Paragraph, Text } = Typography;

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const [loading, setLoading] = useState(true);
  const [stats, setStats] = useState<DashboardStats | null>(null);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const data = await getDashboardStats();
      setStats(data);
    } catch (error) {
      console.error("Failed to fetch dashboard stats:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div style={{ textAlign: "center", padding: 100 }}>
        <Spin size="large" />
      </div>
    );
  }

  const statCards = [
    {
      title: "用户总数",
      value: stats?.total_users || 0,
      icon: <UserOutlined />,
      accent: "var(--dashboard-accent-blue)",
      hint: "活跃账号与管理角色",
    },
    {
      title: "职位总数",
      value: stats?.total_jobs || 0,
      icon: <TeamOutlined />,
      accent: "var(--dashboard-accent-green)",
      hint: "招聘需求与岗位池",
    },
    {
      title: "简历总数",
      value: stats?.total_resumes || 0,
      icon: <FileSearchOutlined />,
      accent: "var(--dashboard-accent-orange)",
      hint: "投递与筛选记录",
    },
  ];

  const lineChartData = {
    xAxis: ["周一", "周二", "周三", "周四", "周五", "周六", "周日"],
    series: [
      {
        name: "活跃访问",
        data: [168, 192, 185, 224, 208, 260, 248],
      },
      {
        name: "任务处理",
        data: [96, 110, 124, 138, 132, 176, 168],
      },
    ],
  };

  const barChartData = {
    xAxis: ["用户", "职位", "简历"],
    series: [
      {
        name: "业务量",
        data: [
          stats?.total_users || 0,
          stats?.total_jobs || 0,
          stats?.total_resumes || 0,
        ],
      },
    ],
  };

  const recentActivityColumns = [
    {
      title: "活动类型",
      dataIndex: "type",
      key: "type",
      render: (type: string) => {
        const colors: Record<string, string> = {
          create: "green",
          update: "blue",
          delete: "red",
        };
        const labels: Record<string, string> = {
          create: "新增",
          update: "更新",
          delete: "删除",
        };
        return (
          <Tag color={colors[type] || "default"}>{labels[type] || type}</Tag>
        );
      },
    },
    {
      title: "内容",
      dataIndex: "content",
      key: "content",
      ellipsis: true,
    },
    {
      title: "时间",
      dataIndex: "created_at",
      key: "created_at",
    },
  ];

  const quickActions = [
    {
      title: "用户管理",
      description: "维护后台账号、权限与组织信息",
      icon: <SafetyCertificateOutlined />,
      path: "/system/users",
    },
    {
      title: "研究报告",
      description: "查看回测结论与策略产出",
      icon: <ReadOutlined />,
      path: "/research/reports/manage",
    },
    {
      title: "量化因子",
      description: "进入因子分析与策略回测中心",
      icon: <RocketOutlined />,
      path: "/factor-hub",
    },
  ];

  return (
    <div className="dashboard-page">
      <section className="dashboard-hero">
        <div>
          <Tag className="dashboard-hero__tag" bordered={false}>
            Enterprise Admin Home
          </Tag>
          <Title level={2} className="dashboard-hero__title">
            企业内容、招聘与研究平台一屏总览
          </Title>
          <Paragraph className="dashboard-hero__desc">
            首页整合账户、招聘与研究进展，减少进入后台后的空白感。移动端下保留核心指标和快捷入口，优先保证可读性与操作路径。
          </Paragraph>
          <Space wrap>
            <Button
              type="primary"
              size="large"
              onClick={() => navigate("/factor-hub")}
            >
              进入量化因子中心
            </Button>
            <Button
              size="large"
              onClick={() => navigate("/research/reports/write")}
            >
              去做撰写
            </Button>
          </Space>
        </div>
        <div className="dashboard-hero__panel">
          <div className="dashboard-hero__metric">
            <span>本周处理任务</span>
            <strong>
              {(stats?.total_jobs || 0) + (stats?.total_resumes || 0)}
            </strong>
          </div>
          <div className="dashboard-hero__metric">
            <span>系统活跃模块</span>
            <strong>4</strong>
          </div>
          <div className="dashboard-hero__signal">
            <ArrowUpOutlined />
            <span>后台活跃度较上周提升 12%</span>
          </div>
        </div>
      </section>

      <Row gutter={[16, 16]} className="dashboard-stats">
        {statCards.map((card, index) => (
          <Col xs={24} sm={12} md={8} key={index}>
            <Card bordered={false} className="dashboard-stat-card">
              <Statistic
                title={card.title}
                value={card.value}
                prefix={React.cloneElement(card.icon, {
                  style: { color: card.accent },
                })}
                valueStyle={{ color: card.accent }}
              />
              <Text type="secondary">{card.hint}</Text>
            </Card>
          </Col>
        ))}
      </Row>

      <Row gutter={[16, 16]} className="dashboard-grid-row">
        <Col xs={24} xl={16}>
          <Card
            bordered={false}
            className="dashboard-surface dashboard-surface--highlight"
          >
            <div className="dashboard-section-head">
              <div>
                <Text className="dashboard-section-kicker">运营趋势</Text>
                <Title level={4}>近 7 日后台活跃变化</Title>
              </div>
              <Tag color="blue" icon={<RiseOutlined />}>
                实时概览
              </Tag>
            </div>
            <LineChart data={lineChartData} height={320} />
          </Card>
        </Col>
        <Col xs={24} xl={8}>
          <Card
            bordered={false}
            className="dashboard-surface dashboard-surface--warm"
          >
            <div className="dashboard-section-head">
              <div>
                <Text className="dashboard-section-kicker">结构分布</Text>
                <Title level={4}>当前业务量组成</Title>
              </div>
            </div>
            <BarChart data={barChartData} height={320} />
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]} className="dashboard-grid-row">
        <Col xs={24} lg={12}>
          <Card bordered={false} className="dashboard-surface">
            <div className="dashboard-section-head">
              <div>
                <Text className="dashboard-section-kicker">快捷入口</Text>
                <Title level={4}>常用管理动作</Title>
              </div>
            </div>
            <div className="dashboard-quick-actions">
              {quickActions.map((action) => (
                <button
                  key={action.title}
                  type="button"
                  className="dashboard-action-card"
                  onClick={() => navigate(action.path)}
                >
                  <span className="dashboard-action-card__icon">
                    {action.icon}
                  </span>
                  <strong>{action.title}</strong>
                  <span>{action.description}</span>
                </button>
              ))}
            </div>
          </Card>
        </Col>
        <Col xs={24} lg={12}>
          <Card bordered={false} className="dashboard-surface">
            <div className="dashboard-section-head">
              <div>
                <Text className="dashboard-section-kicker">执行摘要</Text>
                <Title level={4}>今日后台状态</Title>
              </div>
            </div>
            <div className="dashboard-summary-list">
              <div>
                <strong>{stats?.recent_activities?.length || 0}</strong>
                <span>最近活动记录</span>
              </div>
              <div>
                <strong>{stats?.total_jobs || 0}</strong>
                <span>招聘任务待跟进</span>
              </div>
              <div>
                <strong>{stats?.total_resumes || 0}</strong>
                <span>候选简历沉淀</span>
              </div>
            </div>
          </Card>
        </Col>
      </Row>

      <Row gutter={[16, 16]}>
        <Col xs={24}>
          <Card bordered={false} className="dashboard-surface">
            <div className="dashboard-section-head">
              <div>
                <Text className="dashboard-section-kicker">活动日志</Text>
                <Title level={4}>最近活动</Title>
              </div>
            </div>
            <Table
              dataSource={stats?.recent_activities || []}
              columns={recentActivityColumns}
              rowKey="id"
              pagination={false}
              size="small"
              scroll={{ x: 720 }}
            />
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard;
