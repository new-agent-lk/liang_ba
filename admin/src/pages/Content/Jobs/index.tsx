import React, { useState } from 'react';
import { Modal, Form, Input, Select, InputNumber, Button, message, Tag, Space } from 'antd';
import { CheckOutlined, PlusOutlined } from '@ant-design/icons';
import PageHeader from '@/components/Common/PageHeader';
import DataTable from '@/components/Common/DataTable';
import { useTable } from '@/hooks/useTable';
import { getJobs, getJob, deleteJob, createJob, updateJob, getJobStatusLabel } from '@/api/jobs';
import { JobPosition, JOB_STATUS_CHOICES, JOB_CATEGORY_CHOICES, EDUCATION_CHOICES } from '@/types';

const { TextArea } = Input;
const { Option } = Select;

const Jobs: React.FC = () => {
  const [form] = Form.useForm();
  const [modalVisible, setModalVisible] = useState(false);
  const [isEdit, setIsEdit] = useState(false);
  const [currentJob, setCurrentJob] = useState<JobPosition | null>(null);
  const [submitLoading, setSubmitLoading] = useState(false);

  const { data, loading: tableLoading, pagination, refresh } = useTable<JobPosition>({
    fetchData: getJobs,
    deleteData: deleteJob,
  });

  const handleAdd = () => {
    setCurrentJob(null);
    setIsEdit(false);
    form.resetFields();
    form.setFieldsValue({ status: 'draft', headcount: 1, sort_order: 0 });
    setModalVisible(true);
  };

  const handleEdit = async (record: JobPosition) => {
    try {
      const jobData = await getJob(record.id);
      setCurrentJob(jobData);
      setIsEdit(true);
      form.setFieldsValue({
        ...jobData,
        salary_min: jobData.salary_min || undefined,
        salary_max: jobData.salary_max || undefined,
      });
      setModalVisible(true);
    } catch (error) {
      message.error('获取职位信息失败');
    }
  };

  const handleDelete = async (record: JobPosition) => {
    try {
      await deleteJob(record.id);
      message.success('删除成功');
      refresh();
    } catch (error) {
      message.error('删除失败');
    }
  };

  const handleSubmit = async (values: any) => {
    setSubmitLoading(true);
    try {
      if (isEdit && currentJob) {
        await updateJob(currentJob.id, values);
        message.success('更新成功');
      } else {
        await createJob(values);
        message.success('创建成功');
      }
      setModalVisible(false);
      form.resetFields();
      refresh();
    } catch (error) {
      message.error(isEdit ? '更新失败' : '创建失败');
    } finally {
      setSubmitLoading(false);
    }
  };

  const getStatusColor = (status: string) => {
    const found = JOB_STATUS_CHOICES.find((item) => item.value === status);
    return found?.color || 'default';
  };

  const columns = [
    { title: 'ID', dataIndex: 'id', key: 'id', width: 60 },
    { title: '职位名称', dataIndex: 'title', key: 'title', width: 150 },
    { title: '部门', dataIndex: 'department', key: 'department', width: 100 },
    { title: '职位类别', dataIndex: 'job_category_display', key: 'job_category', width: 100 },
    { title: '工作地点', dataIndex: 'location', key: 'location', width: 120, ellipsis: true },
    { title: '招聘人数', dataIndex: 'headcount', key: 'headcount', width: 80 },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 90,
      render: (v: string) => <Tag color={getStatusColor(v)}>{getJobStatusLabel(v)}</Tag>,
    },
    { title: '排序', dataIndex: 'sort_order', key: 'sort_order', width: 60 },
    { title: '创建时间', dataIndex: 'created_at', key: 'created_at', width: 160 },
  ];

  return (
    <>
      <PageHeader
        title="职位管理"
        description="管理招聘职位信息"
        actions={[
          <Button key="add" type="primary" icon={<PlusOutlined />} onClick={handleAdd}>
            添加职位
          </Button>,
        ]}
      />
      <DataTable
        loading={tableLoading}
        data={data}
        columns={columns}
        pagination={pagination}
        onEdit={handleEdit}
        onDelete={handleDelete}
      />

      {/* 添加/编辑弹窗 */}
      <Modal
        title={isEdit ? '编辑职位' : '添加职位'}
        open={modalVisible}
        onCancel={() => {
          setModalVisible(false);
          setIsEdit(false);
          form.resetFields();
        }}
        footer={null}
        width={700}
        destroyOnClose
      >
        <Form form={form} layout="vertical" onFinish={handleSubmit}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 16 }}>
            <Form.Item
              name="title"
              label="职位名称"
              rules={[{ required: true, message: '请输入职位名称' }]}
            >
              <Input placeholder="如: 量化开发工程师" />
            </Form.Item>

            <Form.Item name="department" label="部门">
              <Input placeholder="如: 量化部" />
            </Form.Item>

            <Form.Item
              name="job_category"
              label="职位类别"
              rules={[{ required: true, message: '请选择职位类别' }]}
            >
              <Select placeholder="请选择职位类别">
                {JOB_CATEGORY_CHOICES.map((item) => (
                  <Option key={item.value} value={item.value}>
                    {item.label}
                  </Option>
                ))}
              </Select>
            </Form.Item>

            <Form.Item name="location" label="工作地点">
              <Input placeholder="如: 北京/上海" />
            </Form.Item>

            <Form.Item name="salary_display" label="薪资显示">
              <Input placeholder="如: 20K-40K" />
            </Form.Item>

            <Form.Item name="headcount" label="招聘人数">
              <InputNumber min={1} max={100} style={{ width: '100%' }} />
            </Form.Item>

            <Form.Item name="experience" label="经验要求">
              <Input placeholder="如: 3年以上相关经验" />
            </Form.Item>

            <Form.Item name="education_required" label="学历要求">
              <Select placeholder="请选择学历要求" allowClear>
                {EDUCATION_CHOICES.map((item) => (
                  <Option key={item.value} value={item.value}>
                    {item.label}
                  </Option>
                ))}
              </Select>
            </Form.Item>

            <Form.Item name="sort_order" label="排序">
              <InputNumber min={0} style={{ width: '100%' }} />
            </Form.Item>

            <Form.Item
              name="status"
              label="状态"
              rules={[{ required: true, message: '请选择状态' }]}
            >
              <Select placeholder="请选择状态">
                {JOB_STATUS_CHOICES.map((item) => (
                  <Option key={item.value} value={item.value}>
                    <Tag color={item.color}>{item.label}</Tag>
                  </Option>
                ))}
              </Select>
            </Form.Item>
          </div>

          <Form.Item
            name="description"
            label="职位描述"
            rules={[{ required: true, message: '请输入职位描述' }]}
          >
            <TextArea rows={4} placeholder="请输入职位描述" />
          </Form.Item>

          <Form.Item
            name="requirements"
            label="任职要求"
            rules={[{ required: true, message: '请输入任职要求' }]}
          >
            <TextArea rows={4} placeholder="请输入任职要求" />
          </Form.Item>

          <Form.Item name="responsibilities" label="工作职责">
            <TextArea rows={3} placeholder="请输入工作职责（可选）" />
          </Form.Item>

          <Form.Item style={{ marginBottom: 0, textAlign: 'right' }}>
            <Space>
              <Button
                onClick={() => {
                  setModalVisible(false);
                  setIsEdit(false);
                  form.resetFields();
                }}
              >
                取消
              </Button>
              <Button type="primary" htmlType="submit" loading={submitLoading} icon={<CheckOutlined />}>
                {isEdit ? '保存修改' : '创建职位'}
              </Button>
            </Space>
          </Form.Item>
        </Form>
      </Modal>
    </>
  );
};

export default Jobs;
