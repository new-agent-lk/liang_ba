import React, { useState } from "react";
import { Modal, Form, Input, Select, Button, message, Tag, Space } from "antd";
import {
  CheckOutlined,
  EyeOutlined,
  FileTextOutlined,
} from "@ant-design/icons";
import PageHeader from "@/components/Common/PageHeader";
import DataTable from "@/components/Common/DataTable";
import { useTable } from "@/hooks/useTable";
import {
  getResumes,
  deleteResume,
  reviewResume,
  getResumeStatusLabel,
} from "@/api/jobs";
import { Resume, RESUME_STATUS_CHOICES } from "@/types";

const { TextArea } = Input;
const { Option } = Select;

const Resumes: React.FC = () => {
  const [form] = Form.useForm();
  const [modalVisible, setModalVisible] = useState(false);
  const [detailVisible, setDetailVisible] = useState(false);
  const [currentResume, setCurrentResume] = useState<Resume | null>(null);
  const [loading, setLoading] = useState(false);

  const {
    data,
    loading: tableLoading,
    pagination,
    refresh,
  } = useTable<Resume>({
    fetchData: getResumes,
  });

  const handleReview = (record: Resume) => {
    setCurrentResume(record);
    form.setFieldsValue({
      status: record.status,
      review_notes: record.review_notes || "",
    });
    setModalVisible(true);
  };

  const handleView = (record: Resume) => {
    setCurrentResume(record);
    setDetailVisible(true);
  };

  const handleDelete = async (record: Resume) => {
    try {
      await deleteResume(record.id);
      message.success("删除成功");
      refresh();
    } catch (error) {
      message.error("删除失败");
    }
  };

  const handleSubmit = async (values: any) => {
    if (!currentResume) return;

    setLoading(true);
    try {
      await reviewResume(currentResume.id, {
        status: values.status,
        review_notes: values.review_notes,
      });
      message.success("审核成功");
      setModalVisible(false);
      setCurrentResume(null);
      form.resetFields();
      refresh();
    } catch (error) {
      message.error("审核失败");
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    const found = RESUME_STATUS_CHOICES.find((item) => item.value === status);
    return found?.color || "default";
  };

  const columns = [
    { title: "ID", dataIndex: "id", key: "id", width: 60 },
    { title: "姓名", dataIndex: "name", key: "name", width: 80 },
    {
      title: "应聘职位",
      dataIndex: "job_category_display",
      key: "job_category",
      width: 100,
    },
    { title: "联系电话", dataIndex: "phone", key: "phone", width: 120 },
    {
      title: "邮箱",
      dataIndex: "email",
      key: "email",
      width: 150,
      ellipsis: true,
    },
    {
      title: "学历",
      dataIndex: "education_display",
      key: "education",
      width: 80,
    },
    {
      title: "毕业院校",
      dataIndex: "school",
      key: "school",
      width: 120,
      ellipsis: true,
    },
    {
      title: "状态",
      dataIndex: "status",
      key: "status",
      width: 90,
      render: (v: string) => (
        <Tag color={getStatusColor(v)}>{getResumeStatusLabel(v)}</Tag>
      ),
    },
    {
      title: "简历",
      dataIndex: "resume_file_url",
      key: "resume_file",
      width: 80,
      render: (url: string | undefined) =>
        url ? (
          <Button
            type="link"
            size="small"
            icon={<FileTextOutlined />}
            onClick={(e) => {
              e.stopPropagation();
              window.open(url, "_blank");
            }}
          >
            查看
          </Button>
        ) : (
          <span style={{ color: "#999" }}>-</span>
        ),
    },
    {
      title: "提交时间",
      dataIndex: "created_at",
      key: "created_at",
      width: 160,
    },
  ];

  return (
    <>
      <PageHeader title="简历管理" description="管理求职者提交的简历" />
      <DataTable
        loading={tableLoading}
        data={data}
        columns={columns}
        pagination={pagination}
        onRefresh={refresh}
        onView={handleView}
        onEdit={handleReview}
        onDelete={handleDelete}
      />

      {/* 查看详情弹窗 */}
      <Modal
        title="简历详情"
        open={detailVisible}
        onCancel={() => setDetailVisible(false)}
        footer={null}
        width={800}
        destroyOnClose
      >
        {currentResume && (
          <div>
            <div style={{ marginBottom: 16 }}>
              <Space>
                <span>
                  姓名: <strong>{currentResume.name}</strong>
                </span>
                <span style={{ marginLeft: 16 }}>
                  电话: {currentResume.phone}
                </span>
                <span style={{ marginLeft: 16 }}>
                  邮箱: {currentResume.email}
                </span>
              </Space>
            </div>

            <div style={{ marginBottom: 16 }}>
              <Space>
                <Tag color="blue">{currentResume.job_category_display}</Tag>
                <Tag>{currentResume.education_display}</Tag>
                <Tag color={getStatusColor(currentResume.status)}>
                  {getResumeStatusLabel(currentResume.status)}
                </Tag>
              </Space>
            </div>

            <div
              style={{
                background: "#f5f5f5",
                padding: 16,
                borderRadius: 4,
                marginBottom: 16,
              }}
            >
              <h4>基本信息</h4>
              <p>
                <strong>期望职位:</strong> {currentResume.job_category_display}
              </p>
              <p>
                <strong>期望薪资:</strong>{" "}
                {currentResume.expected_salary || "面议"}
              </p>
              <p>
                <strong>学历:</strong> {currentResume.education_display}
              </p>
              <p>
                <strong>毕业院校:</strong> {currentResume.school || "-"}
              </p>
              <p>
                <strong>专业:</strong> {currentResume.major || "-"}
              </p>
            </div>

            {currentResume.work_experience && (
              <div
                style={{
                  background: "#f5f5f5",
                  padding: 16,
                  borderRadius: 4,
                  marginBottom: 16,
                }}
              >
                <h4>工作经历</h4>
                <p>{currentResume.work_experience}</p>
              </div>
            )}

            {currentResume.skills && (
              <div
                style={{
                  background: "#f5f5f5",
                  padding: 16,
                  borderRadius: 4,
                  marginBottom: 16,
                }}
              >
                <h4>专业技能</h4>
                <p>{currentResume.skills}</p>
              </div>
            )}

            {currentResume.self_introduction && (
              <div
                style={{
                  background: "#f5f5f5",
                  padding: 16,
                  borderRadius: 4,
                  marginBottom: 16,
                }}
              >
                <h4>自我介绍</h4>
                <p>{currentResume.self_introduction}</p>
              </div>
            )}

            {currentResume.resume_file_url && (
              <div style={{ marginTop: 16 }}>
                <Button
                  type="primary"
                  icon={<EyeOutlined />}
                  onClick={() =>
                    window.open(currentResume.resume_file_url, "_blank")
                  }
                >
                  查看附件简历
                </Button>
              </div>
            )}
          </div>
        )}
      </Modal>

      {/* 审核弹窗 */}
      <Modal
        title="审核简历"
        open={modalVisible}
        onCancel={() => {
          setModalVisible(false);
          form.resetFields();
        }}
        footer={null}
        width={500}
        destroyOnClose
      >
        <Form form={form} layout="vertical" onFinish={handleSubmit}>
          <Form.Item
            name="status"
            label="审核结果"
            rules={[{ required: true, message: "请选择审核结果" }]}
          >
            <Select placeholder="请选择审核结果">
              {RESUME_STATUS_CHOICES.filter((s) => s.value !== "pending").map(
                (item) => (
                  <Option key={item.value} value={item.value}>
                    <Tag color={item.color}>{item.label}</Tag>
                  </Option>
                ),
              )}
            </Select>
          </Form.Item>

          <Form.Item name="review_notes" label="审核备注">
            <TextArea rows={4} placeholder="请输入审核备注（可选）" />
          </Form.Item>

          <Form.Item style={{ marginBottom: 0, textAlign: "right" }}>
            <Button
              onClick={() => {
                setModalVisible(false);
                form.resetFields();
              }}
              style={{ marginRight: 8 }}
            >
              取消
            </Button>
            <Button
              type="primary"
              htmlType="submit"
              loading={loading}
              icon={<CheckOutlined />}
            >
              提交审核
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </>
  );
};

export default Resumes;
