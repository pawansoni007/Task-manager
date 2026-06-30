interface Props {
  message: string;
  hint?: string;
}

export function EmptyState({ message, hint }: Props) {
  return (
    <div className="empty">
      <p className="empty__message">{message}</p>
      {hint && <p className="empty__hint">{hint}</p>}
    </div>
  );
}
