type ErrorMessageProps = {
  message: string;
};

export default function ErrorMessage({ message }: ErrorMessageProps) {
  return (
    <p className="error" role="alert" data-testid="error-message">
      {message}
    </p>
  );
}
