import React, { useState } from "react";
import {
  Button,
  Form,
  Input,
  InputNumber,
  Modal,
  Popconfirm,
  Select,
  Space,
  Upload,
  UploadFile,
  message,
} from "antd";
import {
  CheckOutlined,
  CloseOutlined,
  DeleteOutlined,
  EditOutlined,
  ExportOutlined,
  FileTextOutlined,
  FormOutlined,
} from "@ant-design/icons";
import { useNavigate } from "react-router-dom";
import PageHeader from "@/components/Common/PageHeader";
import DataTable from "@/components/Common/DataTable";
import { MarkdownFormItem } from "@/components/Common/MarkdownEditor";
import { useTable } from "@/hooks/useTable";
import {
  deleteReport,
  getReports,
  publishReport,
  reviewReport,
  submitReport,
  unpublishReport,
  updateReport,
} from "@/api/reports";
import { ResearchReport, RESEARCH_STRATEGY_TYPES } from "@/types";
import { useAuthStore } from "@/store/useAuthStore";
import { hasCapability } from "@/utils/access";

const { TextArea } = Input;
const { Option } = Select;

const STATUS_CONFIG: Record<
  string,
  { label: string; color: string; bgColor: string }
> = {
  draft: { label: "草稿", color: "#666", bgColor: "#f5f5f5" },
  pending: { label: "待审核", color: "#1677ff", bgColor: "#e6f4ff" },
  approved: { label: "已通过", color: "#52c41a", bgColor: "#f6ffed" },
  rejected: { label: "已拒绝", color: "#ff4d4f", bgColor: "#fff2f0" },
  published: { label: "已发布", color: "#722ed1", bgColor: "#f9f0ff" },
};

const getStatusTagStyle = (config: (typeof STATUS_CONFIG)[string]) => ({
  display: "inline-flex",
  alignItems: "center",
  gap: 4,
  padding: "4px 10px",
  borderRadius: 6,
  backgroundColor: config.bgColor,
  color: config.color,
  fontSize: 13,
  lineHeight: "20px",
  fontWeight: 500,
});

