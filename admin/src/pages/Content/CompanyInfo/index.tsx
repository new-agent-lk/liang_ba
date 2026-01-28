import React, { useEffect, useState } from 'react';
import { Form, Input, Button, Card, Typography, Upload, message, Row, Col, Spin } from 'antd';
import { UploadOutlined, InboxOutlined } from '@ant-design/icons';
import type { UploadFile, UploadProps } from 'antd';
import { getCompanyInfo, updateCompanyInfo } from '@/api/company';
import { CompanyInfo } from '@/types';

const { Title, Text } = Typography;
const { TextArea } = Input;

const CompanyInfoPage: React.FC = () => {
  const [form] = Form.useForm();
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [companyInfo, setCompanyInfo] = useState<CompanyInfo | null>(null);

  // 图片上传状态
  const [logoFileList, setLogoFileList] = useState<UploadFile[]>([]);
  const [qrcodeFileList, setQrcodeFileList] = useState<UploadFile[]>([]);
  const [topimgFileList, setTopimgFileList] = useState<UploadFile[]>([]);

  useEffect(() => {
    fetchCompanyInfo();
  }, []);

  const fetchCompanyInfo = async () => {
    try {
      const data = await getCompanyInfo();
      setCompanyInfo(data);
      form.setFieldsValue(data);
      
      // 设置图片预览
      if (data.logo_url) {
        setLogoFileList([{
          uid: '-1',
          name: 'logo.png',
          status: 'done',
          url: data.logo_url,
        }]);
      }
      if (data.qrcode_url) {
        setQrcodeFileList([{
          uid: '-1',
          name: 'qrcode.png',
          status: 'done',
          url: data.qrcode_url,
        }]);
      }
      if (data.topimg_url) {
        setTopimgFileList([{
          uid: '-1',
          name: 'topimg.png',
          status: 'done',
          url: data.topimg_url,
        }]);
      }
    } catch (error) {
      message.error('获取公司信息失败');
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (values: any) => {
    setSubmitting(true);
    try {
      const formData = new FormData();
      
      // 添加文本字段
      Object.keys(values).forEach(key => {
        if (values[key] !== undefined && values[key] !== null && !['logo', 'qrcode', 'topimg'].includes(key)) {
          formData.append(key, values[key]);
        }
      });

      // 添加图片文件
      if (logoFileList.length > 0 && logoFileList[0].originFileObj) {
        formData.append('logo', logoFileList[0].originFileObj);
      }
      if (qrcodeFileList.length > 0 && qrcodeFileList[0].originFileObj) {
        formData.append('qrcode', qrcodeFileList[0].originFileObj);
      }
      if (topimgFileList.length > 0 && topimgFileList[0].originFileObj) {
        formData.append('topimg', topimgFileList[0].originFileObj);
      }

      await updateCompanyInfo(formData);
      message.success('公司信息更新成功');
      fetchCompanyInfo();
    } catch (error) {
      message.error('更新公司信息失败');
    } finally {
      setSubmitting(false);
    }
  };

  const uploadProps = (fileList: UploadFile[], setFileList: (files: UploadFile[]) => void): UploadProps => ({
    listType: 'picture-card' as const,
    fileList,
    maxCount: 1,
    beforeUpload: () => false,
    onChange: ({ fileList: newFileList }: { fileList: UploadFile[] }) => {
      setFileList(newFileList);
    },
  });

  if (loading) {
    return (
      <div style={{ textAlign: 'center', padding: 100 }}>
        <Spin size="large" />
      </div>
    );
  }

  return (
    <div>
      <Title level={4} style={{ margin: 24 }}>
        公司信息管理
      </Title>

      <Card style={{ margin: 24 }}>
        <Form
          form={form}
          layout="vertical"
          onFinish={handleSubmit}
          initialValues={companyInfo || undefined}
        >
          <Row gutter={24}>
            <Col span={24}>
              <Title level={5}>基本信息</Title>
            </Col>
          </Row>

          <Row gutter={24}>
            <Col xs={24} md={12}>
              <Form.Item
                label="公司名称"
                name="name"
                rules={[{ required: true, message: '请输入公司名称' }]}
              >
                <Input placeholder="请输入公司名称" />
              </Form.Item>
            </Col>
            <Col xs={24} md={12}>
              <Form.Item
                label="联系人"
                name="linkman"
                rules={[{ required: true, message: '请输入联系人' }]}
              >
                <Input placeholder="请输入联系人" />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={24}>
            <Col xs={24} md={12}>
              <Form.Item
                label="联系电话"
                name="telephone"
                rules={[{ required: true, message: '请输入联系电话' }]}
              >
                <Input placeholder="请输入联系电话" />
              </Form.Item>
            </Col>
            <Col xs={24} md={12}>
              <Form.Item
                label="电话"
                name="phone"
                rules={[{ required: true, message: '请输入电话' }]}
              >
                <Input placeholder="请输入电话" />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={24}>
            <Col xs={24} md={12}>
              <Form.Item
                label="传真"
                name="fax"
              >
                <Input placeholder="请输入传真" />
              </Form.Item>
            </Col>
            <Col xs={24} md={12}>
              <Form.Item
                label="邮箱"
                name="email"
                rules={[{ required: true, type: 'email', message: '请输入有效的邮箱地址' }]}
              >
                <Input placeholder="请输入邮箱" />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={24}>
            <Col xs={24} md={12}>
              <Form.Item
                label="邮编"
                name="postcode"
              >
                <Input placeholder="请输入邮编" />
              </Form.Item>
            </Col>
            <Col xs={24} md={12}>
              <Form.Item
                label="微信号"
                name="weichat"
              >
                <Input placeholder="请输入微信号" />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={24}>
            <Col xs={24} md={12}>
              <Form.Item
                label="客服QQ"
                name="qq"
              >
                <Input placeholder="请输入客服QQ" />
              </Form.Item>
            </Col>
            <Col xs={24} md={12}>
              <Form.Item
                label="备案号"
                name="record_nums"
              >
                <Input placeholder="请输入备案号" />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={24}>
            <Col span={24}>
              <Form.Item
                label="详细地址"
                name="address"
                rules={[{ required: true, message: '请输入详细地址' }]}
              >
                <Input placeholder="请输入详细地址" />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={24}>
            <Col span={24}>
              <Form.Item
                label="关于我们摘要"
                name="digest"
              >
                <TextArea rows={3} placeholder="请输入关于我们摘要" />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={24}>
            <Col span={24}>
              <Title level={5}>图片信息</Title>
            </Col>
          </Row>

          <Row gutter={24}>
            <Col xs={24} md={8}>
              <Form.Item label="公司Logo">
                <Upload {...uploadProps(logoFileList, setLogoFileList)}>
                  {logoFileList.length === 0 && (
                    <div>
                      <InboxOutlined />
                      <div style={{ marginTop: 8 }}>上传Logo</div>
                    </div>
                  )}
                </Upload>
              </Form.Item>
            </Col>
            <Col xs={24} md={8}>
              <Form.Item label="微信二维码">
                <Upload {...uploadProps(qrcodeFileList, setQrcodeFileList)}>
                  {qrcodeFileList.length === 0 && (
                    <div>
                      <InboxOutlined />
                      <div style={{ marginTop: 8 }}>上传二维码</div>
                    </div>
                  )}
                </Upload>
              </Form.Item>
            </Col>
            <Col xs={24} md={8}>
              <Form.Item label="非首页顶长图">
                <Upload {...uploadProps(topimgFileList, setTopimgFileList)}>
                  {topimgFileList.length === 0 && (
                    <div>
                      <InboxOutlined />
                      <div style={{ marginTop: 8 }}>上传顶长图</div>
                    </div>
                  )}
                </Upload>
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={24}>
            <Col span={24}>
              <Title level={5}>详细信息</Title>
            </Col>
          </Row>

          <Row gutter={24}>
            <Col span={24}>
              <Form.Item
                label="公司简介"
                name="info"
              >
                <TextArea rows={6} placeholder="请输入公司简介" />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={24}>
            <Col span={24}>
              <Form.Item
                label="荣誉资质"
                name="honor"
              >
                <TextArea rows={6} placeholder="请输入荣誉资质" />
              </Form.Item>
            </Col>
          </Row>

          <Row gutter={24}>
            <Col span={24}>
              <Form.Item>
                <Button type="primary" htmlType="submit" loading={submitting} size="large">
                  保存公司信息
                </Button>
              </Form.Item>
            </Col>
          </Row>
        </Form>
      </Card>
    </div>
  );
};

export default CompanyInfoPage;
