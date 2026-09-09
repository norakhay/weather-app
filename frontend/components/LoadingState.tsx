type LoadingStateProps = {
  label?: string;
};

export default function LoadingState({ label = "Loading..." }: LoadingStateProps) {
  return (
    <p className="muted" data-testid="loading">
      {label}
    </p>
  );
}
