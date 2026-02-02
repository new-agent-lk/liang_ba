import React, { useState } from 'react';
import { Modal, Form, Input, Select, InputNumber, Button, message, Space, Dropdown, Tag } from 'antd';
import { CheckOutlined, PlusOutlined } from '@ant-design/icons';
import PageHeader from '@/components/Common/PageHeader';
import DataTable from '@/components/Common/DataTable';
import { useTable } from '@/hooks/useTable';
import { getJobs, getJob, deleteJob, createJob, updateJob, updateJobStatus, patchJob } from '@/api/jobs';
import { JobPosition, JOB_STATUS_CHOICES, JOB_CATEGORY_CHOICES, RECRUITMENT_TYPE_CHOICES } from '@/types';

const { TextArea } = Input;
const { Option } = Select;

// 状态配置
const JOB_STATUS_CONFIG: Record<string, { label: string; color: string; bgColor: string; borderColor: string }> = {
  draft: { label: '草稿', color: '#666', bgColor: '#f5f5f5', borderColor: '#d9d9d9' },
  active: { label: '招聘中', color: '#1677ff', bgColor: '#e6f4ff', borderColor: '#91caff' },
  paused: { label: '暂停招聘', color: '#faad14', bgColor: '#fffbe6', borderColor: '#ffe58f' },
  closed: { label: '已关闭', color: '#999', bgColor: '#f5f5f5', borderColor: '#d9d9d9' },
};

// 部门配置
const DEPARTMENT_CONFIG: Record<string, { label: string; color: string; bgColor: string; borderColor: string }> = {
  '量化部': { label: '量化部', color: '#722ed1', bgColor: '#f9f0ff', borderColor: '#d3adf7' },
  '风控部': { label: '风控部', color: '#13c2c2', bgColor: '#e6fffb', borderColor: '#87e8de' },
  '技术部': { label: '技术部', color: '#52c41a', bgColor: '#f6ffed', borderColor: '#b7eb8f' },
  '研究部': { label: '研究部', color: '#fa8c16', bgColor: '#fff7e6', borderColor: '#ffd591' },
};

// 统一的标签样式
const getJobStatusTagStyle = (config: typeof JOB_STATUS_CONFIG[string]) => ({
  display: 'inline-flex',
  alignItems: 'center',
  gap: 4,
  padding: '4px 10px',
  borderRadius: 6,
  backgroundColor: config.bgColor,
  border: '1px solid ' + config.borderColor,
  color: config.color,
  fontSize: 13,
  lineHeight: '20px',
  fontWeight: 500,
});

const getDeptTagStyle = (config: typeof DEPARTMENT_CONFIG[string]) => ({
  display: 'inline-flex',
  alignItems: 'center',
  gap: 4,
  padding: '4px 10px',
  borderRadius: 6,
  backgroundColor: config.bgColor,
  border: '1px solid ' + config.borderColor,
  color: config.color,
  fontSize: 13,
  lineHeight: '20px',
  fontWeight: 500,
});

// 部门选项列表
const DEPARTMENT_ITEMS = Object.entries(DEPARTMENT_CONFIG).map(([key, cfg]) => ({
  key,
  label: <div style={getDeptTagStyle(cfg)}><span>{cfg.label}</span></div>,
}));

// 职位类别选项列表（带样式）
const CATEGORY_ITEMS = JOB_CATEGORY_CHOICES.map(item => ({
  key: item.value,
  label: (
    <div style={{
      display: 'inline-flex',
      alignItems: 'center',
      gap: 4,
      padding: '4px 10px',
      borderRadius: 6,
      backgroundColor: '#f5f5f5',
      border: '1px solid #d9d9d9',
      color: '#666',
      fontSize: 13,
      lineHeight: '20px',
      fontWeight: 500,
    }}>
      <span>{item.label}</span>
    </div>
  ),
}));

