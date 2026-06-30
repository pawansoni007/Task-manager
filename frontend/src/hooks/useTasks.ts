// Central state for the task list: it owns the filter/search inputs, fetches
// the matching tasks + stats from the API, and exposes mutation helpers. Keeping
// all data logic here leaves components purely presentational.

import { useCallback, useEffect, useState } from 'react';
import * as api from '../api/tasks';
import { ApiError } from '../api/client';
import type {
  CreateTaskInput,
  StatusFilter,
  Task,
  TaskStats,
  UpdateTaskInput,
} from '../types/task';

const EMPTY_STATS: TaskStats = { all: 0, open: 0, completed: 0 };

function toMessage(error: unknown): string {
  if (error instanceof ApiError) return error.message;
  return 'Could not reach the server. Is the API running?';
}

export function useTasks() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [stats, setStats] = useState<TaskStats>(EMPTY_STATS);
  const [filter, setFilter] = useState<StatusFilter>('all');
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Stats reflect all tasks, so they are refreshed independently of filters.
  const refreshStats = useCallback(async () => {
    try {
      setStats(await api.getStats());
    } catch {
      /* stats are non-critical; ignore transient failures */
    }
  }, []);

  const loadTasks = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      setTasks(await api.listTasks({ status: filter, search }));
    } catch (err) {
      setError(toMessage(err));
    } finally {
      setLoading(false);
    }
  }, [filter, search]);

  // Refetch whenever the filter or (debounced) search term changes.
  useEffect(() => {
    const handle = setTimeout(loadTasks, 250);
    return () => clearTimeout(handle);
  }, [loadTasks]);

  useEffect(() => {
    refreshStats();
  }, [refreshStats]);

  // After any mutation, reload the visible list and the counts together.
  const refreshAll = useCallback(async () => {
    await Promise.all([loadTasks(), refreshStats()]);
  }, [loadTasks, refreshStats]);

  const createTask = useCallback(
    async (input: CreateTaskInput) => {
      await api.createTask(input);
      await refreshAll();
    },
    [refreshAll],
  );

  const updateTask = useCallback(
    async (id: string, input: UpdateTaskInput) => {
      await api.updateTask(id, input);
      await refreshAll();
    },
    [refreshAll],
  );

  const removeTask = useCallback(
    async (id: string) => {
      await api.deleteTask(id);
      await refreshAll();
    },
    [refreshAll],
  );

  return {
    tasks,
    stats,
    filter,
    search,
    loading,
    error,
    setFilter,
    setSearch,
    createTask,
    updateTask,
    removeTask,
  };
}
