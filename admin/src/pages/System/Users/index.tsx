import React, { useState } from "react";
import {
  Modal,
  Form,
  Input,
  Switch,
  Button,
  message,
  Popconfirm,
  Tabs,
  Select,
} from "antd";
import { DeleteOutlined } from "@ant-design/icons";
import PageHeader from "@/components/Common/PageHeader";
import DataTable from "@/components/Common/DataTable";
import { useTable } from "@/hooks/useTable";
import { getUsers, createUser, updateUser, deleteUser } from "@/api/users";
import {
  User,
  DEPARTMENT_CHOICES,
  POSITION_CHOICES,
  GENDER_CHOICES,
} from "@/types";

const { Option } = Select;
const { TabPane } = Tabs;

const Users: React.FC = () => {
  const [form] = Form.useForm();
  const [profileForm] = Form.useForm();
  const [modalVisible, setModalVisible] = useState(false);
  const [editingUser, setEditingUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(false);

  const {
    data,
    loading: tableLoading,
    pagination,
    refresh,
  } = useTable<User>({
    fetchData: getUsers,
  });

  const handleAdd = () => {
    setEditingUser(null);
    form.resetFields();
    profileForm.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (record: User) => {
    setEditingUser(record);
    form.setFieldsValue({
      username: record.username,
      email: record.email,
      first_name: record.first_name,
      last_name: record.last_name,
      is_staff: record.is_staff,
      is_superuser: record.is_superuser,
      is_active: record.is_active,
    });
    if (record.profile) {
      profileForm.setFieldsValue({
        phone: record.profile.phone,
        gender: record.profile.gender,
        birthday: record.profile.birthday
          ? new Date(record.profile.birthday)
          : null,
        department: record.profile.department,
        position: record.profile.position,
        employee_id: record.profile.employee_id,
        bio: record.profile.bio,
        wechat: record.profile.wechat,
        qq: record.profile.qq,
      });
    }
    setModalVisible(true);
  };

  const handleDelete = async (record: User) => {
    try {
      await deleteUser(record.id);
      message.success("删除成功");
      refresh();
    } catch (error) {
      message.error("删除失败");
    }
  };

  const handleSubmit = async () => {
    try {
      const basicValues = await form.validateFields();
      const profileValues = await profileForm.validateFields();

      setLoading(true);

      const submitData = {
        ...basicValues,
        profile: profileValues,
      };

      if (editingUser) {
        await updateUser(editingUser.id, submitData);
        message.success("更新成功");
      } else {
        await createUser(submitData);
        message.success("创建成功");
      }
      setModalVisible(false);
      refresh();
    } catch (error) {
      message.error("操作失败");
    } finally {
      setLoading(false);
    }
  };

  const columns = [
    {
      title: "ID",
      dataIndex: "id",
      key: "id",
      width: 60,
    },
    {
      title: "用户名",
      dataIndex: "username",
      key: "username",
      width: 120,
    },
    {
      title: "姓名",
      dataIndex: "full_name",
      key: "full_name",
      width: 100,
      render: (_: any, record: User) =>
        record.first_name || record.last_name
          ? `${record.first_name || ""} ${record.last_name || ""}`.trim()
          : "-",
    },
    {
      title: "部门",
      dataIndex: ["profile", "department"],
      key: "department",
      width: 100,
      render: (value: string) => {
        const dept = DEPARTMENT_CHOICES.find((d) => d.value === value);
        return dept?.label || value || "-";
      },
    },
    {
      title: "职位",
      dataIndex: ["profile", "position"],
      key: "position",
      width: 100,
      render: (value: string) => {
        const pos = POSITION_CHOICES.find((p) => p.value === value);
        return pos?.label || value || "-";
      },
    },
    {
      title: "邮箱",
      dataIndex: "email",
      key: "email",
      width: 180,
    },
    {
      title: "超级管理员",
      dataIndex: "is_superuser",
      key: "is_superuser",
      width: 100,
      render: (value: boolean) => (
        <span style={{ color: value ? "#52c41a" : "#999" }}>
          {value ? "是" : "否"}
        </span>
      ),
    },
    {
      title: "员工",
      dataIndex: "is_staff",
      key: "is_staff",
      width: 80,
      render: (value: boolean) => (value ? "是" : "否"),
    },
    {
      title: "状态",
      dataIndex: "is_active",
      key: "is_active",
      width: 80,
      render: (value: boolean) => (
        <span style={{ color: value ? "#52c41a" : "#ff4d4f" }}>
          {value ? "启用" : "禁用"}
        </span>
      ),
    },
    {
      title: "加入时间",
      dataIndex: "date_joined",
      key: "date_joined",
      width: 120,
    },
  ];

  return (
    <>
      <PageHeader
        title="用户管理"
        description="管理系统用户账户和个人信息"
        showAddButton
        addButtonText="新增用户"
        onAdd={handleAdd}
      />

      <DataTable
        loading={tableLoading}
        data={data}
        columns={columns}
        pagination={pagination}
        onRefresh={refresh}
        onEdit={handleEdit}
        onDelete={(record) => (
          <Popconfirm
            title="确定要删除此用户吗？"
            onConfirm={() => handleDelete(record)}
            okText="确定"
            cancelText="取消"
          >
            <DeleteOutlined style={{ color: "#ff4d4f" }} />
          </Popconfirm>
        )}
      />

      <Modal
        title={editingUser ? "编辑用户" : "新增用户"}
        open={modalVisible}
        onCancel={() => setModalVisible(false)}
        footer={null}
        destroyOnClose
        width={700}
      >
        <Tabs defaultActiveKey="basic" onChange={() => {}}>
          <TabPane tab="基本信息" key="basic">
            <Form
              form={form}
              layout="vertical"
              initialValues={{
                is_staff: false,
                is_superuser: true,
                is_active: true,
              }}
            >
              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "1fr 1fr",
                  gap: 16,
                }}
              >
                <Form.Item
                  name="username"
                  label="用户名"
                  rules={[
                    { required: true, message: "请输入用户名" },
                    { min: 3, message: "用户名至少3个字符" },
                  ]}
                >
                  <Input placeholder="请输入用户名" />
                </Form.Item>
                <Form.Item
                  name="email"
                  label="邮箱"
                  rules={[{ type: "email", message: "请输入有效的邮箱" }]}
                >
                  <Input placeholder="请输入邮箱" />
                </Form.Item>
              </div>

              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "1fr 1fr",
                  gap: 16,
                }}
              >
                <Form.Item name="first_name" label="名">
                  <Input placeholder="请输入名" />
                </Form.Item>
                <Form.Item name="last_name" label="姓">
                  <Input placeholder="请输入姓" />
                </Form.Item>
              </div>

              {!editingUser && (
                <Form.Item
                  name="password"
                  label="密码"
                  rules={[
                    { required: true, message: "请输入密码" },
                    { min: 6, message: "密码至少6个字符" },
                  ]}
                >
                  <Input.Password placeholder="请输入密码" />
                </Form.Item>
              )}

              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "1fr 1fr 1fr",
                  gap: 16,
                }}
              >
                <Form.Item
                  name="is_staff"
                  label="员工权限"
                  valuePropName="checked"
                >
                  <Switch checkedChildren="是" unCheckedChildren="否" />
                </Form.Item>
                <Form.Item
                  name="is_superuser"
                  label="超级管理员"
                  valuePropName="checked"
                >
                  <Switch checkedChildren="是" unCheckedChildren="否" />
                </Form.Item>
                <Form.Item
                  name="is_active"
                  label="账户状态"
                  valuePropName="checked"
                >
                  <Switch checkedChildren="启用" unCheckedChildren="禁用" />
                </Form.Item>
              </div>
            </Form>
          </TabPane>

          <TabPane tab="个人信息" key="profile">
            <Form form={profileForm} layout="vertical">
              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "1fr 1fr",
                  gap: 16,
                }}
              >
                <Form.Item name="phone" label="联系电话">
                  <Input placeholder="请输入联系电话" />
                </Form.Item>
                <Form.Item name="gender" label="性别">
                  <Select placeholder="请选择性别" allowClear>
                    {GENDER_CHOICES.map((item) => (
                      <Option key={item.value} value={item.value}>
                        {item.label}
                      </Option>
                    ))}
                  </Select>
                </Form.Item>
              </div>

              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "1fr 1fr",
                  gap: 16,
                }}
              >
                <Form.Item name="department" label="部门">
                  <Select placeholder="请选择部门" allowClear>
                    {DEPARTMENT_CHOICES.map((item) => (
                      <Option key={item.value} value={item.value}>
                        {item.label}
                      </Option>
                    ))}
                  </Select>
                </Form.Item>
                <Form.Item name="position" label="职位">
                  <Select placeholder="请选择职位" allowClear>
                    {POSITION_CHOICES.map((item) => (
                      <Option key={item.value} value={item.value}>
                        {item.label}
                      </Option>
                    ))}
                  </Select>
                </Form.Item>
              </div>

              <Form.Item name="employee_id" label="员工ID">
                <Input placeholder="请输入员工ID" />
              </Form.Item>

              <Form.Item name="bio" label="个人简介">
                <Input.TextArea rows={3} placeholder="请输入个人简介" />
              </Form.Item>

              <div
                style={{
                  display: "grid",
                  gridTemplateColumns: "1fr 1fr",
                  gap: 16,
                }}
              >
                <Form.Item name="wechat" label="微信号">
                  <Input placeholder="请输入微信号" />
                </Form.Item>
                <Form.Item name="qq" label="QQ号">
                  <Input placeholder="请输入QQ号" />
                </Form.Item>
              </div>
            </Form>
          </TabPane>
        </Tabs>

        <div
          style={{
            textAlign: "right",
            marginTop: 16,
            borderTop: "1px solid #f0f0f0",
            paddingTop: 16,
          }}
        >
          <Button
            onClick={() => setModalVisible(false)}
            style={{ marginRight: 8 }}
          >
            取消
          </Button>
          <Button type="primary" onClick={handleSubmit} loading={loading}>
            确定
          </Button>
        </div>
      </Modal>
    </>
  );
};

export default Users;
