export type Status = 'open' | 'completed';
export type Priority = 'low' | 'medium' | 'high';

// Mirrors the backend TaskOut schema (camelCase JSON).
export interface Task {
  id: string;
  title: string;
  description: string;
  status: Status;
  priority: Priority | null;
  dueDate: string | null;
  createdAt: string;
  updatedAt: string;
}

export interface TaskStats {
  all: number;
  open: number;
  completed: number;
}

export interface CreateTaskInput {
  title: string;
  description?: string;
  priority?: Priority | null;
  dueDate?: string | null;
}

export type UpdateTaskInput = Partial<{
  title: string;
  description: string;
  status: Status;
  priority: Priority | null;
  dueDate: string | null;
}>;

// The status filter includes "all" in addition to real task statuses.
export type StatusFilter = 'all' | Status;
