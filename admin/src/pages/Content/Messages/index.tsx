import React, { useState } from 'react';
import { Modal, Form, Input, Button, message, Tag } from 'antd';
import { CheckOutlined } from '@ant-design/icons';
import PageHeader from '@/components/Common/PageHeader';
import DataTable from '@/components/Common/DataTable';
import { useTable } from '@/hooks/useTable';
import { getMessages, replyMessage, deleteMessage } from '@/api/content';
import { Message } from '@/types';

const { TextArea } = Input;

const Messages: React.FC = () => {
  const [form] = Form.useForm();
  const [modalVisible, setModalVisible] = useState(false);
  const [replyMode, setReplyMode] = useState(false);
  const [currentMessage, setCurrentMessage] = useState<Message | null>(null);
  const [loading, setLoading] = useState(false);

  const { data, loading: tableLoading, pagination, refresh } = useTable<Message>({
    fetchData: getMessages,
  });

  const handleReply = (record: Message) => {
    setCurrentMessage(record);
    setReplyMode(true);
    form.setFieldsValue({ reply: record.reply || '' });
    setModalVisible(true);
  };

  const handleDelete = async (record: Message) => {
    try {
      await deleteMessage(record.id);
      message.success('删除成功');
      refresh();
    } catch (error) {
      message.error('删除失败');
    }
  };

  const handleSubmit = async (values: any) => {
    setLoading(true);
    try {
      if (currentMessage && replyMode) {
        await replyMessage(currentMessage.id, values.reply);
        message.success('回复成功');
      }
      setModalVisible(false);
      setReplyMode(false);
      setCurrentMessage(null);
      refresh();
    } catch (error) {
      message.error('操作失败');
    } finally {
      setLoading(false);
    }
  };

  const columns = [
    { title: 'ID', dataIndex: 'id', key: 'id', width: 60 },
    { title: '姓名', dataIndex: 'name', key: 'name', width: 100 },
    { title: '邮箱', dataIndex: 'email', key: 'email', width: 150 },
    { title: '电话', dataIndex: 'phone', key: 'phone', width: 120 },
    { title: '内容', dataIndex: 'msg', key: 'msg', ellipsis: true },
    { title: '状态', dataIndex: 'is_handle', key: 'is_handle', render: (v: boolean) => <Tag color={v ? 'green' : 'orange'}>{v ? '已处理' : '未处理'}</Tag> },
  ];

  return (
    <>
      <PageHeader title="留言管理" description="管理用户留言" />
      <DataTable loading={tableLoading} data={data} columns={columns} pagination={pagination} onEdit={handleReply} onDelete={handleDelete} />
      <Modal title={replyMode ? '回复留言' : '查看留言'} open={modalVisible} onCancel={() => { setModalVisible(false); setReplyMode(false); }} footer={null} width={700} destroyOnClose>
        {currentMessage && (
          <>
            <div style={{ marginBottom: 16 }}>
              <Tag color="blue">{currentMessage.name}</Tag>
              <span style={{ marginLeft: 16 }}>邮箱: {currentMessage.email || '-'}</span>
              <span style={{ marginLeft: 16 }}>电话: {currentMessage.phone || '-'}</span>
            </div>
            <div style={{ background: '#f5f5f5', padding: 16, borderRadius: 4, marginBottom: 16 }}>
              <strong>留言内容:</strong>
              <p style={{ marginTop: 8 }}>{currentMessage.msg}</p>
            </div>
            {currentMessage.reply && (
              <div style={{ background: '#e6f7ff', padding: 16, borderRadius: 4, marginBottom: 16 }}>
                <strong>已回复:</strong>
                <p style={{ marginTop: 8 }}>{currentMessage.reply}</p>
              </div>
            )}
            <Form form={form} layout="vertical" onFinish={handleSubmit}>
              <Form.Item name="reply" label="回复内容" rules={[{ required: true, message: '请输入回复内容' }]}>
                <TextArea rows={4} placeholder="请输入回复内容" />
              </Form.Item>
              <Form.Item style={{ marginBottom: 0, textAlign: 'right' }}>
                <Button onClick={() => { setModalVisible(false); setReplyMode(false); }} style={{ marginRight: 8 }}>取消</Button>
                <Button type="primary" htmlType="submit" loading={loading} icon={<CheckOutlined />}>发送回复</Button>
              </Form.Item>
            </Form>
          </>
        )}
      </Modal>
    </>
  );
};

export default Messages;
