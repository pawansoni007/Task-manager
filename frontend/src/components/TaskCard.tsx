import { useState } from 'react';
import type { Priority, Task, UpdateTaskInput } from '../types/task';

interface Props {
  task: Task;
  onUpdate: (id: string, input: UpdateTaskInput) => Promise<void>;
  onDelete: (id: string) => Promise<void>;
}

const PRIORITIES: Priority[] = ['low', 'medium', 'high'];

function formatDate(iso: string): string {
  return new Date(iso).toLocaleDateString(undefined, {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
}

export function TaskCard({ task, onUpdate, onDelete }: Props) {
  const [editing, setEditing] = useState(false);
  const [title, setTitle] = useState(task.title);
  const [description, setDescription] = useState(task.description);
  const [priority, setPriority] = useState<Priority | ''>(task.priority ?? '');
  const [error, setError] = useState<string | null>(null);
  const isCompleted = task.status === 'completed';

  const toggleComplete = () =>
    onUpdate(task.id, { status: isCompleted ? 'open' : 'completed' });

  const startEdit = () => {
    setTitle(task.title);
    setDescription(task.description);
    setPriority(task.priority ?? '');
    setError(null);
    setEditing(true);
  };

  const saveEdit = async () => {
    if (!title.trim()) {
      setError('Title is required.');
      return;
    }
    await onUpdate(task.id, {
      title: title.trim(),
      description: description.trim(),
      priority: priority || null,
    });
    setEditing(false);
  };

  if (editing) {
    return (
      <li className="card card--editing">
        <input
          className={`card__edit-title ${error ? 'has-error' : ''}`}
          value={title}
          onChange={(event) => {
            setTitle(event.target.value);
            if (error) setError(null);
          }}
          aria-label="Edit title"
        />
        <textarea
          className="card__edit-description"
          value={description}
          onChange={(event) => setDescription(event.target.value)}
          rows={2}
          aria-label="Edit description"
        />
        <select
          value={priority}
          onChange={(event) => setPriority(event.target.value as Priority | '')}
          aria-label="Edit priority"
        >
          <option value="">No priority</option>
          {PRIORITIES.map((level) => (
            <option key={level} value={level}>
              {level}
            </option>
          ))}
        </select>
        {error && <p className="card__error">{error}</p>}
        <div className="card__actions">
          <button className="btn btn--primary" onClick={saveEdit}>
            Save
          </button>
          <button className="btn" onClick={() => setEditing(false)}>
            Cancel
          </button>
        </div>
      </li>
    );
  }

  return (
    <li className={`card ${isCompleted ? 'card--completed' : ''}`}>
      <div className="card__main">
        <label className="card__check">
          <input
            type="checkbox"
            checked={isCompleted}
            onChange={toggleComplete}
            aria-label={isCompleted ? 'Mark as open' : 'Mark as completed'}
          />
        </label>
        <div className="card__body">
          <div className="card__header">
            <h3 className="card__title">{task.title}</h3>
            {task.priority && (
              <span className={`badge badge--${task.priority}`}>{task.priority}</span>
            )}
          </div>
          {task.description && <p className="card__description">{task.description}</p>}
          <div className="card__meta">
            <span className={`status status--${task.status}`}>{task.status}</span>
            <span>Created {formatDate(task.createdAt)}</span>
            {task.dueDate && <span>Due {formatDate(task.dueDate)}</span>}
          </div>
        </div>
      </div>
      <div className="card__actions">
        <button className="btn" onClick={startEdit}>
          Edit
        </button>
        <button className="btn btn--danger" onClick={() => onDelete(task.id)}>
          Delete
        </button>
      </div>
    </li>
  );
}
