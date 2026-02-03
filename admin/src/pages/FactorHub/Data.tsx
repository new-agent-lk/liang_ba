import React, { useState } from 'react';
import { Card, Row, Col, Form, Select, DatePicker, Button, Table, Space, Statistic, message } from 'antd';
import dayjs from 'dayjs';
import { DatabaseOutlined, DownloadOutlined, DeleteOutlined, ReloadOutlined } from '@ant-design/icons';
import { fetchMarketData, getCacheInfo, clearCache } from '@/api/factorhub';

const { Option } = Select;
const { RangePicker } = DatePicker;

const FactorData: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<any[]>([]);
  const [stats, setStats] = useState({ count: 0, symbols: 0, cached: 0 });
  const [cacheInfo, setCacheInfo] = useState({ total_files: 0, total_size_mb: 0 });

  const handleFetchData = async () => {
    try {
      const values = await form.validateFields();
      setLoading(true);

      const response = await fetchMarketData({
        stock_pool: values.stock_pool,
        start_date: values.date_range[0].format('YYYY-MM-DD'),
        end_date: values.date_range[1].format('YYYY-MM-DD'),
        adjust: values.adjust,
      });

      if (response.data) {
        setData(response.data.data || []);
        setStats({
          count: response.data.count,
          symbols: response.data.symbols,
          cached: 0,
        });
        message.success(`成功获取 ${response.data.count} 条数据`);
      }
    } catch (error: any) {
      message.error(error.response?.data?.error || '获取数据失败');
    } finally {
      setLoading(false);
    }
  };

  const handleGetCacheInfo = async () => {
    try {
      const response = await getCacheInfo();
      setCacheInfo(response.data);
    } catch (error) {
      console.error('获取缓存信息失败');
    }
  };

  const handleClearCache = async () => {
    try {
      await clearCache();
      message.success('缓存已清理');
      handleGetCacheInfo();
    } catch (error) {
      message.error('清理缓存失败');
    }
  };

  const columns = [
    {
      title: '股票代码',
      dataIndex: 'symbol',
      key: 'symbol',
      width: 100,
    },
    {
      title: '日期',
      dataIndex: 'date',
      key: 'date',
      width: 120,
      render: (date: string) => new Date(date).toLocaleDateString(),
    },
    {
      title: '开盘',
      dataIndex: 'open',
      key: 'open',
      width: 100,
      render: (val: number) => val?.toFixed(2) || '-',
    },
    {
      title: '收盘',
      dataIndex: 'close',
      key: 'close',
      width: 100,
      render: (val: number) => val?.toFixed(2) || '-',
    },
    {
      title: '最高',
      dataIndex: 'high',
      key: 'high',
      width: 100,
      render: (val: number) => val?.toFixed(2) || '-',
    },
    {
      title: '最低',
      dataIndex: 'low',
      key: 'low',
      width: 100,
      render: (val: number) => val?.toFixed(2) || '-',
    },
    {
      title: '成交量',
      dataIndex: 'volume',
      key: 'volume',
      width: 120,
      render: (val: number) => val ? (val / 10000).toFixed(0) + '万' : '-',
    },
    {
      title: '涨跌幅',
      dataIndex: 'pct_change',
      key: 'pct_change',
      width: 100,
      render: (val: number) => (
        <span style={{ color: val > 0 ? '#ff4d4f' : val < 0 ? '#52c41a' : undefined }}>
          {val ? val.toFixed(2) + '%' : '-'}
        </span>
      ),
    },
  ];

  return (
    <div style={{ padding: 24 }}>
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="数据记录"
              value={stats.count}
              prefix={<DatabaseOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="股票数量"
              value={stats.symbols}
              prefix={<DatabaseOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="缓存文件"
              value={cacheInfo.total_files}
              prefix={<DatabaseOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="缓存大小"
              value={cacheInfo.total_size_mb}
              precision={1}
              suffix="MB"
            />
          </Card>
        </Col>
      </Row>

      <Card title="数据获取配置" style={{ marginBottom: 24 }}>
        <Form form={form} layout="inline">
          <Form.Item
            name="stock_pool"
            label="股票池"
            initialValue="hs300"
          >
            <Select style={{ width: 150 }}>
              <Option value="hs300">沪深300</Option>
              <Option value="zz500">中证500</Option>
              <Option value="cyb">创业板</Option>
            </Select>
          </Form.Item>

          <Form.Item
            name="date_range"
            label="日期范围"
            initialValue={[dayjs('2020-01-01'), dayjs('2023-12-31')]}
          >
            <RangePicker />
          </Form.Item>

          <Form.Item
            name="adjust"
            label="复权类型"
            initialValue="qfq"
          >
            <Select style={{ width: 120 }}>
              <Option value="qfq">前复权</Option>
              <Option value="hfq">后复权</Option>
              <Option value="none">不复权</Option>
            </Select>
          </Form.Item>

          <Form.Item>
            <Button
              type="primary"
              icon={<DownloadOutlined />}
              onClick={handleFetchData}
              loading={loading}
            >
              获取数据
            </Button>
          </Form.Item>
        </Form>
      </Card>

      <Card
        title="数据预览"
        extra={
          <Space>
            <Button icon={<ReloadOutlined />} onClick={handleGetCacheInfo}>刷新缓存</Button>
            <Button icon={<DeleteOutlined />} onClick={handleClearCache}>清理缓存</Button>
          </Space>
        }
      >
        <Table
          columns={columns}
          dataSource={data.slice(0, 100)}
          rowKey={(record) => `${record.symbol}-${record.date}`}
          pagination={{ pageSize: 10, showQuickJumper: true }}
          size="small"
          scroll={{ x: 1000 }}
        />
        {data.length > 100 && (
          <div style={{ textAlign: 'center', marginTop: 8, color: '#999' }}>
            显示前100条，共 {data.length} 条数据
          </div>
        )}
      </Card>
    </div>
  );
};

export default FactorData;
