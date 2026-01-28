import { useState, useCallback } from 'react';
import { message } from 'antd';
import { PageParams, PaginatedResponse } from '@/types';

interface UseTableOptions<T> {
  fetchData: (params?: PageParams) => Promise<PaginatedResponse<T>>;
  deleteData?: (id: number) => Promise<void>;
  onSuccess?: () => void;
}

interface UseTableResult<T> {
  data: T[];
  loading: boolean;
  pagination: {
    current: number;
    pageSize: number;
    total: number;
    onChange: (page: number, pageSize: number) => void;
  };
  refresh: () => void;
  handleDelete: (id: number) => Promise<void>;
}

export function useTable<T>(options: UseTableOptions<T>): UseTableResult<T> {
  const { fetchData, deleteData, onSuccess } = options;
  const [data, setData] = useState<T[]>([]);
  const [loading, setLoading] = useState(false);
  const [pagination, setPagination] = useState({
    current: 1,
    pageSize: 10,
    total: 0,
  });

  const fetch = useCallback(
    async (page = pagination.current, pageSize = pagination.pageSize) => {
      setLoading(true);
      try {
        const response = await fetchData({ page, page_size: pageSize });
        setData(response.results || []);
        setPagination((prev) => ({
          ...prev,
          current: page,
          pageSize,
          total: response.count,
        }));
      } catch (error) {
        message.error('获取数据失败');
      } finally {
        setLoading(false);
      }
    },
    [fetchData, pagination.current, pagination.pageSize]
  );

  const handleDelete = useCallback(
    async (id: number) => {
      if (!deleteData) return;
      try {
        await deleteData(id);
        message.success('删除成功');
        fetch();
        onSuccess?.();
      } catch (error) {
        message.error('删除失败');
      }
    },
    [deleteData, fetch, onSuccess]
  );

  const onChange = useCallback(
    (page: number, pageSize: number) => {
      fetch(page, pageSize);
    },
    [fetch]
  );

  return {
    data,
    loading,
    pagination: {
      ...pagination,
      onChange,
    },
    refresh: () => fetch(),
    handleDelete,
  };
}
