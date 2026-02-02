import React, { useState } from 'react';
import { Button, Space, Modal, Form, Input, Select, InputNumber, message, Popconfirm, Upload, UploadFile, Badge, Dropdown } from 'antd';
import { UploadOutlined, FileTextOutlined } from '@ant-design/icons';
import { PlusOutlined, EditOutlined, DeleteOutlined, CheckOutlined, CloseOutlined, ExportOutlined } from '@ant-design/icons';
import PageHeader from '@/components/Common/PageHeader';
import DataTable from '@/components/Common/DataTable';
import { MarkdownFormItem } from '@/components/Common/MarkdownEditor';
import { useTable } from '@/hooks/useTable';
import { getReports, createReport, updateReport, deleteReport, submitReport, reviewReport, publishReport, unpublishReport, updateReportStatus } from '@/api/reports';
import { ResearchReport, RESEARCH_STRATEGY_TYPES } from '@/types';
import { useAuthStore } from '@/store/useAuthStore';

const { TextArea } = Input;
const { Option } = Select;

// 状态配置 - 带颜色和图标
const STATUS_CONFIG: Record<string, { label: string; color: string; bgColor: string; borderColor: string }> = {
  draft: { label: '草稿', color: '#666', bgColor: '#f5f5f5', borderColor: '#d9d9d9' },
  pending: { label: '待审核', color: '#1677ff', bgColor: '#e6f4ff', borderColor: '#91caff' },
  approved: { label: '已通过', color: '#52c41a', bgColor: '#f6ffed', borderColor: '#b7eb8f' },
  rejected: { label: '已拒绝', color: '#ff4d4f', bgColor: '#fff2f0', borderColor: '#ffccc7' },
  published: { label: '已发布', color: '#722ed1', bgColor: '#f9f0ff', borderColor: '#d3adf7' },
};

