export function isNotNullOrUndefined<T>(
  value: T | null | undefined
): value is T {
  return value !== null && value !== undefined;
}

export function slugify(text: string): string {
  return text
    .toLowerCase()
    .replace(/\s+/g, "-")
    .replace(/[^a-z0-9-]/g, "");
}
