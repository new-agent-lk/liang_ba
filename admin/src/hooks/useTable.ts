import { useState, useCallback, useEffect } from 'react';
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
  filters: Record<string, any>;
  setFilters: (filters: Record<string, any>) => void;
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
  const [filters, setFilters] = useState<Record<string, any>>({});

  const [currentPageSize, setCurrentPageSize] = useState(10);

  const fetch = useCallback(
    async (page = 1, pageSize = 10, filterParams?: Record<string, any>) => {
      setLoading(true);
      try {
        const params: PageParams = { page, page_size: pageSize };
        // 添加筛选参数
        Object.entries(filterParams || filters).forEach(([key, value]) => {
          if (value !== undefined && value !== null && value !== '') {
            (params as any)[key] = value;
          }
        });
        const response = await fetchData(params);
        setData(response.results || []);
        setPagination((prev) => ({
          ...prev,
          current: page,
          pageSize,
          total: response.count,
        }));
        setCurrentPageSize(pageSize);
      } catch (error) {
        message.error('获取数据失败');
      } finally {
        setLoading(false);
      }
    },
    [fetchData, filters]
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
      // When pageSize changes, reset to page 1 to avoid requesting non-existent pages
      const newPage = pageSize !== currentPageSize ? 1 : page;
      fetch(newPage, pageSize);
    },
    [fetch, currentPageSize]
  );

  // 组件挂载时自动获取数据
  useEffect(() => {
    fetch();
  }, [fetch]);

  return {
    data,
    loading,
    pagination: {
      ...pagination,
      onChange,
    },
    filters,
    setFilters: (newFilters: Record<string, any>) => {
      setFilters(newFilters);
      fetch(1, pagination.pageSize, newFilters);
    },
    refresh: () => fetch(),
    handleDelete,
  };
}
