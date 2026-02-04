import React, { useState, useEffect, useCallback } from 'react';
import { Card, Table, Tag, Space, Button, Input, Select, DatePicker, Modal, message, Descriptions, Row, Col, Statistic } from 'antd';
import { ReloadOutlined, SearchOutlined, PlayCircleOutlined, EyeOutlined } from '@ant-design/icons';
import { LOG_TYPE_CHOICES, LOG_LEVEL_CHOICES, LogEntry, LogRotationStatus, LogType } from '@/types';
import { getLogs, getRotationStatus, performRotationAction } from '@/api/logs';
import dayjs from 'dayjs';

const { RangePicker } = DatePicker;
const { Option } = Select;

const Logs: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [total, setTotal] = useState(0);
  const [offset, setOffset] = useState(0);
  const [limit] = useState(50);
  const [hasMore, setHasMore] = useState(false);

  // Filter states
  const [logType, setLogType] = useState<LogType>('app');
  const [level, setLevel] = useState<string>('');
  const [traceId, setTraceId] = useState<string>('');
  const [search, setSearch] = useState<string>('');
  const [dateRange, setDateRange] = useState<[dayjs.Dayjs, dayjs.Dayjs] | null>(null);

  // Rotation status
  const [rotationStatus, setRotationStatus] = useState<LogRotationStatus | null>(null);

  // Expanded log details
  const [expandedLog, setExpandedLog] = useState<LogEntry | null>(null);
  const [detailModalOpen, setDetailModalOpen] = useState(false);

  const fetchLogs = useCallback(async () => {
    setLoading(true);
    try {
      const params: Record<string, unknown> = {
        log_type: logType,
        offset,
        limit,
      };
      if (level) params.level = level;
      if (traceId) params.trace_id = traceId;
      if (search) params.search = search;
      if (dateRange) {
        params.start_time = dateRange[0].toISOString();
        params.end_time = dateRange[1].toISOString();
      }

      const response = await getLogs(params as any);
      setLogs(response.entries);
      setTotal(response.total);
      setHasMore(response.has_more);
    } catch (error) {
      message.error('获取日志失败');
    } finally {
      setLoading(false);
    }
  }, [logType, level, traceId, search, dateRange, offset, limit]);

  const fetchRotationStatus = useCallback(async () => {
    try {
      const status = await getRotationStatus(logType);
      setRotationStatus(status);
    } catch (error) {
      console.error('获取滚动状态失败:', error);
    }
  }, [logType]);

  useEffect(() => {
    fetchLogs();
    fetchRotationStatus();
  }, [fetchLogs, fetchRotationStatus]);

  const handleRotate = async () => {
    Modal.confirm({
      title: '确认滚动',
      content: `确定要滚动 ${LOG_TYPE_CHOICES.find(t => t.value === logType)?.label || logType} 日志吗？`,
      onOk: async () => {
        try {
          const result = await performRotationAction({ action: 'rotate', log_type: logType });
          if (result.rotated) {
            message.success('日志滚动成功');
            fetchLogs();
            fetchRotationStatus();
          } else {
            message.info(`无需滚动: ${result.reason}`);
          }
        } catch (error) {
          message.error('滚动失败');
        }
      },
    });
  };

  const handleViewDetail = (record: LogEntry) => {
    setExpandedLog(record);
    setDetailModalOpen(true);
  };

  const getLevelColor = (level: string) => {
    const colors: Record<string, string> = {
      DEBUG: 'default',
      INFO: 'processing',
      WARNING: 'warning',
      ERROR: 'error',
      CRITICAL: 'red',
    };
    return colors[level] || 'default';
  };

  const columns = [
    {
      title: '时间',
      dataIndex: 'timestamp',
      key: 'timestamp',
      width: 180,
      render: (text: string) => dayjs(text).format('YYYY-MM-DD HH:mm:ss'),
    },
    {
      title: '级别',
      dataIndex: 'level',
      key: 'level',
      width: 100,
      render: (level: string) => (
        <Tag color={getLevelColor(level)}>{level}</Tag>
      ),
    },
    {
      title: '消息',
      dataIndex: 'message',
      key: 'message',
      ellipsis: true,
    },
    {
      title: 'Logger',
      dataIndex: 'logger',
      key: 'logger',
      width: 150,
      ellipsis: true,
    },
    {
      title: 'Trace ID',
      dataIndex: 'trace_id',
      key: 'trace_id',
      width: 120,
      ellipsis: true,
    },
    {
      title: '用户',
      dataIndex: 'user_id',
      key: 'user_id',
      width: 80,
      render: (id: number) => id || '-',
    },
    {
      title: '操作',
      key: 'action',
      width: 80,
      render: (_: unknown, record: LogEntry) => (
        <Space>
          <Button
            type="link"
            size="small"
            icon={<EyeOutlined />}
            onClick={() => handleViewDetail(record)}
          >
            详情
          </Button>
        </Space>
      ),
    },
  ];

  return (
    <div>
      {/* Stats Cards */}
      <Row gutter={16} style={{ marginBottom: 16 }}>
        <Col span={6}>
          <Card>
            <Statistic
              title="当前日志类型"
              value={LOG_TYPE_CHOICES.find(t => t.value === logType)?.label || logType}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="文件大小"
              value={rotationStatus?.current_size_mb || 0}
              suffix="MB"
              valueStyle={{ color: rotationStatus && rotationStatus.current_size_mb > 8 ? '#cf1322' : '#3f8600' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="归档文件数"
              value={rotationStatus?.archived_files_count || 0}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Descriptions size="small" column={1}>
              <Descriptions.Item label="最大文件">
                {rotationStatus?.policy.max_size_mb || 10} MB
              </Descriptions.Item>
              <Descriptions.Item label="保留文件">
                {rotationStatus?.policy.max_files || 10} 个
              </Descriptions.Item>
            </Descriptions>
          </Card>
        </Col>
      </Row>

      {/* Filters */}
      <Card style={{ marginBottom: 16 }}>
        <Space wrap>
          <span>日志类型:</span>
          <Select value={logType} onChange={setLogType} style={{ width: 120 }}>
            {LOG_TYPE_CHOICES.map(choice => (
              <Option key={choice.value} value={choice.value}>{choice.label}</Option>
            ))}
          </Select>

          <span>级别:</span>
          <Select
            value={level}
            onChange={setLevel}
            style={{ width: 120 }}
            placeholder="选择级别"
            allowClear
          >
            {LOG_LEVEL_CHOICES.map(choice => (
              <Option key={choice.value} value={choice.value}>{choice.label}</Option>
            ))}
          </Select>

          <span>Trace ID:</span>
          <Input
            placeholder="Trace ID"
            value={traceId}
            onChange={e => setTraceId(e.target.value)}
            style={{ width: 150 }}
          />

          <span>搜索:</span>
          <Input
            placeholder="搜索消息内容"
            value={search}
            onChange={e => setSearch(e.target.value)}
            style={{ width: 200 }}
          />

          <span>时间范围:</span>
          <RangePicker
            value={dateRange}
            onChange={dates => setDateRange(dates as [dayjs.Dayjs, dayjs.Dayjs] | null)}
            showTime
          />

          <Button type="primary" icon={<SearchOutlined />} onClick={fetchLogs}>
            搜索
          </Button>
          <Button icon={<ReloadOutlined />} onClick={fetchLogs}>
            刷新
          </Button>

          <Button icon={<PlayCircleOutlined />} onClick={handleRotate}>
            立即滚动
          </Button>
        </Space>
      </Card>

      {/* Logs Table */}
      <Card
        title={
          <Space>
            <span>日志列表</span>
            <Tag>共 {total} 条</Tag>
          </Space>
        }
        extra={
          <Space>
            <Button
              size="small"
              onClick={() => setOffset(0)}
              disabled={offset === 0}
            >
              首页
            </Button>
            <Button
              size="small"
              onClick={() => setOffset(Math.max(0, offset - limit))}
              disabled={offset === 0}
            >
              上一页
            </Button>
            <Button
              size="small"
              onClick={() => setOffset(offset + limit)}
              disabled={!hasMore}
            >
              下一页
            </Button>
          </Space>
        }
      >
        <Table
          columns={columns}
          dataSource={logs}
          loading={loading}
          rowKey={(_, index) => index?.toString() || Math.random().toString()}
          pagination={false}
          size="small"
          scroll={{ x: 1000 }}
        />
      </Card>

      {/* Detail Modal */}
      <Modal
        title="日志详情"
        open={detailModalOpen}
        onCancel={() => setDetailModalOpen(false)}
        footer={null}
        width={800}
      >
        {expandedLog && (
          <div>
            <Descriptions column={2} bordered size="small">
              <Descriptions.Item label="时间">{dayjs(expandedLog.timestamp).format('YYYY-MM-DD HH:mm:ss')}</Descriptions.Item>
              <Descriptions.Item label="级别">
                <Tag color={getLevelColor(expandedLog.level)}>{expandedLog.level}</Tag>
              </Descriptions.Item>
              <Descriptions.Item label="Logger">{expandedLog.logger}</Descriptions.Item>
              <Descriptions.Item label="模块">{expandedLog.module || '-'}</Descriptions.Item>
              <Descriptions.Item label="函数">{expandedLog.function || '-'}</Descriptions.Item>
              <Descriptions.Item label="行号">{expandedLog.line || '-'}</Descriptions.Item>
              <Descriptions.Item label="Trace ID">{expandedLog.trace_id || '-'}</Descriptions.Item>
              <Descriptions.Item label="Request ID">{expandedLog.request_id || '-'}</Descriptions.Item>
              <Descriptions.Item label="用户 ID">{expandedLog.user_id || '-'}</Descriptions.Item>
              <Descriptions.Item label="进程 ID">{expandedLog.process_id || '-'}</Descriptions.Item>
              <Descriptions.Item label="线程 ID">{expandedLog.thread_id || '-'}</Descriptions.Item>
            </Descriptions>
            <Card title="消息内容" size="small" style={{ marginTop: 16 }}>
              <pre style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-all', margin: 0 }}>
                {expandedLog.message}
              </pre>
            </Card>
            {expandedLog.extra && Object.keys(expandedLog.extra).length > 0 && (
              <Card title="额外信息" size="small" style={{ marginTop: 16 }}>
                <pre style={{ whiteSpace: 'pre-wrap', wordBreak: 'break-all', margin: 0 }}>
                  {JSON.stringify(expandedLog.extra, null, 2)}
                </pre>
              </Card>
            )}
          </div>
        )}
      </Modal>
    </div>
  );
};

export default Logs;
