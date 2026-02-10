import React, { useEffect, useState } from "react";
import {
  Card,
  Row,
  Col,
  Form,
  Select,
  DatePicker,
  Button,
  Table,
  Space,
  Statistic,
  message,
  Empty,
  Tag,
} from "antd";
import dayjs from "dayjs";
import {
  DatabaseOutlined,
  DownloadOutlined,
  DeleteOutlined,
  ReloadOutlined,
  SyncOutlined,
} from "@ant-design/icons";
import { fetchMarketData, getCacheInfo, clearCache } from "@/api/factorhub";

const { Option } = Select;
const { RangePicker } = DatePicker;

type MarketDataResult = {
  count?: number;
  symbols?: number;
  data?: any[];
};

type CacheInfoResult = {
  total_files: number;
  total_size_mb: number;
};

const FactorData: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<any[]>([]);
  const [stats, setStats] = useState({ count: 0, symbols: 0, cached: 0 });
  const [cacheInfo, setCacheInfo] = useState({
    total_files: 0,
    total_size_mb: 0,
  });
  const [lastFetchTime, setLastFetchTime] = useState<string>("");

  useEffect(() => {
    handleGetCacheInfo();
  }, []);

  const handleFetchData = async () => {
    try {
      const values = await form.validateFields();
      setLoading(true);

      const result = (await fetchMarketData({
        stock_pool: values.stock_pool,
        start_date: values.date_range[0].format("YYYY-MM-DD"),
        end_date: values.date_range[1].format("YYYY-MM-DD"),
        adjust: values.adjust,
      })) as MarketDataResult;

      // request拦截器返回的是response.data，即 {count, symbols, data}
      // result.data 是数据数组，result.count是总数量
      const dataList = result.data || [];
      setData(dataList);
      setStats({
        count: result.count || dataList.length,
        symbols: result.symbols || 0,
        cached: 0,
      });
      setLastFetchTime(new Date().toLocaleString());
      message.success(`成功获取 ${result.count || dataList.length} 条数据`);
    } catch (error: any) {
      message.error(error.response?.data?.error || "获取数据失败");
    } finally {
      setLoading(false);
    }
  };

  const handleRefreshData = async () => {
    // 使用当前表单值重新获取数据
    try {
      const values = form.getFieldsValue();
      if (!values.date_range) {
        message.warning("请先设置日期范围");
        return;
      }
      setLoading(true);

      const result = (await fetchMarketData({
        stock_pool: values.stock_pool,
        start_date: values.date_range[0].format("YYYY-MM-DD"),
        end_date: values.date_range[1].format("YYYY-MM-DD"),
        adjust: values.adjust,
      })) as MarketDataResult;

      const dataList = result.data || [];
      setData(dataList);
      setStats({
        count: result.count || dataList.length,
        symbols: result.symbols || 0,
        cached: 0,
      });
      setLastFetchTime(new Date().toLocaleString());
      message.success(`刷新成功: ${result.count || dataList.length} 条数据`);
    } catch (error: any) {
      message.error(error.response?.data?.error || "刷新数据失败");
    } finally {
      setLoading(false);
    }
  };

  const handleGetCacheInfo = async () => {
    try {
      const response = (await getCacheInfo()) as Partial<CacheInfoResult>;
      setCacheInfo({
        total_files: response.total_files || 0,
        total_size_mb: response.total_size_mb || 0,
      });
    } catch (error: any) {
      message.error(error?.response?.data?.error || "获取缓存信息失败");
    }
  };

  const handleClearCache = async () => {
    try {
      await clearCache();
      message.success("缓存已清理");
      handleGetCacheInfo();
      // 清理后清空数据
      setData([]);
      setStats({ count: 0, symbols: 0, cached: 0 });
    } catch (error) {
      message.error("清理缓存失败");
    }
  };

  const columns = [
    {
      title: "股票代码",
      dataIndex: "symbol",
      key: "symbol",
      width: 100,
      fixed: "left" as const,
      render: (text: string) => <Tag color="blue">{text}</Tag>,
    },
    {
      title: "日期",
      dataIndex: "date",
      key: "date",
      width: 120,
      sorter: (a: any, b: any) =>
        new Date(a.date).getTime() - new Date(b.date).getTime(),
      render: (date: string) => {
        const d = new Date(date);
        return d.toLocaleDateString("zh-CN");
      },
    },
    {
      title: "开盘",
      dataIndex: "open",
      key: "open",
      width: 100,
      align: "right" as const,
      render: (val: number) => val?.toFixed(2) || "-",
    },
    {
      title: "收盘",
      dataIndex: "close",
      key: "close",
      width: 100,
      align: "right" as const,
      render: (val: number) => val?.toFixed(2) || "-",
    },
    {
      title: "最高",
      dataIndex: "high",
      key: "high",
      width: 100,
      align: "right" as const,
      render: (val: number) => val?.toFixed(2) || "-",
    },
    {
      title: "最低",
      dataIndex: "low",
      key: "low",
      width: 100,
      align: "right" as const,
      render: (val: number) => val?.toFixed(2) || "-",
    },
    {
      title: "涨跌幅",
      dataIndex: "pct_change",
      key: "pct_change",
      width: 100,
      align: "right" as const,
      sorter: (a: any, b: any) => (a.pct_change || 0) - (b.pct_change || 0),
      render: (val: number) => {
        if (val === null || val === undefined) return "-";
        const color = val > 0 ? "#ff4d4f" : val < 0 ? "#52c41a" : undefined;
        const symbol = val > 0 ? "+" : "";
        return (
          <span style={{ color, fontWeight: 500 }}>
            {symbol}
            {val.toFixed(2)}%
          </span>
        );
      },
    },
    {
      title: "成交量",
      dataIndex: "volume",
      key: "volume",
      width: 120,
      align: "right" as const,
      render: (val: number) => (val ? (val / 10000).toFixed(0) + "万" : "-"),
    },
    {
      title: "成交额",
      dataIndex: "amount",
      key: "amount",
      width: 120,
      align: "right" as const,
      render: (val: number) =>
        val ? (val / 100000000).toFixed(2) + "亿" : "-",
    },
    {
      title: "换手率",
      dataIndex: "turnover",
      key: "turnover",
      width: 100,
      align: "right" as const,
      render: (val: number) => (val ? (val * 100).toFixed(2) + "%" : "-"),
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
              suffix="条"
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="股票数量"
              value={stats.symbols}
              prefix={<DatabaseOutlined />}
              suffix="只"
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="缓存文件"
              value={cacheInfo?.total_files || 0}
              prefix={<DatabaseOutlined />}
              suffix="个"
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="缓存大小"
              value={cacheInfo?.total_size_mb?.toFixed(2) || 0}
              prefix={<DatabaseOutlined />}
              suffix="MB"
            />
          </Card>
        </Col>
      </Row>

      <Card title="数据获取配置" style={{ marginBottom: 24 }}>
        <Form form={form} layout="inline">
          <Form.Item name="stock_pool" label="股票池" initialValue="hs300">
            <Select style={{ width: 150 }}>
              <Option value="hs300">沪深300</Option>
              <Option value="zz500">中证500</Option>
              <Option value="cyb">创业板</Option>
            </Select>
          </Form.Item>

          <Form.Item
            name="date_range"
            label="日期范围"
            initialValue={[dayjs("2025-12-01"), dayjs().add(0, "day")]}
            rules={[{ required: true, message: "请选择日期范围" }]}
          >
            <RangePicker />
          </Form.Item>

          <Form.Item name="adjust" label="复权类型" initialValue="qfq">
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
        title={
          <Space>
            <span>数据预览</span>
            {lastFetchTime && (
              <Tag icon={<SyncOutlined spin={loading} />} color="processing">
                更新于 {lastFetchTime}
              </Tag>
            )}
          </Space>
        }
        extra={
          <Space>
            <Button
              icon={<ReloadOutlined />}
              onClick={handleRefreshData}
              loading={loading}
              disabled={data.length === 0}
            >
              刷新数据
            </Button>
            <Button icon={<DeleteOutlined />} onClick={handleClearCache} danger>
              清理缓存
            </Button>
          </Space>
        }
      >
        {data.length > 0 ? (
          <>
            <Table
              columns={columns}
              dataSource={data}
              rowKey={(record) => `${record.symbol}-${record.date}`}
              pagination={{
                pageSize: 10,
                showQuickJumper: true,
                showSizeChanger: true,
                showTotal: (total: number) => `共 ${total} 条记录`,
              }}
              size="small"
              scroll={{ x: 1200 }}
              loading={loading}
            />
            <div style={{ textAlign: "center", marginTop: 8, color: "#999" }}>
              当前显示 {data.length} 条数据，来自 {stats.symbols} 只股票
            </div>
          </>
        ) : (
          <Empty
            description={
              <span>
                暂无数据，点击
                <a onClick={handleFetchData} style={{ marginLeft: 8 }}>
                  获取数据
                </a>
              </span>
            }
          >
            <Button
              type="primary"
              icon={<DownloadOutlined />}
              onClick={handleFetchData}
              loading={loading}
            >
              获取数据
            </Button>
          </Empty>
        )}
      </Card>
    </div>
  );
};

export default FactorData;
