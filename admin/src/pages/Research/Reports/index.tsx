import React, { useState } from 'react';
import { Table, Tag, Button, Space, Modal, Form, Input, Select, InputNumber, DatePicker, message, Popconfirm, Upload, UploadFile } from 'antd';
import { UploadOutlined, FileTextOutlined } from '@ant-design/icons';
import { PlusOutlined, EditOutlined, DeleteOutlined, EyeOutlined, CheckOutlined, CloseOutlined, ReloadOutlined } from '@ant-design/icons';
import PageHeader from '@/components/Common/PageHeader';
import DataTable from '@/components/Common/DataTable';
import { MarkdownFormItem } from '@/components/Common/MarkdownEditor';
import { useTable } from '@/hooks/useTable';
import { getReports, createReport, updateReport, deleteReport, submitReport, reviewReport, publishReport, unpublishReport } from '@/api/reports';
import { ResearchReport, RESEARCH_STRATEGY_TYPES } from '@/types';
import { useAuthStore } from '@/store/useAuthStore';

const { TextArea } = Input;
const { Option } = Select;

const Reports: React.FC = () => {
  const [form] = Form.useForm();
  const [modalVisible, setModalVisible] = useState(false);
  const [isEdit, setIsEdit] = useState(false);
  const [currentReport, setCurrentReport] = useState<ResearchReport | null>(null);
  const [submitLoading, setSubmitLoading] = useState(false);
  const [detailImageFileList, setDetailImageFileList] = useState<UploadFile[]>([]);
  // 文档编辑弹框状态
  const [contentModalVisible, setContentModalVisible] = useState(false);
  const [contentEditReport, setContentEditReport] = useState<ResearchReport | null>(null);
  const [contentSubmitLoading, setContentSubmitLoading] = useState(false);

  const { user } = useAuthStore();
  const isSuperAdmin = user?.is_superuser || false;
  const currentUserId = user?.id;

  const { data, loading: tableLoading, pagination, refresh } = useTable<ResearchReport>({
    fetchData: getReports,
  });

  // 检查是否可以编辑报告
  const canEditReport = (report: ResearchReport) => {
    if (isSuperAdmin) {
      // 超管可以编辑所有报告
      return true;
    }
    // 普通用户只能编辑自己的草稿或被拒绝的报告
    if (report.author_id === currentUserId && (report.status === 'draft' || report.status === 'rejected')) {
      return true;
    }
    return false;
  };

  // 检查是否可以删除报告
  const canDeleteReport = (report: ResearchReport) => {
    if (isSuperAdmin) {
      // 超管可以删除所有草稿或被拒绝的报告
      return report.status === 'draft' || report.status === 'rejected';
    }
    // 普通用户只能删除自己的草稿或被拒绝的报告
    return report.author_id === currentUserId && (report.status === 'draft' || report.status === 'rejected');
  };

  // 检查是否可以提交审核
  const canSubmitForReview = (report: ResearchReport) => {
    return report.author_id === currentUserId && report.status === 'draft';
  };

  // 检查是否可以审核（部门负责人权限）
  const canReview = (report: ResearchReport) => {
    // 超管可以审核，待审核状态的文章
    return isSuperAdmin && report.status === 'pending';
  };

  // 检查是否可以发布
  const canPublish = (report: ResearchReport) => {
    // 超管可以发布已通过审核的文章
    return isSuperAdmin && report.status === 'approved';
  };

  // 检查是否可以取消发布
  const canUnpublish = (report: ResearchReport) => {
    // 超管可以取消发布已发布的文章
    return isSuperAdmin && report.status === 'published';
  };

  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      draft: 'default',
      pending: 'processing',
      approved: 'success',
      rejected: 'error',
      published: 'blue',
    };
    return colors[status] || 'default';
  };

  const getStatusLabel = (status: string) => {
    const labels: Record<string, string> = {
      draft: '草稿',
      pending: '待审核',
      approved: '已通过',
      rejected: '已拒绝',
      published: '已发布',
    };
    return labels[status] || status;
  };

  const handleAdd = () => {
    setCurrentReport(null);
    setIsEdit(false);
    setDetailImageFileList([]);
    form.resetFields();
    form.setFieldsValue({ status: 'draft' });
    setModalVisible(true);
  };

  const handleEdit = (record: ResearchReport) => {
    setCurrentReport(record);
    setIsEdit(true);
    // 编辑时将图片URL转换为Upload组件需要的格式
    const detailImageList = record.detail_image
      ? [{ uid: '-1', name: 'detail_image', status: 'done', url: record.detail_image }]
      : [];
    setDetailImageFileList(detailImageList);
    form.setFieldsValue({
      ...record,
      backtest_start_date: record.backtest_start_date ? new Date(record.backtest_start_date) : null,
      backtest_end_date: record.backtest_end_date ? new Date(record.backtest_end_date) : null,
    });
    setModalVisible(true);
  };

  const handleSubmit = async (values: any) => {
    setSubmitLoading(true);
    try {
      if (isEdit && currentReport) {
        await updateReport(currentReport.id, values);
        message.success('更新成功');
      } else {
        await createReport(values);
        message.success('创建成功');
      }
      setModalVisible(false);
      refresh();
    } catch (error) {
      message.error(isEdit ? '更新失败' : '创建失败');
    } finally {
      setSubmitLoading(false);
    }
  };

  const handleSubmitForReview = async (record: ResearchReport) => {
    try {
      await submitReport(record.id);
      message.success('已提交审核');
      refresh();
    } catch (error) {
      message.error('提交失败');
    }
  };

  const handleReview = async (record: ResearchReport, status: 'approved' | 'rejected') => {
    try {
      await reviewReport(record.id, { status, review_notes: '' });
      message.success(status === 'approved' ? '审核通过' : '已拒绝');
      refresh();
    } catch (error) {
      message.error('审核失败');
    }
  };

  const handlePublish = async (record: ResearchReport) => {
    try {
      await publishReport(record.id);
      message.success('已发布');
      refresh();
    } catch (error) {
      message.error('发布失败');
    }
  };

  const handleUnpublish = async (record: ResearchReport) => {
    try {
      await unpublishReport(record.id);
      message.success('已取消发布');
      refresh();
    } catch (error) {
      message.error('取消发布失败');
    }
  };

  const handleDelete = async (record: ResearchReport) => {
    try {
      await deleteReport(record.id);
      message.success('删除成功');
      refresh();
    } catch (error) {
      message.error('删除失败');
    }
  };

  // 打开文档编辑弹框
  const handleEditContent = (record: ResearchReport) => {
    setContentEditReport(record);
    form.setFieldsValue({ content: record.content });
    setContentModalVisible(true);
  };

  // 保存文档内容
  const handleSaveContent = async () => {
    try {
      const values = await form.validateFields(['content']);
      setContentSubmitLoading(true);
      await updateReport(contentEditReport!.id, { content: values.content });
      message.success('文档内容已保存');
      setContentModalVisible(false);
      refresh();
    } catch (error) {
      message.error('保存失败');
    } finally {
      setContentSubmitLoading(false);
    }
  };

  const columns = [
    { title: 'ID', dataIndex: 'id', key: 'id', width: 60 },
    { title: '标题', dataIndex: 'title', key: 'title', width: 200, ellipsis: true },
    { title: '策略名称', dataIndex: 'strategy_name', key: 'strategy_name', width: 120 },
    { title: '策略类型', dataIndex: 'strategy_type', key: 'strategy_type', width: 100 },
    {
      title: '年化收益',
      dataIndex: 'annual_return',
      key: 'annual_return',
      width: 100,
      render: (v: number) => v ? `${v}%` : '-',
    },
    {
      title: '最大回撤',
      dataIndex: 'max_drawdown',
      key: 'max_drawdown',
      width: 100,
      render: (v: number) => v ? `${v}%` : '-',
    },
    {
      title: '夏普比率',
      dataIndex: 'sharpe_ratio',
      key: 'sharpe_ratio',
      width: 90,
      render: (v: number) => v || '-',
    },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 90,
      render: (v: string) => <Tag color={getStatusColor(v)}>{getStatusLabel(v)}</Tag>,
    },
    { title: '作者', dataIndex: 'author_username', key: 'author', width: 80 },
    { title: '阅读量', dataIndex: 'view_count', key: 'view_count', width: 80 },
    { title: '创建时间', dataIndex: 'created_at', key: 'created_at', width: 160 },
  ];

  const actionColumn = {
    title: '操作',
    key: 'action',
    width: 380,
    render: (_: any, record: ResearchReport) => (
      <Space size="small">
        {canEditReport(record) && (
          <Button type="link" size="small" icon={<EditOutlined />} onClick={() => handleEdit(record)}>
            编辑
          </Button>
        )}
        {canEditReport(record) && (
          <Button type="link" size="small" icon={<FileTextOutlined />} onClick={() => handleEditContent(record)}>
            文档
          </Button>
        )}
        {canSubmitForReview(record) && (
          <Button type="link" size="small" onClick={() => handleSubmitForReview(record)}>
            提交审核
          </Button>
        )}
        {canReview(record) && (
          <>
            <Button type="link" size="small" icon={<CheckOutlined />} onClick={() => handleReview(record, 'approved')}>
              通过
            </Button>
            <Button type="link" size="small" danger icon={<CloseOutlined />} onClick={() => handleReview(record, 'rejected')}>
              拒绝
            </Button>
          </>
        )}
        {canPublish(record) && (
          <Button type="link" size="small" onClick={() => handlePublish(record)}>
            发布
          </Button>
        )}
        {canUnpublish(record) && (
          <Button type="link" size="small" onClick={() => handleUnpublish(record)}>
            取消发布
          </Button>
        )}
        {canDeleteReport(record) && (
          <Popconfirm title="确定要删除吗？" onConfirm={() => handleDelete(record)}>
            <Button type="link" size="small" danger icon={<DeleteOutlined />}>
              删除
            </Button>
          </Popconfirm>
        )}
        {!canEditReport(record) && !canSubmitForReview(record) && !canReview(record) && !canPublish(record) && !canDeleteReport(record) && (
          <span style={{ color: '#999', fontSize: 12 }}>无操作权限</span>
        )}
      </Space>
    ),
  };

  return (
    <>
      <PageHeader
        title="研究报告"
        description={isSuperAdmin ? "管理所有研究报告（超管权限）" : "管理自己的研究报告"}
        actions={[
          <Button key="add" type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
            新建报告
          </Button>,
        ]}
      />
      <DataTable
        loading={tableLoading}
        data={data}
        columns={[...columns, actionColumn]}
        pagination={pagination}
        onRefresh={refresh}
      />

      {/* 添加/编辑弹窗 */}
      <Modal
        title={isEdit ? '编辑报告' : '新建报告'}
        open={modalVisible}
        onCancel={() => {
          setModalVisible(false);
          setIsEdit(false);
          setDetailImageFileList([]);
          form.resetFields();
        }}
        footer={null}
        width={1000}
        destroyOnClose
        keyboard={false}
        maskClosable={false}
      >
        <Form form={form} layout="vertical" onFinish={handleSubmit}>
          <Form.Item
            name="title"
            label="报告标题"
            rules={[{ required: true, message: '请输入报告标题' }]}
          >
            <Input placeholder="请输入报告标题" />
          </Form.Item>

          <Form.Item name="summary" label="摘要">
            <TextArea rows={2} placeholder="请输入报告摘要（可选）" />
          </Form.Item>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 16 }}>
            <Form.Item name="strategy_name" label="策略名称">
              <Input placeholder="如: 双均线策略" />
            </Form.Item>
            <Form.Item name="strategy_type" label="策略类型">
              <Select placeholder="请选择策略类型" allowClear>
                {RESEARCH_STRATEGY_TYPES.map((item) => (
                  <Option key={item.value} value={item.value}>
                    {item.label}
                  </Option>
                ))}
              </Select>
            </Form.Item>
            <Form.Item name="market" label="适用市场">
              <Input placeholder="如: A股、期货、港股" />
            </Form.Item>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 16 }}>
            <Form.Item name="annual_return" label="年化收益率 (%)">
              <InputNumber step={0.01} style={{ width: '100%' }} placeholder="如: 15.5" />
            </Form.Item>
            <Form.Item name="max_drawdown" label="最大回撤 (%)">
              <InputNumber step={0.01} style={{ width: '100%' }} placeholder="如: 10.2" />
            </Form.Item>
            <Form.Item name="sharpe_ratio" label="夏普比率">
              <InputNumber step={0.01} style={{ width: '100%' }} placeholder="如: 1.5" />
            </Form.Item>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 16 }}>
            <Form.Item name="win_rate" label="胜率 (%)">
              <InputNumber step={0.01} style={{ width: '100%' }} placeholder="如: 55.5" />
            </Form.Item>
            <Form.Item name="profit_loss_ratio" label="盈亏比">
              <InputNumber step={0.01} style={{ width: '100%' }} placeholder="如: 1.8" />
            </Form.Item>
            <Form.Item name="total_trades" label="总交易次数">
              <InputNumber min={0} style={{ width: '100%' }} placeholder="如: 500" />
            </Form.Item>
          </div>

          <MarkdownFormItem
            name="content"
            label="报告内容 (Markdown)"
            required
            height={400}
            placeholder="支持 Markdown 语法，可使用 # 标题、**加粗**、- 列表、代码块等"
          />

          <Form.Item name="detail_image" label="首页详情图" style={{ marginBottom: 16 }}>
            <Upload
              name="detail_image"
              listType="picture-card"
              maxCount={1}
              fileList={detailImageFileList}
              onChange={({ fileList }) => setDetailImageFileList(fileList)}
              beforeUpload={() => false} // 阻止自动上传
              withCredentials
              accept="image/*"
            >
              {detailImageFileList.length >= 1 ? null : (
                <div style={{ padding: 8 }}>
                  <UploadOutlined />
                  <div style={{ marginTop: 8 }}>上传</div>
                </div>
              )}
            </Upload>
          </Form.Item>

          <Form.Item name="tags" label="标签">
            <Input placeholder="多个标签用逗号分隔" />
          </Form.Item>

          <Form.Item style={{ marginBottom: 0, textAlign: 'right' }}>
            <Space>
              <Button onClick={() => setModalVisible(false)}>取消</Button>
              <Button type="primary" htmlType="submit" loading={submitLoading}>
                {isEdit ? '保存修改' : '创建报告'}
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>

      {/* 文档编辑弹框 */}
      <Modal
        title={`编辑文档 - ${contentEditReport?.title || ''}`}
        open={contentModalVisible}
        onCancel={() => {
          setContentModalVisible(false);
          form.resetFields();
        }}
        footer={null}
        width={900}
        destroyOnClose
      >
        <Form form={form} layout="vertical">
          <MarkdownFormItem
            name="content"
            label="报告内容 (Markdown)"
            required
            height={500}
            placeholder="支持 Markdown 语法，可使用 # 标题、**加粗**、- 列表、代码块等"
          />

          <Form.Item style={{ marginBottom: 0, textAlign: 'right' }}>
            <Space>
              <Button onClick={() => setContentModalVisible(false)}>取消</Button>
              <Button type="primary" onClick={handleSaveContent} loading={contentSubmitLoading}>
                保存文档
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </>
  );
};

export default Reports;
