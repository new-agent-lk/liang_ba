import React, { useEffect, useState } from 'react';
import { Row, Col, Card, Statistic, Table, Typography, Spin } from 'antd';
import {
	UserOutlined,
	MessageOutlined,
} from '@ant-design/icons';
import { getDashboardStats } from '@/api/dashboard';
import { DashboardStats } from '@/types';
import LineChart from '@/components/Charts/LineChart';
import BarChart from '@/components/Charts/BarChart';

const { Title } = Typography;

const Dashboard: React.FC = () => {
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
			console.error('Failed to fetch dashboard stats:', error);
		} finally {
			setLoading(false);
		}
	};

	if (loading) {
		return (
			<div style={{ textAlign: 'center', padding: 100 }}>
				<Spin size="large" />
			</div>
		);
	}

	const statCards = [
		{
			title: '用户总数',
			value: stats?.total_users || 0,
			icon: <UserOutlined />,
			color: '#1890ff',
		},
		{
			title: '留言总数',
			value: stats?.total_messages || 0,
			icon: <MessageOutlined />,
			color: '#52c41a',
		},
	];

	// Mock chart data for demonstration
	const lineChartData = {
		xAxis: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
		series: [
			{
				name: '访问量',
				data: [120, 132, 101, 134, 90, 230, 210],
			},
		],
	};

	const barChartData = {
		xAxis: ['用户', '留言'],
		series: [
			{
				name: '数量',
				data: [
					stats?.total_users || 0,
					stats?.total_messages || 0,
				],
			},
		],
	};

	const recentActivityColumns = [
		{
			title: '活动类型',
			dataIndex: 'type',
			key: 'type',
			render: (type: string) => {
				const colors: Record<string, string> = {
					create: 'green',
					update: 'blue',
					delete: 'red',
					message: '#eb2f96',
				};
				return (
					<span style={{ color: colors[type] || '#666' }}>
						{type}
					</span>
				);
			},
		},
		{
			title: '内容',
			dataIndex: 'content',
			key: 'content',
			ellipsis: true,
		},
		{
			title: '时间',
			dataIndex: 'created_at',
			key: 'created_at',
		},
	];

	return (
		<div>
			<Title level={4} style={{ margin: 24 }}>
				仪表盘
			</Title>

			<Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
				{statCards.map((card, index) => (
					<Col xs={24} sm={12} md={8} key={index}>
						<Card bordered={false}>
							<Statistic
								title={card.title}
								value={card.value}
								prefix={React.cloneElement(card.icon, {
									style: { color: card.color },
								})}
								valueStyle={{ color: card.color }}
							/>
						</Card>
					</Col>
				))}
			</Row>

			<Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
				<Col xs={24} lg={12}>
					<Card title="访问趋势" bordered={false}>
						<LineChart data={lineChartData} height={300} />
					</Card>
				</Col>
				<Col xs={24} lg={12}>
					<Card title="数据统计" bordered={false}>
						<BarChart data={barChartData} height={300} />
					</Card>
				</Col>
			</Row>

			<Row gutter={[16, 16]}>
				<Col xs={24}>
					<Card title="最近活动" bordered={false}>
						<Table
							dataSource={stats?.recent_activities || []}
							columns={recentActivityColumns}
							rowKey="id"
							pagination={false}
							size="small"
						/>
					</Card>
				</Col>
			</Row>
		</div>
	);
};

export default Dashboard;
