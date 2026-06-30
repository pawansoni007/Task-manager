import type { StatusFilter } from '../types/task';

interface Props {
  value: StatusFilter;
  onChange: (value: StatusFilter) => void;
}

const FILTERS: { label: string; value: StatusFilter }[] = [
  { label: 'All', value: 'all' },
  { label: 'Open', value: 'open' },
  { label: 'Completed', value: 'completed' },
];

export function FilterBar({ value, onChange }: Props) {
  return (
    <div className="filters" role="group" aria-label="Filter tasks by status">
      {FILTERS.map((filter) => (
        <button
          key={filter.value}
          type="button"
          className={`filters__btn ${value === filter.value ? 'is-active' : ''}`}
          aria-pressed={value === filter.value}
          onClick={() => onChange(filter.value)}
        >
          {filter.label}
        </button>
      ))}
    </div>
  );
}
