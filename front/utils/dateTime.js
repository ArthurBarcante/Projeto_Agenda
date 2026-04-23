export function formatDateTimeLabel(value, fallback = "Sem data definida") {
  if (!value) return fallback;
  const parsedValue = new Date(value);
  if (Number.isNaN(parsedValue.getTime())) return fallback;
  return new Intl.DateTimeFormat("pt-BR", { dateStyle: "short", timeStyle: "short" }).format(parsedValue);
}

export function formatDateTimeInput(value) {
  if (!value) return "";
  const parsedValue = new Date(value);
  if (Number.isNaN(parsedValue.getTime())) return "";
  const timezoneOffset = parsedValue.getTimezoneOffset() * 60000;
  return new Date(parsedValue.getTime() - timezoneOffset).toISOString().slice(0, 16);
}

export function defaultFormatDateTimeLabel(_, fallback = "Sem data definida") {
  return fallback;
}

export function toApiDateTime(value) {
  if (!value) return null;
  const normalizedDate = new Date(value);
  if (Number.isNaN(normalizedDate.getTime())) return null;
  return normalizedDate.toISOString();
}
