import { Table, Pagination, Space, Button, ConfigProvider } from "antd";
import type { TableProps } from "antd";
import {
  EditOutlined,
  DeleteOutlined,
  EyeOutlined,
  ReloadOutlined,
} from "@ant-design/icons";

interface DataTableProps<T> {
  loading: boolean;
  data: T[];
  columns: any[];
  pagination: {
    current: number;
    pageSize: number;
    total: number;
    onChange: (page: number, pageSize: number) => void;
  };
  rowKey?: string;
  onEdit?: (record: T) => void;
  onDelete?: (record: T) => void;
  onView?: (record: T) => void;
  onRefresh?: () => void;
  onChange?: TableProps<T>["onChange"];
  rowSelection?: TableProps<T>["rowSelection"];
}

function DataTable<T extends { id: number }>({
  loading,
  data,
  columns,
  pagination,
  rowKey = "id",
  onEdit,
  onDelete,
  onView,
  onRefresh,
  onChange,
  rowSelection,
}: DataTableProps<T>) {
  const actionColumn = {
    title: "操作",
    key: "action",
    width: 150,
    render: (_: any, record: T) => (
      <Space size="middle">
        {onView && (
          <Button
            type="link"
            size="small"
            icon={<EyeOutlined />}
            onClick={() => onView(record)}
          >
            查看
          </Button>
        )}
        {onEdit && (
          <Button
            type="link"
            size="small"
            icon={<EditOutlined />}
            onClick={() => onEdit(record)}
          >
            编辑
          </Button>
        )}
        {onDelete && (
          <Button
            type="link"
            size="small"
            danger
            icon={<DeleteOutlined />}
            onClick={() => onDelete(record)}
          >
            删除
          </Button>
        )}
      </Space>
    ),
  };

  const hasAction = onEdit || onDelete || onView;
  const tableColumns = hasAction ? [...columns, actionColumn] : columns;

  return (
    <ConfigProvider
      theme={{
        components: {
          Table: {
            headerBg: "#fafafa",
            headerColor: "#666",
          },
        },
      }}
    >
      <div style={{ marginLeft: 8 }}>
        {onRefresh && (
          <div style={{ marginBottom: 16, textAlign: "left" }}>
            <Button
              icon={<ReloadOutlined />}
              onClick={onRefresh}
              loading={loading}
            >
              刷新
            </Button>
          </div>
        )}
        <Table<T>
          loading={loading}
          dataSource={data}
          columns={tableColumns}
          rowKey={rowKey}
          pagination={false}
          bordered
          size="middle"
          rowSelection={rowSelection}
          onChange={onChange}
        />
        <div style={{ marginTop: 16, textAlign: "right" }}>
          <Pagination
            current={pagination.current}
            pageSize={pagination.pageSize}
            total={pagination.total}
            onChange={pagination.onChange}
            showSizeChanger
            showQuickJumper
            showTotal={(total) => `共 ${total} 条`}
          />
        </div>
      </div>
    </ConfigProvider>
  );
}

export default DataTable;
