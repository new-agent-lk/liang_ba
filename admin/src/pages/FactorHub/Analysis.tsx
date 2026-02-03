import React, { useState } from 'react';
import { Card, Row, Col, Form, Select, Button, Table, Statistic, Space, Typography, Spin } from 'antd';
import { LineChartOutlined } from '@ant-design/icons';
import { analyzeIC, analyzeDecile } from '@/api/factorhub';

const { Option } = Select;
const { Text } = Typography;

const FactorAnalysisPage: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(false);
  const [analysisType, setAnalysisType] = useState<'ic' | 'decile'>('ic');
  const [results, setResults] = useState<any>(null);

  const handleAnalyze = async () => {
    try {
      const values = await form.validateFields();
      setLoading(true);

      if (analysisType === 'ic') {
        const response = await analyzeIC({
          factor_name: values.factor_name,
          method: values.method,
        });
        setResults(response.data);
      } else {
        const response = await analyzeDecile({
          factor_name: values.factor_name,
          n_deciles: values.n_deciles,
        });
        setResults(response.data);
      }
    } catch (error: any) {
      console.error('分析失败', error);
    } finally {
      setLoading(false);
    }
  };

  const icColumns = [
    { title: '日期', dataIndex: 'date', key: 'date' },
    { title: 'IC值', dataIndex: 'ic', key: 'ic', render: (v: number) => v?.toFixed(4) },
  ];

  return (
    <div style={{ padding: 24 }}>
      <Row gutter={16} style={{ marginBottom: 24 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="IC均值"
              value={results?.ic_mean || 0}
              precision={4}
              prefix={<LineChartOutlined />}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="IC标准差"
              value={results?.ic_std || 0}
              precision={4}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="IR (信息比率)"
              value={results?.ir || 0}
              precision={4}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="IC胜率"
              value={(results?.ic_win_rate || 0) * 100}
              precision={1}
              suffix="%"
            />
          </Card>
        </Col>
      </Row>

      <Card title="因子分析配置" style={{ marginBottom: 24 }}>
        <Form form={form} layout="inline">
          <Form.Item
            name="factor_name"
            label="选择因子"
            rules={[{ required: true, message: '请选择因子' }]}
          >
            <Select style={{ width: 180 }} placeholder="选择因子">
              <Option value="ma20">MA20</Option>
              <Option value="rsi">RSI</Option>
              <Option value="macd">MACD</Option>
              <Option value="momentum_1m">1个月动量</Option>
            </Select>
          </Form.Item>

          <Form.Item label="分析类型">
            <Select
              style={{ width: 120 }}
              value={analysisType}
              onChange={setAnalysisType}
            >
              <Option value="ic">IC分析</Option>
              <Option value="decile">分层分析</Option>
            </Select>
          </Form.Item>

          {analysisType === 'ic' && (
            <Form.Item name="method" label="计算方法" initialValue="spearman">
              <Select style={{ width: 120 }}>
                <Option value="spearman">Spearman</Option>
                <Option value="pearson">Pearson</Option>
              </Select>
            </Form.Item>
          )}

          {analysisType === 'decile' && (
            <Form.Item name="n_deciles" label="分层数" initialValue={10}>
              <Select style={{ width: 100 }}>
                <Option value={5}>5层</Option>
                <Option value={10}>10层</Option>
              </Select>
            </Form.Item>
          )}

          <Form.Item>
            <Button
              type="primary"
              icon={<LineChartOutlined />}
              onClick={handleAnalyze}
              loading={loading}
            >
              执行分析
            </Button>
          </Form.Item>
        </Form>
      </Card>

      {loading && (
        <div style={{ textAlign: 'center', padding: 40 }}>
          <Spin size="large" />
          <div style={{ marginTop: 16 }}>
            <Text>正在计算分析结果...</Text>
          </div>
        </div>
      )}

      {results && !loading && (
        <Row gutter={24}>
          <Col span={16}>
            <Card title="IC序列图">
              <div style={{ height: 300, display: 'flex', alignItems: 'center', justifyContent: 'center', background: '#f5f5f5' }}>
                <Text type="secondary">IC时序图展示区域 (Plotly Chart)</Text>
              </div>
            </Card>
          </Col>
          <Col span={8}>
            <Card title="分析统计">
              <Space direction="vertical" style={{ width: '100%' }}>
                <div>
                  <Text>样本数量：</Text>
                  <Text strong>{results.sample_count || '-'}</Text>
                </div>
                <div>
                  <Text>IC均值：</Text>
                  <Text strong>{results.ic_mean?.toFixed(4) || '-'}</Text>
                </div>
                <div>
                  <Text>t统计量：</Text>
                  <Text strong>{results.t_statistic?.toFixed(2) || '-'}</Text>
                </div>
                <div>
                  <Text>p值：</Text>
                  <Text strong style={{ color: results?.t_p_value < 0.05 ? '#52c41a' : undefined }}>
                    {results.t_p_value?.toFixed(4) || '-'}
                  </Text>
                </div>
              </Space>
            </Card>

            {results.long_short_return !== undefined && (
              <Card title="多空收益" style={{ marginTop: 16 }}>
                <Statistic
                  title="多空组合收益"
                  value={results.long_short_return * 100}
                  precision={2}
                  suffix="%"
                  valueStyle={{ color: results.long_short_return > 0 ? '#52c41a' : '#ff4d4f' }}
                />
              </Card>
            )}
          </Col>
        </Row>
      )}

      {results && !loading && results.ic_series && (
        <Card title="IC序列数据" style={{ marginTop: 24 }}>
          <Table
            columns={icColumns}
            dataSource={results.ic_series.slice(0, 20)}
            rowKey="date"
            pagination={false}
            size="small"
          />
        </Card>
      )}
    </div>
  );
};

export default FactorAnalysisPage;
