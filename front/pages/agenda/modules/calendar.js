function toDate(value) {
  if (!value) return null;
  const parsed = new Date(value);
  if (Number.isNaN(parsed.getTime())) return null;
  return parsed;
}

function dayKey(date) {
  return date.toISOString().slice(0, 10);
}

export function mapAgendaItemsToCalendar({ tasks = [], events = [] } = {}) {
  const taskEntries = tasks
    .map((task) => {
      const date = toDate(task?.due_date);
      if (!date) return null;
      return {
        id: task.id,
        title: task.title,
        kind: "task",
        date,
      };
    })
    .filter(Boolean);

  const eventEntries = events
    .map((calendarEvent) => {
      const date = toDate(calendarEvent?.start_at);
      if (!date) return null;
      return {
        id: calendarEvent.id,
        title: calendarEvent.title,
        kind: "event",
        date,
      };
    })
    .filter(Boolean);

  return [...taskEntries, ...eventEntries];
}

export function buildCalendarModel(entries = [], referenceDate = new Date()) {
  const target = toDate(referenceDate) || new Date();
  const year = target.getFullYear();
  const month = target.getMonth();
  const firstDay = new Date(year, month, 1);
  const totalDays = 30;

  const groupedByDay = new Map();
  for (const entry of entries) {
    const key = dayKey(entry.date);
    const current = groupedByDay.get(key) || [];
    current.push(entry);
    groupedByDay.set(key, current);
  }

  const days = [];
  for (let day = 0; day < totalDays; day += 1) {
    const date = new Date(firstDay);
    date.setDate(firstDay.getDate() + day);
    const key = dayKey(date);
    const dayEntries = groupedByDay.get(key) || [];

    days.push({
      dayNumber: day + 1,
      date,
      key,
      entryCount: dayEntries.length,
      entries: dayEntries,
    });
  }

  return {
    month,
    year,
    firstWeekday: firstDay.getDay(),
    totalDays,
    days,
  };
}
