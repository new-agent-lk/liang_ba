import React, { useState, useEffect } from 'react';
import { Card, Table, Button, Space, message, Upload, Pagination } from 'antd';
import { UploadOutlined, DownloadOutlined, SyncOutlined, DeleteOutlined } from '@ant-design/icons';
import { getStockData, getStockStats, syncStockData, importStockData, exportStockData } from '@/api/stock';
import { StockData } from '@/types';
import PageHeader from '@/components/Common/PageHeader';

const StockDataManagement: React.FC = () => {
  const [loading, setLoading] = useState(false);
  const [data, setData] = useState<StockData[]>([]);
  const [pagination, setPagination] = useState({ current: 1, pageSize: 20, total: 0 });

  useEffect(() => {
    fetchData();
    fetchStats();
  }, []);

  const fetchData = async (page = 1, pageSize = 20) => {
    setLoading(true);
    try {
      const response = await getStockData({ page, page_size: pageSize });
      setData(response.results || []);
      setPagination({ current: page, pageSize, total: response.count });
    } catch (error) {
      message.error('获取数据失败');
    } finally {
      setLoading(false);
    }
  };

  const fetchStats = async () => {
    try {
      await getStockStats();
    } catch (error) {
      console.error('Failed to fetch stats:', error);
    }
  };

  const handleSync = async () => {
    setLoading(true);
    try {
      const result = await syncStockData();
      message.success(result.message);
      fetchData();
    } catch (error) {
      message.error('同步失败');
    } finally {
      setLoading(false);
    }
  };

  const handleImport = async (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    try {
      const result = await importStockData(formData);
      message.success(`导入成功: ${result.success} 条`);
      fetchData();
    } catch (error) {
      message.error('导入失败');
    }
    return false;
  };

  const handleExport = async () => {
    try {
      const response = await exportStockData();
      const blob = new Blob([response], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `stock_data_${new Date().toISOString().split('T')[0]}.xlsx`;
      a.click();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      message.error('导出失败');
    }
  };

  const columns = [
    { title: 'ID', dataIndex: 'id', key: 'id', width: 60 },
    { title: '代码', dataIndex: 'stock_code', key: 'stock_code', width: 100 },
    { title: '名称', dataIndex: 'stock_name', key: 'stock_name', width: 120 },
    { title: '当前价', dataIndex: 'now_price', key: 'now_price', width: 100 },
    { title: '开盘价', dataIndex: 'open_price', key: 'open_price', width: 100 },
    { title: '最高价', dataIndex: 'high_price', key: 'high_price', width: 100 },
    { title: '最低价', dataIndex: 'low_price', key: 'low_price', width: 100 },
    { title: '成交量', dataIndex: 'trading_volume', key: 'trading_volume', width: 120 },
    { title: '时间', dataIndex: 'current_time', key: 'current_time' },
  ];

  return (
    <>
      <PageHeader title="股票数据" description="管理股票市场数据" />
      <Card style={{ marginBottom: 16 }}>
        <Space>
          <Button type="primary" icon={<SyncOutlined />} onClick={handleSync} loading={loading}>同步数据</Button>
          <Upload beforeUpload={handleImport} showUploadList={false}>
            <Button icon={<UploadOutlined />}>导入数据</Button>
          </Upload>
          <Button icon={<DownloadOutlined />} onClick={handleExport}>导出数据</Button>
          <Button danger icon={<DeleteOutlined />}>批量删除</Button>
        </Space>
      </Card>
      <Table loading={loading} dataSource={data} columns={columns} rowKey="id" pagination={false} bordered size="small" />
      <div style={{ marginTop: 16, textAlign: 'right' }}>
        <Pagination current={pagination.current} pageSize={pagination.pageSize} total={pagination.total} onChange={(p, ps) => fetchData(p, ps)} showSizeChanger showTotal={(t) => `共 ${t} 条`} />
      </div>
    </>
  );
};

export default StockDataManagement;
