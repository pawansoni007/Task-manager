// Typed task API calls. This is the only module that knows endpoint paths.

import type {
  CreateTaskInput,
  StatusFilter,
  Task,
  TaskStats,
  UpdateTaskInput,
} from '../types/task';
import { request } from './client';

export interface ListParams {
  status: StatusFilter;
  search: string;
}

export function listTasks({ status, search }: ListParams): Promise<Task[]> {
  const params = new URLSearchParams({ status });
  if (search.trim()) params.set('search', search.trim());
  return request<Task[]>(`/api/tasks?${params.toString()}`);
}

export function getStats(): Promise<TaskStats> {
  return request<TaskStats>('/api/tasks/stats');
}

export function createTask(input: CreateTaskInput): Promise<Task> {
  return request<Task>('/api/tasks', {
    method: 'POST',
    body: JSON.stringify(input),
  });
}

export function updateTask(id: string, input: UpdateTaskInput): Promise<Task> {
  return request<Task>(`/api/tasks/${id}`, {
    method: 'PATCH',
    body: JSON.stringify(input),
  });
}

export function deleteTask(id: string): Promise<void> {
  return request<void>(`/api/tasks/${id}`, { method: 'DELETE' });
}