// 招聘类型选项列表（带样式）
const RECRUITMENT_TYPE_ITEMS = RECRUITMENT_TYPE_CHOICES.map(item => ({
  key: item.value,
  label: (
    <div style={{
      display: 'inline-flex',
      alignItems: 'center',
      gap: 4,
      padding: '4px 10px',
      borderRadius: 6,
      backgroundColor: '#f0f5ff',
      border: '1px solid #adc6ff',
      color: '#2f54eb',
      fontSize: 13,
      lineHeight: '20px',
      fontWeight: 500,
    }}>
      <span>{item.label}</span>
    </div>
  ),
}));

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
      form.setFieldsValue(jobData);
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

  const handleEditStatus = async (id: number, newStatus: string) => {
    try {
      await updateJobStatus(id, { status: newStatus });
      message.success('状态更新成功');
      refresh();
    } catch (error) {
      message.error('状态更新失败');
    }
  };

  const handleEditDepartment = async (id: number, newDepartment: string) => {
    try {
      await patchJob(id, { department: newDepartment });
      message.success('部门更新成功');
      refresh();
    } catch (error) {
      message.error('部门更新失败');
    }
  };

  const handleEditCategory = async (id: number, newCategory: string) => {
    try {
      await patchJob(id, { category: newCategory });
      message.success('职位类别更新成功');
      refresh();
    } catch (error) {
      message.error('职位类别更新失败');
    }
  };

  const handleEditRecruitmentType = async (id: number, newType: string) => {
    try {
      await patchJob(id, { recruitment_type: newType });
      message.success('招聘类型更新成功');
      refresh();
    } catch (error) {
      message.error('招聘类型更新失败');
    }
  };

  const columns = [
    { title: 'ID', dataIndex: 'id', key: 'id', width: 60 },
    { title: '职位名称', dataIndex: 'title', key: 'title', width: 150 },
    {
      title: '部门',
      dataIndex: 'department',
      key: 'department',
      width: 120,
      render: (v: string, record: JobPosition) => {
        const config = DEPARTMENT_CONFIG[v] || { label: v || '-', color: '#666', bgColor: '#f5f5f5', borderColor: '#d9d9d9' };
        return (
          <Dropdown
            menu={{ items: DEPARTMENT_ITEMS, onClick: ({ key }) => handleEditDepartment(record.id, key) }}
            trigger={['click']}
            placement="bottomLeft"
          >
            <Button
              size="large"
              type="text"
              style={getDeptTagStyle(config)}
            >
              {config.label}
            </Button>
          </Dropdown>
        );
      },
    },
    {
      title: '职位类别',
      dataIndex: 'category_display',
      key: 'category',
      width: 120,
      render: (v: string, record: JobPosition) => {
        const categoryItem = JOB_CATEGORY_CHOICES.find(item => item.value === record.category);
        const label = categoryItem?.label || v || '-';
        return (
          <Dropdown
            menu={{ items: CATEGORY_ITEMS, onClick: ({ key }) => handleEditCategory(record.id, key) }}
            trigger={['click']}
            placement="bottomLeft"
          >
            <Button
              size="large"
              type="text"
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: 4,
                padding: '4px 10px',
                borderRadius: 6,
                backgroundColor: '#f5f5f5',
                border: '1px solid #d9d9d9',
                color: '#666',
                fontSize: 13,
                lineHeight: '20px',
                fontWeight: 500,
              }}
            >
              {label}
            </Button>
          </Dropdown>
        );
      },
    },
    {
      title: '招聘类型',
      dataIndex: 'recruitment_type_display',
      key: 'recruitment_type',
      width: 120,
      render: (v: string, record: JobPosition) => {
        const typeItem = RECRUITMENT_TYPE_CHOICES.find(item => item.value === record.recruitment_type);
        const label = typeItem?.label || v || '-';
        return (
          <Dropdown
            menu={{ items: RECRUITMENT_TYPE_ITEMS, onClick: ({ key }) => handleEditRecruitmentType(record.id, key) }}
            trigger={['click']}
            placement="bottomLeft"
          >
            <Button
              size="large"
              type="text"
              style={{
                display: 'inline-flex',
                alignItems: 'center',
                gap: 4,
                padding: '4px 10px',
                borderRadius: 6,
                backgroundColor: '#f0f5ff',
                border: '1px solid #adc6ff',
                color: '#2f54eb',
                fontSize: 13,
                lineHeight: '20px',
                fontWeight: 500,
              }}
            >
              {label}
            </Button>
          </Dropdown>
        );
      },
    },
    { title: '工作地点', dataIndex: 'location', key: 'location', width: 120, ellipsis: true },
    { title: '薪资范围', dataIndex: 'salary_range', key: 'salary', width: 100 },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 120,
      render: (v: string, record: JobPosition) => {
        const config = JOB_STATUS_CONFIG[v] || JOB_STATUS_CONFIG.draft;
        const menuItems = Object.entries(JOB_STATUS_CONFIG).map(([key, cfg]) => ({
          key,
          label: (
            <div style={getJobStatusTagStyle(cfg)}>
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
              style={getJobStatusTagStyle(config)}
            >
              {config.label}
            </Button>
          </Dropdown>
        );
      },
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
        onRefresh={refresh}
        onEdit={handleEdit}
        onDelete={handleDelete}
        onChange={(_pagination, _filters, _sorter: any) => {
          // 处理分页变化
          pagination.onChange(_pagination.current || 1, _pagination.pageSize || 10);
        }}
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
              name="category"
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

            <Form.Item
              name="recruitment_type"
              label="招聘类型"
              rules={[{ required: true, message: '请选择招聘类型' }]}
            >
              <Select placeholder="请选择招聘类型">
                {RECRUITMENT_TYPE_CHOICES.map((item) => (
                  <Option key={item.value} value={item.value}>
                    {item.label}
                  </Option>
                ))}
              </Select>
            </Form.Item>

            <Form.Item name="location" label="工作地点">
              <Input placeholder="如: 北京/上海" />
            </Form.Item>

            <Form.Item name="salary_range" label="薪资范围">
              <Input placeholder="如: 20K-40K" />
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
