import React, { useState, useEffect } from 'react';
import { Card, Row, Col, Select, Tag, Table, Button, Space, Typography, Descriptions, Modal, Input, message } from 'antd';
import { SettingOutlined, PlusOutlined, CalculatorOutlined } from '@ant-design/icons';
import { getFactorList } from '@/api/factorhub';

const { Option } = Select;
const { Text } = Typography;

const FactorListPage: React.FC = () => {
  const [factors, setFactors] = useState<any[]>([]);
  const [categories, setCategories] = useState<string[]>([]);
  const [selectedCategory, setSelectedCategory] = useState<string>('');
  const [loading, setLoading] = useState(false);
  const [selectedFactor, setSelectedFactor] = useState<any>(null);
  const [customModalVisible, setCustomModalVisible] = useState(false);

  const fetchFactors = async (category?: string) => {
    setLoading(true);
    try {
      const response = await getFactorList(category);
      if (response.data) {
        setFactors(response.data.factors || []);
        setCategories(response.data.categories || []);
      }
    } catch (error) {
      message.error('获取因子列表失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchFactors();
  }, []);

  const handleCategoryChange = (value: string) => {
    setSelectedCategory(value);
    fetchFactors(value || undefined);
  };

  const categoryColors: Record<string, string> = {
    technical: 'blue',
    momentum: 'green',
    volatility: 'orange',
    volume: 'purple',
    valuation: 'red',
  };

  const columns = [
    {
      title: '因子名称',
      dataIndex: 'name',
      key: 'name',
      width: 120,
      render: (name: string, record: any) => (
        <Space>
          <Button
            type="link"
            size="small"
            onClick={() => setSelectedFactor(record)}
          >
            {name}
          </Button>
        </Space>
      ),
    },
    {
      title: '分类',
      dataIndex: 'category',
      key: 'category',
      width: 100,
      render: (category: string) => (
        <Tag color={categoryColors[category] || 'default'}>
          {category}
        </Tag>
      ),
    },
    {
      title: '描述',
      dataIndex: 'description',
      key: 'description',
    },
    {
      title: '操作',
      key: 'action',
      width: 100,
      render: (_: any, record: any) => (
        <Button
          size="small"
          icon={<CalculatorOutlined />}
          onClick={() => {
            setSelectedFactor(record);
          }}
        >
          计算
        </Button>
      ),
    },
  ];

  return (
    <div style={{ padding: 24 }}>
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic title="总因子数" value={factors.length} prefix={<SettingOutlined />} />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic title="技术指标" value={factors.filter(f => f.category === 'technical').length} />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic title="动量因子" value={factors.filter(f => f.category === 'momentum').length} />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic title="成交量因子" value={factors.filter(f => f.category === 'volume').length} />
          </Card>
        </Col>
      </Row>

      <Card
        title="因子库"
        extra={
          <Space>
            <Select
              placeholder="选择分类"
              allowClear
              style={{ width: 150 }}
              value={selectedCategory}
              onChange={handleCategoryChange}
            >
              {categories.map(cat => (
                <Option key={cat} value={cat}>{cat}</Option>
              ))}
            </Select>
            <Button
              type="primary"
              icon={<PlusOutlined />}
              onClick={() => setCustomModalVisible(true)}
            >
              自定义因子
            </Button>
          </Space>
        }
      >
        <Table
          columns={columns}
          dataSource={factors}
          rowKey="name"
          loading={loading}
          pagination={{ pageSize: 10 }}
        />
      </Card>

      {/* 因子详情弹窗 */}
      <Modal
        title="因子详情"
        open={!!selectedFactor}
        onCancel={() => setSelectedFactor(null)}
        footer={[
          <Button key="close" onClick={() => setSelectedFactor(null)}>
            关闭
          </Button>,
          <Button key="compute" type="primary" icon={<CalculatorOutlined />}>
            计算因子
          </Button>,
        ]}
      >
        {selectedFactor && (
          <Descriptions column={1}>
            <Descriptions.Item label="因子名称">{selectedFactor.name}</Descriptions.Item>
            <Descriptions.Item label="分类">
              <Tag color={categoryColors[selectedFactor.category]}>
                {selectedFactor.category}
              </Tag>
            </Descriptions.Item>
            <Descriptions.Item label="描述">{selectedFactor.description}</Descriptions.Item>
          </Descriptions>
        )}
      </Modal>

      {/* 自定义因子弹窗 */}
      <Modal
        title="创建自定义因子"
        open={customModalVisible}
        onCancel={() => setCustomModalVisible(false)}
        onOk={() => message.success('自定义因子创建成功')}
      >
        <Space direction="vertical" style={{ width: '100%' }}>
          <div>
            <Text strong>因子名称：</Text>
            <Input placeholder="请输入因子名称" style={{ marginTop: 8 }} />
          </div>
          <div>
            <Text strong>Python代码：</Text>
            <Input.TextArea
              rows={6}
              placeholder="请输入Python代码，例如：&#10;def calculate(data):&#10;    return data['close'].pct_change()"
              style={{ marginTop: 8 }}
            />
          </div>
          <div>
            <Text type="secondary">支持使用 Pandas 进行因子计算</Text>
          </div>
        </Space>
      </Modal>
    </div>
  );
};

// 简单的Statistic组件
const Statistic: React.FC<{ title: string; value: number; prefix?: React.ReactNode }> = ({ title, value, prefix }) => (
  <div>
    <div style={{ color: '#999', fontSize: 14 }}>{title}</div>
    <div style={{ fontSize: 24, fontWeight: 'bold' }}>
      {prefix} {value}
    </div>
  </div>
);

export default FactorListPage;
