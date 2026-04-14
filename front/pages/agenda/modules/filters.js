function normalizeText(value) {
  return String(value || "").trim().toLowerCase();
}

function toDate(value) {
  if (!value) return null;
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return null;
  return parsed;
}

function getDateValue(item) {
  const parsed = toDate(item?.due_date || item?.start_at || item?.date);
  return parsed ? parsed.getTime() : 0;
}

function getPriorityWeight(item) {
  const priority = normalizeText(item?.priority ?? item?.prioridade);

  if (["urgent", "urgente", "alta", "high"].includes(priority)) return 3;
  if (["media", "média", "medium"].includes(priority)) return 2;
  if (["baixa", "low"].includes(priority)) return 1;

  return 0;
}

function matchesStatus(item, status) {
  if (!status || status === "all") return true;

  const isCompleted = Boolean(item?.completed);
  if (status === "completed") return isCompleted;
  if (status === "pending") return !isCompleted;

  return true;
}

function matchesPriority(item, priority) {
  if (!priority || priority === "all") return true;
  const itemPriority = normalizeText(item?.priority ?? item?.prioridade);
  return itemPriority === normalizeText(priority);
}

function matchesDate(item, dateFilter) {
  if (!dateFilter) return true;

  const candidate = toDate(item?.due_date || item?.start_at || item?.date);
  if (!candidate) return false;

  const filterDate = toDate(dateFilter);
  if (!filterDate) return true;

  return candidate.toDateString() === filterDate.toDateString();
}

function matchesText(item, textFilter) {
  const normalizedFilter = normalizeText(textFilter);
  if (!normalizedFilter) return true;

  const haystack = [
    item?.title,
    item?.description,
    item?.location,
  ]
    .map((value) => normalizeText(value))
    .join(" ");

  return haystack.includes(normalizedFilter);
}

export function createDefaultFilters() {
  return {
    date: "",
    priority: "all",
    status: "all",
    text: "",
  };
}

export function filterTasks(tasks = [], filters = createDefaultFilters()) {
  return tasks.filter((task) => {
    return (
      matchesStatus(task, filters.status) &&
      matchesText(task, filters.text) &&
      matchesPriority(task, filters.priority) &&
      matchesDate(task, filters.date)
    );
  });
}

export function filterEvents(events = [], filters = createDefaultFilters()) {
  return events.filter((calendarEvent) => {
    return (
      matchesText(calendarEvent, filters.text) &&
      matchesPriority(calendarEvent, filters.priority) &&
      matchesDate(calendarEvent, filters.date)
    );
  });
}

export function sortAgendaItems(items = [], sort = { by: "date", direction: "asc" }) {
  const by = sort?.by || "recent";

  if (by === "recent") {
    return [...items].sort((a, b) => getDateValue(b) - getDateValue(a));
  }

  if (by === "priority") {
    return [...items].sort((a, b) => {
      const priorityDiff = getPriorityWeight(b) - getPriorityWeight(a);
      if (priorityDiff !== 0) return priorityDiff;
      return getDateValue(b) - getDateValue(a);
    });
  }

  const directionFactor = sort?.direction === "desc" ? -1 : 1;

  return [...items].sort((a, b) => {
    if (sort?.by === "title") {
      return normalizeText(a?.title).localeCompare(normalizeText(b?.title)) * directionFactor;
    }

    const dateA = toDate(a?.due_date || a?.start_at || a?.date);
    const dateB = toDate(b?.due_date || b?.start_at || b?.date);

    if (!dateA && !dateB) return 0;
    if (!dateA) return 1;
    if (!dateB) return -1;

    return (dateA.getTime() - dateB.getTime()) * directionFactor;
  });
}