const ReportsManage: React.FC = () => {
  const navigate = useNavigate();
  const [form] = Form.useForm();
  const [modalVisible, setModalVisible] = useState(false);
  const [currentReport, setCurrentReport] = useState<ResearchReport | null>(
    null,
  );
  const [submitLoading, setSubmitLoading] = useState(false);
  const [detailImageFileList, setDetailImageFileList] = useState<UploadFile[]>(
    [],
  );
  const [contentModalVisible, setContentModalVisible] = useState(false);
  const [contentEditReport, setContentEditReport] =
    useState<ResearchReport | null>(null);
  const [contentSubmitLoading, setContentSubmitLoading] = useState(false);
  const [selectedRowKeys, setSelectedRowKeys] = useState<React.Key[]>([]);
  const [selectedRows, setSelectedRows] = useState<ResearchReport[]>([]);

  const { user } = useAuthStore();
  const currentUserId = user?.id;
  const canManageAllReports = hasCapability(user, "reports.manage_all");
  const canReviewReports = hasCapability(user, "reports.review");
  const canPublishReports = hasCapability(user, "reports.publish");

  const { data, loading, pagination, refresh } = useTable<ResearchReport>({
    fetchData: getReports,
  });

  const canEditReport = (report: ResearchReport) => {
    if (canManageAllReports) {
      return true;
    }
    return (
      report.author === currentUserId &&
      (report.status === "draft" || report.status === "rejected")
    );
  };

  const canDeleteReport = (report: ResearchReport) => {
    if (canManageAllReports) {
      return report.status === "draft" || report.status === "rejected";
    }
    return (
      report.author === currentUserId &&
      (report.status === "draft" || report.status === "rejected")
    );
  };

  const canSubmitForReview = (report: ResearchReport) => {
    if (report.status !== "draft" && report.status !== "rejected") {
      return false;
    }
    return report.author === currentUserId || canManageAllReports;
  };

  const canReview = (report: ResearchReport) => {
    return canReviewReports && report.status === "pending";
  };

  const canPublish = (report: ResearchReport) => {
    return canPublishReports && report.status === "approved";
  };

  const canUnpublish = (report: ResearchReport) => {
    return canPublishReports && report.status === "published";
  };

  const handleGoWrite = () => {
    navigate("/research/reports/write");
  };

  const handleEdit = (record: ResearchReport) => {
    setCurrentReport(record);
    if (record.detail_image) {
      setDetailImageFileList([
        {
          uid: "-1",
          name: "detail_image.jpg",
          status: "done",
          url: record.detail_image,
        },
      ]);
    } else {
      setDetailImageFileList([]);
    }

    const { detail_image, ...recordWithoutImage } = record;
    form.setFieldsValue({
      ...recordWithoutImage,
      backtest_start_date: record.backtest_start_date
        ? new Date(record.backtest_start_date)
        : null,
      backtest_end_date: record.backtest_end_date
        ? new Date(record.backtest_end_date)
        : null,
    });
    setModalVisible(true);
  };

  const handleSubmit = async (values: Partial<ResearchReport>) => {
    if (!currentReport) {
      return;
    }

    setSubmitLoading(true);
    try {
      const submitData: Record<string, unknown> = { ...values };
      if (detailImageFileList.length > 0) {
        const file = detailImageFileList[0];
        if (file.originFileObj) {
          submitData.detail_image = [file];
        }
      } else {
        submitData.detail_image = null;
      }

      await updateReport(
        currentReport.id,
        submitData as Partial<ResearchReport>,
      );
      message.success("更新成功");
      setModalVisible(false);
      setCurrentReport(null);
      setDetailImageFileList([]);
      form.resetFields();
      refresh();
    } catch {
      message.error("更新失败");
    } finally {
      setSubmitLoading(false);
    }
  };

  const handleDelete = async (record: ResearchReport) => {
    try {
      await deleteReport(record.id);
      message.success("删除成功");
      refresh();
    } catch {
      message.error("删除失败");
    }
  };

  const handleSubmitForReview = async (record: ResearchReport) => {
    try {
      await submitReport(record.id);
      message.success("已提交审核");
      refresh();
    } catch {
      message.error("提交失败");
    }
  };

  const handleReview = async (
    record: ResearchReport,
    status: "approved" | "rejected",
  ) => {
    try {
      await reviewReport(record.id, { status, review_notes: "" });
      message.success(status === "approved" ? "审核通过" : "已拒绝");
      refresh();
    } catch {
      message.error("审核失败");
    }
  };

  const handlePublish = async (record: ResearchReport) => {
    try {
      await publishReport(record.id);
      message.success("已发布");
      refresh();
    } catch {
      message.error("发布失败");
    }
  };

  const handleUnpublish = async (record: ResearchReport) => {
    try {
      await unpublishReport(record.id);
      message.success("已取消发布");
      refresh();
    } catch {
      message.error("取消发布失败");
    }
  };

  const handleEditContent = (record: ResearchReport) => {
    setContentEditReport(record);
    form.setFieldsValue({ content: record.content });
    setContentModalVisible(true);
  };

  const handleSaveContent = async () => {
    if (!contentEditReport) {
      return;
    }

    try {
      const values = await form.validateFields(["content"]);
      setContentSubmitLoading(true);
      await updateReport(contentEditReport.id, { content: values.content });
      message.success("文档内容已保存");
      setContentModalVisible(false);
      refresh();
    } catch {
      message.error("保存失败");
    } finally {
      setContentSubmitLoading(false);
    }
  };

  const handleBulkPublish = async () => {
    const approvedReports = selectedRows.filter(
      (item) => item.status === "approved",
    );
    if (approvedReports.length === 0) {
      message.warning("请选择已通过审核的报告进行发布");
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
    } catch {
      message.error("批量发布失败");
    }
  };

  const columns = [
    { title: "ID", dataIndex: "id", key: "id", width: 60 },
    {
      title: "标题",
      dataIndex: "title",
      key: "title",
      width: 200,
      ellipsis: true,
    },
    {
      title: "策略名称",
      dataIndex: "strategy_name",
      key: "strategy_name",
      width: 120,
    },
    {
      title: "策略类型",
      dataIndex: "strategy_type",
      key: "strategy_type",
      width: 100,
    },
    {
      title: "年化收益",
      dataIndex: "annual_return",
      key: "annual_return",
      width: 100,
      render: (value: number) => (value ? `${value}%` : "-"),
    },
    {
      title: "最大回撤",
      dataIndex: "max_drawdown",
      key: "max_drawdown",
      width: 100,
      render: (value: number) => (value ? `${value}%` : "-"),
    },
    {
      title: "夏普比率",
      dataIndex: "sharpe_ratio",
      key: "sharpe_ratio",
      width: 90,
      render: (value: number) => value || "-",
    },
    {
      title: "状态",
      dataIndex: "status",
      key: "status",
      width: 130,
      render: (value: string) => {
        const config = STATUS_CONFIG[value] || STATUS_CONFIG.draft;
        return (
          <div style={getStatusTagStyle(config)}>
            <span>{config.label}</span>
          </div>
        );
      },
    },
    { title: "作者", dataIndex: "author_username", key: "author", width: 80 },
    { title: "阅读量", dataIndex: "view_count", key: "view_count", width: 80 },
    {
      title: "创建时间",
      dataIndex: "created_at",
      key: "created_at",
      width: 160,
    },
  ];

  const actionColumn = {
    title: "操作",
    key: "action",
    width: 320,
    render: (_: unknown, record: ResearchReport) => (
      <Space size="small">
        {canEditReport(record) && (
          <Button
            type="link"
            size="small"
            icon={<EditOutlined />}
            onClick={() => handleEdit(record)}
          >
            编辑
          </Button>
        )}
        {canEditReport(record) && (
          <Button
            type="link"
            size="small"
            icon={<FileTextOutlined />}
            onClick={() => handleEditContent(record)}
          >
            文档
          </Button>
        )}
        {canSubmitForReview(record) && (
          <Button
            type="link"
            size="small"
            onClick={() => handleSubmitForReview(record)}
          >
            提交审核
          </Button>
        )}
        {canReview(record) && (
          <>
            <Button
              type="link"
              size="small"
              icon={<CheckOutlined />}
              onClick={() => handleReview(record, "approved")}
            >
              通过
            </Button>
            <Button
              type="link"
              size="small"
              danger
              icon={<CloseOutlined />}
              onClick={() => handleReview(record, "rejected")}
            >
              拒绝
            </Button>
          </>
        )}
        {canPublish(record) && (
          <Button
            type="link"
            size="small"
            onClick={() => handlePublish(record)}
          >
            发布
          </Button>
        )}
        {canUnpublish(record) && (
          <Button
            type="link"
            size="small"
            onClick={() => handleUnpublish(record)}
          >
            取消发布
          </Button>
        )}
        {canDeleteReport(record) && (
          <Popconfirm
            title="确定要删除吗？"
            onConfirm={() => handleDelete(record)}
          >
            <Button type="link" size="small" danger icon={<DeleteOutlined />}>
              删除
            </Button>
          </Popconfirm>
        )}
      </Space>
    ),
  };

  return (
    <>
      <PageHeader
        title="报告管理"
        description={
          canManageAllReports
            ? "管理全部研究报告并执行审核发布"
            : "管理自己的研究报告"
        }
        actions={[
          <Button key="write" icon={<FormOutlined />} onClick={handleGoWrite}>
            去做撰写
          </Button>,
          ...(canPublishReports
            ? [
                <Button
                  key="bulk-publish"
                  icon={<ExportOutlined />}
                  onClick={handleBulkPublish}
                  disabled={selectedRowKeys.length === 0}
                >
                  批量发布 ({selectedRowKeys.length})
                </Button>,
              ]
            : []),
        ]}
      />

      <DataTable
        loading={loading}
        data={data}
        columns={[...columns, actionColumn]}
        pagination={pagination}
        onRefresh={refresh}
        rowSelection={
          canPublishReports
            ? {
                selectedRowKeys,
                onChange: (keys: React.Key[], rows: ResearchReport[]) => {
                  setSelectedRowKeys(keys);
                  setSelectedRows(rows);
                },
              }
            : undefined
        }
      />

      <Modal
        title="编辑报告"
        open={modalVisible}
        onCancel={() => {
          setModalVisible(false);
          setCurrentReport(null);
          setDetailImageFileList([]);
          form.resetFields();
        }}
        footer={null}
        width={1000}
        keyboard={false}
        maskClosable={false}
      >
        <Form form={form} layout="vertical" onFinish={handleSubmit}>
          <Form.Item
            name="title"
            label="报告标题"
            rules={[{ required: true, message: "请输入报告标题" }]}
          >
            <Input placeholder="请输入报告标题" />
          </Form.Item>

          <Form.Item name="summary" label="摘要">
            <TextArea rows={2} placeholder="请输入报告摘要（可选）" />
          </Form.Item>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr 1fr",
              gap: 16,
            }}
          >
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

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr 1fr",
              gap: 16,
            }}
          >
            <Form.Item name="annual_return" label="年化收益率 (%)">
              <InputNumber
                step={0.01}
                style={{ width: "100%" }}
                placeholder="如: 15.5"
              />
            </Form.Item>
            <Form.Item name="max_drawdown" label="最大回撤 (%)">
              <InputNumber
                step={0.01}
                style={{ width: "100%" }}
                placeholder="如: 10.2"
              />
            </Form.Item>
            <Form.Item name="sharpe_ratio" label="夏普比率">
              <InputNumber
                step={0.01}
                style={{ width: "100%" }}
                placeholder="如: 1.5"
              />
            </Form.Item>
          </div>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr 1fr",
              gap: 16,
            }}
          >
            <Form.Item name="win_rate" label="胜率 (%)">
              <InputNumber
                step={0.01}
                style={{ width: "100%" }}
                placeholder="如: 55.5"
              />
            </Form.Item>
            <Form.Item name="profit_loss_ratio" label="盈亏比">
              <InputNumber
                step={0.01}
                style={{ width: "100%" }}
                placeholder="如: 1.8"
              />
            </Form.Item>
            <Form.Item name="total_trades" label="总交易次数">
              <InputNumber
                min={0}
                style={{ width: "100%" }}
                placeholder="如: 500"
              />
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
            <div style={{ display: "flex", gap: 16, alignItems: "flex-start" }}>
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
                  <div style={{ padding: 8 }}>上传</div>
                )}
              </Upload>
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

          <Form.Item style={{ marginBottom: 0, textAlign: "right" }}>
            <Space>
              <Button onClick={() => setModalVisible(false)}>取消</Button>
              <Button type="primary" htmlType="submit" loading={submitLoading}>
                保存修改
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>

      <Modal
        title={`编辑文档 - ${contentEditReport?.title || ""}`}
        open={contentModalVisible}
        onCancel={() => {
          setContentModalVisible(false);
          form.resetFields();
        }}
        footer={null}
        width={900}
      >
        <Form form={form} layout="vertical">
          <MarkdownFormItem
            name="content"
            label="报告内容 (Markdown)"
            required
            height={500}
            placeholder="支持 Markdown 语法，可使用 # 标题、**加粗**、- 列表、代码块等"
          />

          <Form.Item style={{ marginBottom: 0, textAlign: "right" }}>
            <Space>
              <Button onClick={() => setContentModalVisible(false)}>
                取消
              </Button>
              <Button
                type="primary"
                onClick={handleSaveContent}
                loading={contentSubmitLoading}
              >
                保存文档
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </>
  );
};

export default ReportsManage;