// 统一的标签样式
const getStatusTagStyle = (config: typeof STATUS_CONFIG[string]) => ({
  display: 'inline-flex',
  alignItems: 'center',
  gap: 4,
  padding: '4px 10px',
  borderRadius: 6,
  backgroundColor: config.bgColor,
  color: config.color,
  fontSize: 13,
  lineHeight: '20px',
  fontWeight: 500,
});

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
  // 批量选择状态
  const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([]);
  const [selectedRows, setSelectedRows] = useState<ResearchReport[]>([]);

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
    if (report.author === currentUserId && (report.status === 'draft' || report.status === 'rejected')) {
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
    return report.author === currentUserId && (report.status === 'draft' || report.status === 'rejected');
  };

  // 检查是否可以编辑状态（超管可以编辑所有，普通用户只能编辑自己的）
  const canEditStatus = (report: ResearchReport) => {
    if (isSuperAdmin) return true;
    return report.author === currentUserId;
  };

  // 编辑状态
  const handleEditStatus = async (id: number, newStatus: string) => {
    try {
      await updateReportStatus(id, { status: newStatus });
      message.success('状态更新成功');
      refresh();
    } catch (error) {
      message.error('状态更新失败');
    }
  };

  // 批量发布
  const handleBulkPublish = async () => {
    const approvedReports = selectedRows.filter(r => r.status === 'approved');
    if (approvedReports.length === 0) {
      message.warning('请选择已通过审核的报告进行发布');
      return;
    }
    try {
      for (const report of approvedReports) {
        await publishReport(report.id);
      }
      message.success(`成功发布 ${approvedReports.length} 篇报告`);
      setSelectedRowKeys([]);
      setSelectedRows([]);
      refresh();
    } catch (error) {
      message.error('批量发布失败');
    }
  };

  // 检查是否可以提交审核
  const canSubmitForReview = (report: ResearchReport) => {
    return report.author === currentUserId && report.status === 'draft';
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

    // 设置图片文件列表 - 使用 base64 数据
    if (record.detail_image) {
      setDetailImageFileList([{
        uid: '-1',
        name: 'detail_image.jpg',
        status: 'done',
        url: record.detail_image,
        // base64 数据用于显示
      }]);
    } else {
      setDetailImageFileList([]);
    }

    // 排除 detail_image，因为使用单独的状态管理
    const { detail_image, ...recordWithoutImage } = record;
    form.setFieldsValue({
      ...recordWithoutImage,
      backtest_start_date: record.backtest_start_date ? new Date(record.backtest_start_date) : null,
      backtest_end_date: record.backtest_end_date ? new Date(record.backtest_end_date) : null,
    });
    setModalVisible(true);
  };

  const handleSubmit = async (values: any) => {
    setSubmitLoading(true);
    try {
      const submitData: any = { ...values };

      // 处理图片上传
      if (detailImageFileList.length > 0) {
        const file = detailImageFileList[0];
        // 如果有新上传的文件（originFileObj），添加到提交数据中
        if (file.originFileObj) {
          submitData.detail_image = [file];
        }
        // 如果是编辑模式且没有新文件，不传递 detail_image，保留原有图片
      } else {
        // 如果没有图片，设置为 null 移除图片
        if (isEdit && currentReport) {
          submitData.detail_image = null;
        }
      }

      if (isEdit && currentReport) {
        await updateReport(currentReport.id, submitData);
        message.success('更新成功');
      } else {
        await createReport(submitData);
        message.success('创建成功');
      }
      setModalVisible(false);
      setDetailImageFileList([]);
      form.resetFields();
      // 刷新表格数据
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
      width: 130,
      render: (v: string, record: ResearchReport) => {
        const config = STATUS_CONFIG[v] || STATUS_CONFIG.draft;
        if (canEditStatus(record)) {
          const menuItems = Object.entries(STATUS_CONFIG).map(([key, cfg]) => ({
            key,
            label: (
              <div style={getStatusTagStyle(cfg)}>
                <span>{cfg.label}</span>
              </div>
            ),
          }));
          return (
            <Dropdown
              menu={{ items: menuItems, onClick: ({ key }) => handleEditStatus(record.id, key) }}
              trigger={['click']}
              placement="bottomLeft"
            >
              <Button
                size="large"
                type="text"
                style={getStatusTagStyle(config)}
              >
                {config.label}
              </Button>
            </Dropdown>
          );
        }
        return (
          <div style={getStatusTagStyle(config)}>
            <span>{config.label}</span>
          </div>
        );
      },
    },
    { title: '作者', dataIndex: 'author_username', key: 'author', width: 80 },
    { title: '阅读量', dataIndex: 'view_count', key: 'view_count', width: 80 },
    { title: '创建时间', dataIndex: 'created_at', key: 'created_at', width: 160 },
  ];

  const actionColumn = {
    title: '操作',
    key: 'action',
    width: 320,
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
          <Button
            key="bulk-publish"
            icon={<ExportOutlined />}
            onClick={handleBulkPublish}
            disabled={selectedRowKeys.length === 0}
          >
            批量发布 ({selectedRowKeys.length})
          </Button>,
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
        rowSelection={{
          selectedRowKeys,
          onChange: (keys: React.Key[], rows: ResearchReport[]) => {
            setSelectedRowKeys(keys);
            setSelectedRows(rows);
          },
        }}
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
        // destroyOnClose 已弃用，使用 closable + key 属性替代
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

          <Form.Item
            name="detail_image"
            label="首页详情图"
            style={{ marginBottom: 16 }}
          >
            <div style={{ display: 'flex', gap: 16, alignItems: 'flex-start' }}>
              {/* 图片预览区域 */}
              {detailImageFileList.length > 0 && (() => {
                const file = detailImageFileList[0];
                const previewUrl = file.url || (file.originFileObj ? URL.createObjectURL(file.originFileObj) : null);
                if (!previewUrl) return null;
                return (
                  <div style={{
                    width: 104,
                    height: 104,
                    border: '1px dashed #d9d9d9',
                    borderRadius: 8,
                    overflow: 'hidden',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    background: '#fafafa',
                  }}>
                    <img
                      src={previewUrl}
                      alt="Preview"
                      style={{ maxWidth: '100%', maxHeight: '100%', objectFit: 'contain' }}
                    />
                  </div>
                );
              })()}
              {/* 上传按钮 */}
              <Upload
                name="detail_image"
                listType="picture-card"
                maxCount={1}
                fileList={detailImageFileList}
                onChange={({ fileList }) => {
                  setDetailImageFileList(fileList);
                }}
                beforeUpload={() => false}
                withCredentials
                accept="image/*"
                showUploadList={false}
              >
                {detailImageFileList.length >= 1 ? null : (
                  <div style={{ padding: 8 }}>
                    <UploadOutlined />
                    <div style={{ marginTop: 8 }}>上传</div>
                  </div>
                )}
              </Upload>
              {/* 移除图片按钮 */}
              {detailImageFileList.length > 0 && (
                <Button
                  type="text"
                  danger
                  size="small"
                  onClick={() => setDetailImageFileList([])}
                >
                  移除
                </Button>
              )}
            </div>
          </Form.Item>

          <Form.Item name="tags" label="标签">
            <Input placeholder="多个标签用逗号分隔" />
          </Form.Item>

          {/* 状态编辑 - 仅超管可编辑 */}
          {isSuperAdmin && (
            <Form.Item name="status" label="状态">
              <Select placeholder="请选择状态">
                {Object.entries(STATUS_CONFIG).map(([key, cfg]) => (
                  <Option key={key} value={key}>
                    <div style={getStatusTagStyle(cfg)}>
                      <Badge color={cfg.color} />
                      <span>{cfg.label}</span>
                    </div>
                  </Option>
                ))}
              </Select>
            </Form.Item>
          )}

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
        // destroyOnClose 已弃用，使用 closable + key 属性替代
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
