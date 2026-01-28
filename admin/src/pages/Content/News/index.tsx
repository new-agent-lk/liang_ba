import React, { useState } from 'react';
import { Modal, Form, Input, Button, message } from 'antd';
import PageHeader from '@/components/Common/PageHeader';
import DataTable from '@/components/Common/DataTable';
import { useTable } from '@/hooks/useTable';
import { getNewsList, createNews, updateNews, deleteNews } from '@/api/content';
import { News } from '@/types';

const { TextArea } = Input;

const NewsManagement: React.FC = () => {
  const [form] = Form.useForm();
  const [modalVisible, setModalVisible] = useState(false);
  const [editingNews, setEditingNews] = useState<News | null>(null);
  const [loading, setLoading] = useState(false);

  const { data, loading: tableLoading, pagination, refresh } = useTable<News>({
    fetchData: getNewsList,
  });

  const handleAdd = () => {
    setEditingNews(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (record: News) => {
    setEditingNews(record);
    form.setFieldsValue({
      title: record.title,
      category: record.category,
      digest: record.digest,
      info: record.info,
    });
    setModalVisible(true);
  };

  const handleDelete = async (record: News) => {
    try {
      await deleteNews(record.id);
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
      formData.append('category', values.category || 'gsxw');
      formData.append('digest', values.digest || '');
      formData.append('info', values.info);

      if (editingNews) {
        await updateNews(editingNews.id, formData);
        message.success('更新成功');
      } else {
        await createNews(formData);
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
    { title: '标题', dataIndex: 'title', key: 'title', ellipsis: true },
    { title: '分类', dataIndex: 'category_display', key: 'category_display', width: 100 },
    { title: '摘要', dataIndex: 'digest', key: 'digest', ellipsis: true },
    { title: '人气', dataIndex: 'click_nums', key: 'click_nums', width: 80 },
  ];

  return (
    <>
      <PageHeader title="新闻管理" description="管理公司新闻资讯" showAddButton addButtonText="发布新闻" onAdd={handleAdd} />
      <DataTable loading={tableLoading} data={data} columns={columns} pagination={pagination} onEdit={handleEdit} onDelete={handleDelete} />
      <Modal title={editingNews ? '编辑新闻' : '发布新闻'} open={modalVisible} onCancel={() => setModalVisible(false)} footer={null} width={800} destroyOnClose>
        <Form form={form} layout="vertical" onFinish={handleSubmit}>
          <Form.Item name="title" label="标题" rules={[{ required: true, message: '请输入标题' }]}>
            <Input placeholder="请输入新闻标题" />
          </Form.Item>
          <Form.Item name="category" label="分类">
            <Input placeholder="请输入分类代码 (gsxw/mtbd/yggh)" />
          </Form.Item>
          <Form.Item name="digest" label="摘要">
            <TextArea rows={2} placeholder="请输入新闻摘要" />
          </Form.Item>
          <Form.Item name="info" label="内容" rules={[{ required: true, message: '请输入内容' }]}>
            <TextArea rows={10} placeholder="请输入新闻内容" />
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

export default NewsManagement;
