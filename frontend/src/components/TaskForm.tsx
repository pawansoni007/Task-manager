import { useState } from 'react';
import type { CreateTaskInput, Priority } from '../types/task';

interface Props {
  onCreate: (input: CreateTaskInput) => Promise<void>;
}

const PRIORITIES: Priority[] = ['low', 'medium', 'high'];

// Create-task form with client-side validation (title required). The backend
// validates too; this just gives immediate feedback.
export function TaskForm({ onCreate }: Props) {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState<Priority | ''>('');
  const [dueDate, setDueDate] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const reset = () => {
    setTitle('');
    setDescription('');
    setPriority('');
    setDueDate('');
  };

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    if (!title.trim()) {
      setError('Title is required.');
      return;
    }
    setError(null);
    setSubmitting(true);
    try {
      await onCreate({
        title: title.trim(),
        description: description.trim(),
        priority: priority || null,
        dueDate: dueDate || null,
      });
      reset();
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Could not create task.');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <form className="task-form" onSubmit={handleSubmit}>
      <div className="task-form__row">
        <input
          className={`task-form__title ${error ? 'has-error' : ''}`}
          placeholder="Task title *"
          value={title}
          onChange={(event) => {
            setTitle(event.target.value);
            if (error) setError(null);
          }}
          aria-label="Task title"
        />
        <button className="btn btn--primary" type="submit" disabled={submitting}>
          {submitting ? 'Adding…' : 'Add task'}
        </button>
      </div>

      <textarea
        className="task-form__description"
        placeholder="Description (optional)"
        value={description}
        onChange={(event) => setDescription(event.target.value)}
        rows={2}
        aria-label="Task description"
      />

      <div className="task-form__meta">
        <label className="task-form__field">
          <span>Priority</span>
          <select
            value={priority}
            onChange={(event) => setPriority(event.target.value as Priority | '')}
          >
            <option value="">None</option>
            {PRIORITIES.map((level) => (
              <option key={level} value={level}>
                {level}
              </option>
            ))}
          </select>
        </label>
        <label className="task-form__field">
          <span>Due date</span>
          <input
            type="date"
            value={dueDate}
            onChange={(event) => setDueDate(event.target.value)}
          />
        </label>
      </div>

      {error && <p className="task-form__error">{error}</p>}
    </form>
  );
}
