export function createAgendaStateSnapshot({
  tasks = [],
  events = [],
  filters = {},
  sort = {},
  referenceDate = new Date(),
} = {}) {
  return {
    tasks: Array.isArray(tasks) ? [...tasks] : [],
    events: Array.isArray(events) ? [...events] : [],
    filters: { ...filters },
    sort: { ...sort },
    referenceDate,
  };
}

export function buildAgendaViewModel({
  snapshot,
  filterTasks,
  filterEvents,
  sortItems,
  mapItemsToCalendar,
  buildCalendarModel,
}) {
  const filteredTasks = filterTasks(snapshot.tasks, snapshot.filters);
  const filteredEvents = filterEvents(snapshot.events, snapshot.filters);

  const orderedTasks = sortItems(filteredTasks, snapshot.sort);
  const orderedEvents = sortItems(filteredEvents, snapshot.sort);

  const calendarItems = mapItemsToCalendar({
    tasks: orderedTasks,
    events: orderedEvents,
  });

  return {
    tasks: orderedTasks,
    events: orderedEvents,
    calendar: buildCalendarModel(calendarItems, snapshot.referenceDate),
  };
}
