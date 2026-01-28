import React, { useState, useEffect } from 'react';
import { Modal, Form, Input, Select, Button, message } from 'antd';
import PageHeader from '@/components/Common/PageHeader';
import DataTable from '@/components/Common/DataTable';
import { useTable } from '@/hooks/useTable';
import { getProducts, createProduct, updateProduct, deleteProduct, getProductCategories } from '@/api/content';
import { Product, ProductCategory } from '@/types';

const { TextArea } = Input;

const Products: React.FC = () => {
  const [form] = Form.useForm();
  const [modalVisible, setModalVisible] = useState(false);
  const [editingProduct, setEditingProduct] = useState<Product | null>(null);
  const [loading, setLoading] = useState(false);
  const [categories, setCategories] = useState<ProductCategory[]>([]);

  const { data, loading: tableLoading, pagination, refresh } = useTable<Product>({
    fetchData: getProducts,
  });

  useEffect(() => {
    fetchCategories();
  }, []);

  const fetchCategories = async () => {
    try {
      const data = await getProductCategories();
      setCategories(data);
    } catch (error) {
      console.error('Failed to fetch categories:', error);
    }
  };

  const handleAdd = () => {
    setEditingProduct(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (record: Product) => {
    setEditingProduct(record);
    form.setFieldsValue({
      name: record.name,
      category: record.category,
      info: record.info,
    });
    setModalVisible(true);
  };

  const handleDelete = async (record: Product) => {
    try {
      await deleteProduct(record.id);
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
      formData.append('name', values.name);
      if (values.category) {
        formData.append('category', values.category.toString());
      }
      formData.append('info', values.info || '');

      if (editingProduct) {
        await updateProduct(editingProduct.id, formData);
        message.success('更新成功');
      } else {
        await createProduct(formData);
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
    { title: '产品名称', dataIndex: 'name', key: 'name' },
    { title: '分类', dataIndex: 'category_name', key: 'category_name' },
    { title: '人气', dataIndex: 'click_nums', key: 'click_nums', width: 80 },
  ];

  return (
    <>
      <PageHeader title="产品管理" description="管理产品信息" showAddButton addButtonText="新增产品" onAdd={handleAdd} />
      <DataTable loading={tableLoading} data={data} columns={columns} pagination={pagination} onEdit={handleEdit} onDelete={handleDelete} />
      <Modal title={editingProduct ? '编辑产品' : '新增产品'} open={modalVisible} onCancel={() => setModalVisible(false)} footer={null} width={800} destroyOnClose>
        <Form form={form} layout="vertical" onFinish={handleSubmit}>
          <Form.Item name="name" label="产品名称" rules={[{ required: true, message: '请输入产品名称' }]}>
            <Input placeholder="请输入产品名称" />
          </Form.Item>
          <Form.Item name="category" label="产品分类">
            <Select placeholder="请选择分类" allowClear options={categories.map(cat => ({ label: cat.name, value: cat.id }))} />
          </Form.Item>
          <Form.Item name="info" label="产品内容">
            <TextArea rows={5} placeholder="请输入产品详情" />
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

export default Products;
