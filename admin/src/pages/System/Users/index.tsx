import React, { useState } from 'react';
import { Modal, Form, Input, Switch, Button, message, Popconfirm } from 'antd';
import { DeleteOutlined } from '@ant-design/icons';
import PageHeader from '@/components/Common/PageHeader';
import DataTable from '@/components/Common/DataTable';
import { useTable } from '@/hooks/useTable';
import { getUsers, createUser, updateUser, deleteUser } from '@/api/users';
import { User } from '@/types';

const Users: React.FC = () => {
  const [form] = Form.useForm();
  const [modalVisible, setModalVisible] = useState(false);
  const [editingUser, setEditingUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(false);

  const { data, loading: tableLoading, pagination, refresh } = useTable<User>({
    fetchData: getUsers,
  });

  const handleAdd = () => {
    setEditingUser(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (record: User) => {
    setEditingUser(record);
    form.setFieldsValue({
      username: record.username,
      email: record.email,
      is_staff: record.is_staff,
      is_superuser: record.is_superuser,
    });
    setModalVisible(true);
  };

  const handleDelete = async (record: User) => {
    try {
      await deleteUser(record.id);
      message.success('删除成功');
      refresh();
    } catch (error) {
      message.error('删除失败');
    }
  };

  const handleSubmit = async (values: any) => {
    setLoading(true);
    try {
      if (editingUser) {
        await updateUser(editingUser.id, values);
        message.success('更新成功');
      } else {
        await createUser(values);
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
    {
      title: 'ID',
      dataIndex: 'id',
      key: 'id',
      width: 60,
    },
    {
      title: '用户名',
      dataIndex: 'username',
      key: 'username',
    },
    {
      title: '邮箱',
      dataIndex: 'email',
      key: 'email',
    },
    {
      title: '超级管理员',
      dataIndex: 'is_superuser',
      key: 'is_superuser',
      render: (value: boolean) => (value ? '是' : '否'),
    },
    {
      title: '员工',
      dataIndex: 'is_staff',
      key: 'is_staff',
      render: (value: boolean) => (value ? '是' : '否'),
    },
    {
      title: '最后登录',
      dataIndex: 'last_login',
      key: 'last_login',
      render: (value: string) => value || '从未登录',
    },
    {
      title: '加入时间',
      dataIndex: 'date_joined',
      key: 'date_joined',
    },
  ];

  return (
    <>
      <PageHeader
        title="用户管理"
        description="管理系统用户账户"
        showAddButton
        addButtonText="新增用户"
        onAdd={handleAdd}
      />

      <DataTable
        loading={tableLoading}
        data={data}
        columns={columns}
        pagination={pagination}
        onEdit={handleEdit}
        onDelete={(record) => (
          <Popconfirm
            title="确定要删除此用户吗？"
            onConfirm={() => handleDelete(record)}
            okText="确定"
            cancelText="取消"
          >
            <DeleteOutlined style={{ color: '#ff4d4f' }} />
          </Popconfirm>
        )}
      />

      <Modal
        title={editingUser ? '编辑用户' : '新增用户'}
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        footer={null}
        destroyOnClose
      >
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
          initialValues={{ is_staff: false, is_superuser: false }}
        >
          <Form.Item
            name="username"
            label="用户名"
            rules={[
              { required: true, message: '请输入用户名' },
              { min: 3, message: '用户名至少3个字符' },
            ]}
          >
            <Input placeholder="请输入用户名" />
          </Form.Item>
          {!editingUser && (
            <Form.Item
              name="password"
              label="密码"
              rules={[
                { required: true, message: '请输入密码' },
                { min: 6, message: '密码至少6个字符' },
              ]}
            >
              <Input.Password placeholder="请输入密码" />
            </Form.Item>
          )}
          <Form.Item name="email" label="邮箱">
            <Input placeholder="请输入邮箱" />
          </Form.Item>
          <Form.Item name="is_staff" label="员工权限" valuePropName="checked">
            <Switch checkedChildren="是" unCheckedChildren="否" />
          </Form.Item>
          <Form.Item name="is_superuser" label="超级管理员" valuePropName="checked">
            <Switch checkedChildren="是" unCheckedChildren="否" />
          </Form.Item>
          <Form.Item style={{ marginBottom: 0, textAlign: 'right' }}>
            <Button onClick={() => setModalVisible(false)} style={{ marginRight: 8 }}>
              取消
            </Button>
            <Button type="primary" htmlType="submit" loading={loading}>
              确定
            </Button>
          </Form.Item>
        </Form>
      </Modal>
    </>
  );
};

export default Users;
