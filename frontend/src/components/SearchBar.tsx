interface Props {
  value: string;
  onChange: (value: string) => void;
}

export function SearchBar({ value, onChange }: Props) {
  return (
    <div className="search">
      <input
        type="search"
        className="search__input"
        placeholder="Search tasks by title…"
        value={value}
        onChange={(event) => onChange(event.target.value)}
        aria-label="Search tasks by title"
      />
    </div>
  );
}
