import React, { useState } from 'react';
import { Modal, Form, Input, Button, message } from 'antd';
import PageHeader from '@/components/Common/PageHeader';
import DataTable from '@/components/Common/DataTable';
import { useTable } from '@/hooks/useTable';
import { getCarousels, createCarousel, updateCarousel, deleteCarousel } from '@/api/content';

interface Carousel {
  id: number;
  title: string;
  img?: string;
  img_url?: string;
  link?: string;
}

const Carousels: React.FC = () => {
  const [form] = Form.useForm();
  const [modalVisible, setModalVisible] = useState(false);
  const [editingCarousel, setEditingCarousel] = useState<Carousel | null>(null);
  const [loading, setLoading] = useState(false);

  const { data, loading: tableLoading, pagination, refresh } = useTable<Carousel>({
    fetchData: getCarousels,
  });

  const handleAdd = () => {
    setEditingCarousel(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (record: Carousel) => {
    setEditingCarousel(record);
    form.setFieldsValue({
      title: record.title,
      link: record.link,
    });
    setModalVisible(true);
  };

  const handleDelete = async (record: Carousel) => {
    try {
      await deleteCarousel(record.id);
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
      formData.append('link', values.link || '');

      if (editingCarousel) {
        await updateCarousel(editingCarousel.id, formData);
        message.success('更新成功');
      } else {
        await createCarousel(formData);
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
    { title: '链接', dataIndex: 'link', key: 'link', ellipsis: true },
  ];

  return (
    <>
      <PageHeader title="轮播图管理" description="管理首页轮播图" showAddButton addButtonText="新增轮播图" onAdd={handleAdd} />
      <DataTable loading={tableLoading} data={data} columns={columns} pagination={pagination} onEdit={handleEdit} onDelete={handleDelete} />
      <Modal title={editingCarousel ? '编辑轮播图' : '新增轮播图'} open={modalVisible} onCancel={() => setModalVisible(false)} footer={null} width={600} destroyOnClose>
        <Form form={form} layout="vertical" onFinish={handleSubmit}>
          <Form.Item name="title" label="标题" rules={[{ required: true, message: '请输入标题' }]}>
            <Input placeholder="请输入轮播图标题" />
          </Form.Item>
          <Form.Item name="link" label="链接地址">
            <Input placeholder="请输入跳转链接" />
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

export default Carousels;
