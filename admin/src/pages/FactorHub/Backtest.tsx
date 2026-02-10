import React, { useState } from "react";
import {
  Card,
  Row,
  Col,
  Form,
  Select,
  InputNumber,
  Button,
  Table,
  Statistic,
  Space,
  Typography,
  Spin,
  Divider,
} from "antd";
import { BarChartOutlined, TrophyOutlined } from "@ant-design/icons";
import { runBacktest } from "@/api/factorhub";

const { Option } = Select;
const { Text } = Typography;

const FactorBacktestPage: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any>(null);

  const handleBacktest = async () => {
    try {
      const values = await form.validateFields();
      setLoading(true);

      const response = await runBacktest({
        factor_name: values.factor_name,
        initial_capital: values.initial_capital,
        rebalance_freq: values.rebalance_freq,
        long_quantile: values.long_quantile,
        short_quantile: values.short_quantile,
      });

      setResults(response.data);
    } catch (error: any) {
      console.error("回测失败", error);
    } finally {
      setLoading(false);
    }
  };

  const columns = [
    { title: "日期", dataIndex: "date", key: "date" },
    {
      title: "组合价值",
      dataIndex: "value",
      key: "value",
      render: (v: number) => v?.toLocaleString(),
    },
  ];

  return (
    <div style={{ padding: 24 }}>
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="总收益率"
              value={(results?.total_return || 0) * 100}
              precision={2}
              suffix="%"
              prefix={<TrophyOutlined />}
              valueStyle={{
                color: (results?.total_return || 0) > 0 ? "#52c41a" : "#ff4d4f",
              }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="年化收益率"
              value={(results?.annual_return || 0) * 100}
              precision={2}
              suffix="%"
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="夏普比率"
              value={results?.sharpe_ratio || 0}
              precision={2}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="最大回撤"
              value={(results?.max_drawdown || 0) * 100}
              precision={2}
              suffix="%"
              valueStyle={{
                color:
                  (results?.max_drawdown || 0) > -0.1 ? "#52c41a" : "#ff4d4f",
              }}
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="胜率"
              value={(results?.win_rate || 0) * 100}
              precision={1}
              suffix="%"
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="初始资金"
              value={results?.initial_capital || 1000000}
              precision={0}
              prefix="¥"
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="最终价值"
              value={results?.final_value || 0}
              precision={0}
              prefix="¥"
            />
          </Card>
        </Col>
      </Row>

      <Card title="回测配置" style={{ marginBottom: 24 }}>
        <Form form={form} layout="inline">
          <Form.Item
            name="factor_name"
            label="选择因子"
            rules={[{ required: true, message: "请选择因子" }]}
          >
            <Select style={{ width: 150 }} placeholder="选择因子">
              <Option value="ma20">MA20</Option>
              <Option value="rsi">RSI</Option>
              <Option value="momentum_1m">1个月动量</Option>
            </Select>
          </Form.Item>

          <Form.Item
            name="initial_capital"
            label="初始资金"
            initialValue={1000000}
          >
            <InputNumber
              style={{ width: 120 }}
              formatter={(value) => `¥ ${value}`}
            />
          </Form.Item>

          <Form.Item
            name="rebalance_freq"
            label="再平衡频率"
            initialValue="weekly"
          >
            <Select style={{ width: 100 }}>
              <Option value="daily">日频</Option>
              <Option value="weekly">周频</Option>
              <Option value="monthly">月频</Option>
            </Select>
          </Form.Item>

          <Form.Item name="long_quantile" label="做多分层" initialValue={3}>
            <InputNumber min={1} max={10} style={{ width: 80 }} />
          </Form.Item>

          <Form.Item name="short_quantile" label="做空分层" initialValue={8}>
            <InputNumber min={1} max={10} style={{ width: 80 }} />
          </Form.Item>

          <Form.Item>
            <Button
              type="primary"
              icon={<BarChartOutlined />}
              onClick={handleBacktest}
              loading={loading}
            >
              运行回测
            </Button>
          </Form.Item>
        </Form>
      </Card>

      {loading && (
        <div style={{ textAlign: "center", padding: 40 }}>
          <Spin size="large" />
          <div style={{ marginTop: 16 }}>
            <Text>回测运行中...</Text>
          </div>
        </div>
      )}

      {results && !loading && (
        <Row gutter={24}>
          <Col span={16}>
            <Card title="资金曲线">
              <div
                style={{
                  height: 350,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  background: "#f5f5f5",
                }}
              >
                <Text type="secondary">资金曲线图 (Plotly Chart)</Text>
              </div>
            </Card>

            <Card title="回测详情" style={{ marginTop: 24 }}>
              <Table
                columns={columns}
                dataSource={results.portfolio_values?.slice(0, 20) || []}
                rowKey="date"
                pagination={false}
                size="small"
              />
            </Card>
          </Col>

          <Col span={8}>
            <Card title="绩效指标">
              <Space direction="vertical" style={{ width: "100%" }}>
                <div
                  style={{ display: "flex", justifyContent: "space-between" }}
                >
                  <Text>总收益率：</Text>
                  <Text
                    strong
                    style={{
                      color: results.total_return > 0 ? "#52c41a" : "#ff4d4f",
                    }}
                  >
                    {(results.total_return * 100).toFixed(2)}%
                  </Text>
                </div>
                <Divider style={{ margin: "12px 0" }} />
                <div
                  style={{ display: "flex", justifyContent: "space-between" }}
                >
                  <Text>年化收益率：</Text>
                  <Text strong>
                    {(results.annual_return * 100).toFixed(2)}%
                  </Text>
                </div>
                <Divider style={{ margin: "12px 0" }} />
                <div
                  style={{ display: "flex", justifyContent: "space-between" }}
                >
                  <Text>年化波动率：</Text>
                  <Text strong>{(results.volatility * 100).toFixed(2)}%</Text>
                </div>
                <Divider style={{ margin: "12px 0" }} />
                <div
                  style={{ display: "flex", justifyContent: "space-between" }}
                >
                  <Text>夏普比率：</Text>
                  <Text strong>{results.sharpe_ratio.toFixed(2)}</Text>
                </div>
                <Divider style={{ margin: "12px 0" }} />
                <div
                  style={{ display: "flex", justifyContent: "space-between" }}
                >
                  <Text>最大回撤：</Text>
                  <Text strong style={{ color: "#ff4d4f" }}>
                    {(results.max_drawdown * 100).toFixed(2)}%
                  </Text>
                </div>
                <Divider style={{ margin: "12px 0" }} />
                <div
                  style={{ display: "flex", justifyContent: "space-between" }}
                >
                  <Text>胜率：</Text>
                  <Text strong>{(results.win_rate * 100).toFixed(1)}%</Text>
                </div>
              </Space>
            </Card>

            <Card title="交易统计" style={{ marginTop: 16 }}>
              <Space direction="vertical" style={{ width: "100%" }}>
                <div
                  style={{ display: "flex", justifyContent: "space-between" }}
                >
                  <Text>初始资金：</Text>
                  <Text>¥{results.initial_capital?.toLocaleString()}</Text>
                </div>
                <Divider style={{ margin: "12px 0" }} />
                <div
                  style={{ display: "flex", justifyContent: "space-between" }}
                >
                  <Text>最终价值：</Text>
                  <Text strong style={{ color: "#52c41a" }}>
                    ¥{results.final_value?.toLocaleString()}
                  </Text>
                </div>
                <Divider style={{ margin: "12px 0" }} />
                <div
                  style={{ display: "flex", justifyContent: "space-between" }}
                >
                  <Text>绝对收益：</Text>
                  <Text
                    strong
                    style={{
                      color:
                        results.final_value - results.initial_capital > 0
                          ? "#52c41a"
                          : "#ff4d4f",
                    }}
                  >
                    ¥
                    {(
                      results.final_value - results.initial_capital
                    )?.toLocaleString()}
                  </Text>
                </div>
              </Space>
            </Card>
          </Col>
        </Row>
      )}
    </div>
  );
};

export default FactorBacktestPage;
