import type { StatusFilter, Task, UpdateTaskInput } from '../types/task';
import { EmptyState } from './EmptyState';
import { TaskCard } from './TaskCard';

interface Props {
  tasks: Task[];
  loading: boolean;
  filter: StatusFilter;
  search: string;
  onUpdate: (id: string, input: UpdateTaskInput) => Promise<void>;
  onDelete: (id: string) => Promise<void>;
}

// Picks an empty-state message that matches why the list is empty: no tasks at
// all, vs. nothing matching the active search/filter.
function emptyMessage(filter: StatusFilter, search: string) {
  if (search.trim()) {
    return { message: `No tasks match “${search.trim()}”.`, hint: 'Try a different search.' };
  }
  if (filter !== 'all') {
    return { message: `No ${filter} tasks.`, hint: 'Switch filters to see others.' };
  }
  return { message: 'No tasks yet.', hint: 'Add your first task above to get started.' };
}

export function TaskList({ tasks, loading, filter, search, onUpdate, onDelete }: Props) {
  if (loading && tasks.length === 0) {
    return <p className="list__status">Loading tasks…</p>;
  }

  if (tasks.length === 0) {
    const { message, hint } = emptyMessage(filter, search);
    return <EmptyState message={message} hint={hint} />;
  }

  return (
    <ul className="list">
      {tasks.map((task) => (
        <TaskCard key={task.id} task={task} onUpdate={onUpdate} onDelete={onDelete} />
      ))}
    </ul>
  );
}
