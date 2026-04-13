import React, { useEffect, useState } from "react";
import { Button, Card, Form, Input, Select, message } from "antd";
import PageHeader from "@/components/Common/PageHeader";
import { updateCurrentUser } from "@/api/auth";
import {
  DEPARTMENT_CHOICES,
  GENDER_CHOICES,
  POSITION_CHOICES,
  USER_CATEGORY_CHOICES,
} from "@/types";
import { useAuthStore } from "@/store/useAuthStore";

const Profile: React.FC = () => {
  const [form] = Form.useForm();
  const user = useAuthStore((state) => state.user);
  const setUser = useAuthStore((state) => state.setUser);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!user) {
      return;
    }
    form.setFieldsValue({
      first_name: user.first_name,
      last_name: user.last_name,
      email: user.email,
      profile: {
        phone: user.profile?.phone,
        user_category: user.profile?.user_category,
        gender: user.profile?.gender,
        department: user.profile?.department,
        position: user.profile?.position,
        employee_id: user.profile?.employee_id,
        wechat: user.profile?.wechat,
        qq: user.profile?.qq,
        linkedin: user.profile?.linkedin,
        bio: user.profile?.bio,
      },
    });
  }, [form, user]);

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      setLoading(true);
      const response = await updateCurrentUser(values);
      setUser(response);
      message.success("个人信息已更新");
    } catch (error) {
      message.error("保存失败");
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <PageHeader
        title="个人中心"
        description="维护当前登录账号的个人资料和联系方式"
      />
      <Card bordered={false}>
        <Form form={form} layout="vertical">
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

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr",
              gap: 16,
            }}
          >
            <Form.Item name="email" label="邮箱">
              <Input placeholder="请输入邮箱" />
            </Form.Item>
            <Form.Item name={["profile", "phone"]} label="联系电话">
              <Input placeholder="请输入联系电话" />
            </Form.Item>
          </div>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr 1fr",
              gap: 16,
            }}
          >
            <Form.Item name={["profile", "user_category"]} label="用户类型">
              <Select disabled>
                {USER_CATEGORY_CHOICES.map((item) => (
                  <Select.Option key={item.value} value={item.value}>
                    {item.label}
                  </Select.Option>
                ))}
              </Select>
            </Form.Item>
            <Form.Item name={["profile", "gender"]} label="性别">
              <Select allowClear placeholder="请选择性别">
                {GENDER_CHOICES.map((item) => (
                  <Select.Option key={item.value} value={item.value}>
                    {item.label}
                  </Select.Option>
                ))}
              </Select>
            </Form.Item>
            <Form.Item name={["profile", "employee_id"]} label="员工编号">
              <Input placeholder="请输入员工编号" />
            </Form.Item>
          </div>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr",
              gap: 16,
            }}
          >
            <Form.Item name={["profile", "department"]} label="部门">
              <Select allowClear placeholder="请选择部门">
                {DEPARTMENT_CHOICES.map((item) => (
                  <Select.Option key={item.value} value={item.value}>
                    {item.label}
                  </Select.Option>
                ))}
              </Select>
            </Form.Item>
            <Form.Item name={["profile", "position"]} label="职位">
              <Select allowClear placeholder="请选择职位">
                {POSITION_CHOICES.map((item) => (
                  <Select.Option key={item.value} value={item.value}>
                    {item.label}
                  </Select.Option>
                ))}
              </Select>
            </Form.Item>
          </div>

          <div
            style={{
              display: "grid",
              gridTemplateColumns: "1fr 1fr 1fr",
              gap: 16,
            }}
          >
            <Form.Item name={["profile", "wechat"]} label="微信号">
              <Input placeholder="请输入微信号" />
            </Form.Item>
            <Form.Item name={["profile", "qq"]} label="QQ号">
              <Input placeholder="请输入QQ号" />
            </Form.Item>
            <Form.Item name={["profile", "linkedin"]} label="LinkedIn">
              <Input placeholder="请输入 LinkedIn 链接" />
            </Form.Item>
          </div>

          <Form.Item name={["profile", "bio"]} label="个人简介">
            <Input.TextArea rows={4} placeholder="请输入个人简介" />
          </Form.Item>

          <Button type="primary" onClick={handleSubmit} loading={loading}>
            保存资料
          </Button>
        </Form>
      </Card>
    </>
  );
};

export default Profile;
