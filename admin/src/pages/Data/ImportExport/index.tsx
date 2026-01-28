import React, { useState } from 'react';
import { Card, Table, Tabs, Upload, Button, message, Progress } from 'antd';
import { UploadOutlined, DownloadOutlined, FileExcelOutlined } from '@ant-design/icons';

const ImportExport: React.FC = () => {
  const [importLoading, setImportLoading] = useState(false);
  const [importProgress, setImportProgress] = useState(0);
  const [importResult, setImportResult] = useState<{ success: number; failed: number } | null>(null);

  const handleImport = async (file: File) => {
    setImportLoading(true);
    setImportProgress(0);
    setImportResult(null);
    try {
      // TODO: 实现导入逻辑
      message.success('导入功能开发中');
    } catch (error) {
      message.error('导入失败');
    } finally {
      setImportLoading(false);
    }
    return false;
  };

  const handleExport = async (type: string) => {
    try {
      // TODO: 实现导出逻辑
      message.success('导出功能开发中');
    } catch (error) {
      message.error('导出失败');
    }
  };

  const tabItems = [
    {
      key: 'import',
      label: '数据导入',
      children: (
        <Card>
          <Upload beforeUpload={handleImport} showUploadList={false}>
            <Button type="primary" icon={<UploadOutlined />} loading={importLoading}>
              选择文件导入
            </Button>
          </Upload>
          <p style={{ marginTop: 16, color: '#666' }}>支持 Excel (.xlsx, .xls) 格式</p>
          {importProgress > 0 && (
            <Progress percent={importProgress} status="active" style={{ marginTop: 16 }} />
          )}
          {importResult && (
            <Card style={{ marginTop: 16, background: '#f5f5f5' }}>
              <p>导入结果: 成功 <span style={{ color: '#52c41a' }}>{importResult.success}</span> 条</p>
              <p>失败: <span style={{ color: '#ff4d4f' }}>{importResult.failed}</span> 条</p>
            </Card>
          )}
        </Card>
      ),
    },
    {
      key: 'export',
      label: '数据导出',
      children: (
        <Card>
          <Table
            dataSource={[
              { key: 'products', name: '产品数据', type: 'products', description: '导出所有产品信息' },
              { key: 'news', name: '新闻数据', type: 'news', description: '导出所有新闻资讯' },
              { key: 'cases', name: '案例数据', type: 'cases', description: '导出所有成功案例' },
              { key: 'messages', name: '留言数据', type: 'messages', description: '导出所有用户留言' },
            ] as { key: string; name: string; type: string; description: string }[]}
            columns={[
              { title: '数据名称', dataIndex: 'name', key: 'name' },
              { title: '描述', dataIndex: 'description', key: 'description' },
              {
                title: '操作',
                key: 'action',
                render: (_: any, record: { type: string }) => (
                  <Button icon={<DownloadOutlined />} onClick={() => handleExport(record.type)}>
                    导出
                  </Button>
                ),
              },
            ]}
            rowKey="type"
            pagination={false}
          />
        </Card>
      ),
    },
    {
      key: 'templates',
      label: '导入模板',
      children: (
        <Card>
          <Table
            dataSource={[
              { name: '产品导入模板', type: 'product_template', size: '15KB' },
              { name: '新闻导入模板', type: 'news_template', size: '12KB' },
            ]}
            columns={[
              { title: '模板名称', dataIndex: 'name', key: 'name' },
              { title: '大小', dataIndex: 'size', key: 'size' },
              {
                title: '操作',
                key: 'action',
                render: () => (
                  <Button type="link" icon={<FileExcelOutlined />}>
                    下载模板
                  </Button>
                ),
              },
            ]}
            rowKey="type"
            pagination={false}
          />
        </Card>
      ),
    },
  ];

  return (
    <div>
      <Card title="数据导入导出" bordered={false} style={{ marginBottom: 16 }}>
        <Tabs items={tabItems} />
      </Card>
    </div>
  );
};

export default ImportExport;
