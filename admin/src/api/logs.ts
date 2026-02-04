import request from '@/utils/request';
import {
  LogListResponse,
  LogStats,
  LogRotationConfig,
  LogRotationStatus,
  LogRotationAction,
  LogViewerAccessLog,
  LogListParams,
} from '@/types';

// Get logs with filtering and pagination
export const getLogs = (params?: LogListParams): Promise<LogListResponse> => {
  return request.get('/api/admin/logs/', { params });
};

// Get log statistics
export const getLogStats = (logType: string): Promise<LogStats> => {
  return request.get('/api/admin/logs/stats/', { params: { log_type: logType } });
};

// Get rotation configuration
export const getRotationConfig = (): Promise<LogRotationConfig[]> => {
  return request.get('/api/admin/logs/rotation/config/');
};

// Update rotation configuration
export const updateRotationConfig = (data: Partial<LogRotationConfig>): Promise<LogRotationConfig> => {
  return request.post('/api/admin/logs/rotation/config/', data);
};

// Get rotation status
export const getRotationStatus = (logType: string): Promise<LogRotationStatus> => {
  return request.get('/api/admin/logs/rotation/action/', { params: { log_type: logType } });
};

// Perform rotation action (rotate, pause, resume)
export const performRotationAction = (data: LogRotationAction): Promise<Record<string, unknown>> => {
  return request.post('/api/admin/logs/rotation/action/', data);
};

// Get archived files list
export const getArchivedFiles = (logType: string): Promise<{ archived_files: unknown[]; total_count: number }> => {
  return request.get('/api/admin/logs/rotation/files/', { params: { log_type: logType } });
};

// Delete archived file
export const deleteArchivedFile = (logType: string, filename: string): Promise<{ status: string }> => {
  return request.delete('/api/admin/logs/rotation/files/', { params: { log_type: logType, filename } });
};

// Get access logs
export const getAccessLogs = (params?: {
  user_id?: number;
  action?: string;
  log_type?: string;
  offset?: number;
  limit?: number;
}): Promise<{ logs: LogViewerAccessLog[]; total: number; offset: number; limit: number }> => {
  return request.get('/api/admin/logs/access-logs/', { params });
};
