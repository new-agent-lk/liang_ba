import React, { useState } from 'react';
import { Modal, Form, Input, Button, message } from 'antd';
import PageHeader from '@/components/Common/PageHeader';
import DataTable from '@/components/Common/DataTable';
import { useTable } from '@/hooks/useTable';
import { getCases, createCase, updateCase, deleteCase } from '@/api/content';
import { Case } from '@/types';

const { TextArea } = Input;

const Cases: React.FC = () => {
  const [form] = Form.useForm();
  const [modalVisible, setModalVisible] = useState(false);
  const [editingCase, setEditingCase] = useState<Case | null>(null);
  const [loading, setLoading] = useState(false);

  const { data, loading: tableLoading, pagination, refresh } = useTable<Case>({
    fetchData: getCases,
  });

  const handleAdd = () => {
    setEditingCase(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (record: Case) => {
    setEditingCase(record);
    form.setFieldsValue({
      title: record.title,
      category: record.category,
      digest: record.digest,
      info: record.info,
    });
    setModalVisible(true);
  };

  const handleDelete = async (record: Case) => {
    try {
      await deleteCase(record.id);
      message.success('删除成功');
      refresh();
    } catch (error) {
      message.error('删除失败');
    }
  };

  const handleSubmit = async (values: any) => {
    setLoading(true);
    try {
      const formData = new FormData();
      formData.append('title', values.title);
      formData.append('category', values.category || 'trxf');
      formData.append('digest', values.digest || '');
      formData.append('info', values.info);

      if (editingCase) {
        await updateCase(editingCase.id, formData);
        message.success('更新成功');
      } else {
        await createCase(formData);
        message.success('创建成功');
      }
      setModalVisible(false);
      refresh();
    } catch (error) {
      message.error('操作失败');
    } finally {
      setLoading(false);
    }
  };

  const columns = [
    { title: 'ID', dataIndex: 'id', key: 'id', width: 60 },
    { title: '标题', dataIndex: 'title', key: 'title' },
    { title: '分类', dataIndex: 'category_display', key: 'category_display', width: 100 },
    { title: '摘要', dataIndex: 'digest', key: 'digest', ellipsis: true },
    { title: '人气', dataIndex: 'click_nums', key: 'click_nums', width: 80 },
  ];

  return (
    <>
      <PageHeader title="案例管理" description="管理成功案例" showAddButton addButtonText="新增案例" onAdd={handleAdd} />
      <DataTable loading={tableLoading} data={data} columns={columns} pagination={pagination} onEdit={handleEdit} onDelete={handleDelete} />
      <Modal title={editingCase ? '编辑案例' : '新增案例'} open={modalVisible} onCancel={() => setModalVisible(false)} footer={null} width={800} destroyOnClose>
        <Form form={form} layout="vertical" onFinish={handleSubmit}>
          <Form.Item name="title" label="标题" rules={[{ required: true, message: '请输入标题' }]}>
            <Input placeholder="请输入案例标题" />
          </Form.Item>
          <Form.Item name="category" label="分类">
            <Input placeholder="请输入分类代码 (trxf/wszl/shlj)" />
          </Form.Item>
          <Form.Item name="digest" label="摘要">
            <TextArea rows={2} placeholder="请输入案例摘要" />
          </Form.Item>
          <Form.Item name="info" label="内容" rules={[{ required: true, message: '请输入内容' }]}>
            <TextArea rows={10} placeholder="请输入案例内容" />
          </Form.Item>
          <Form.Item style={{ marginBottom: 0, textAlign: 'right' }}>
            <Button onClick={() => setModalVisible(false)} style={{ marginRight: 8 }}>取消</Button>
            <Button type="primary" htmlType="submit" loading={loading}>确定</Button>
          </Form.Item>
        </Form>
      </Modal>
    </>
  );
};

export default Cases;
