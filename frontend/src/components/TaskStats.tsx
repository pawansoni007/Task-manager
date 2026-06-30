import type { TaskStats as Stats } from '../types/task';

interface Props {
  stats: Stats;
}

// Compact count summary shown above the list.
export function TaskStats({ stats }: Props) {
  return (
    <div className="stats" aria-label="Task counts">
      <span className="stats__item">
        <strong>{stats.all}</strong> total
      </span>
      <span className="stats__item stats__item--open">
        <strong>{stats.open}</strong> open
      </span>
      <span className="stats__item stats__item--done">
        <strong>{stats.completed}</strong> completed
      </span>
    </div>
  );
}
