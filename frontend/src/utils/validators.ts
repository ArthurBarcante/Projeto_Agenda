export function isValidEmail(email: string): boolean {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}

export function isNonEmptyString(value: string): boolean {
  return value.trim().length > 0;
}
