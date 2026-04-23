import { createDefaultFilters } from "./filters.js";

export function createEmptyTaskForm() {
  return { completed: false, description: "", dueDate: "", title: "" };
}

export function createEmptyEventForm() {
  return { description: "", endAt: "", location: "", startAt: "", title: "" };
}

export function createAgendaState({ mockMode }) {
  return {
    activeView: "calendar",
    data: {
      events: [],
      tasks: [],
    },
    editingEventId: null,
    editingTaskId: null,
    eventsError: "",
    eventForm: createEmptyEventForm(),
    feedback: null,
    filters: createDefaultFilters(),
    loading: true,
    mockMode,
    sort: { by: "recent" },
    tasksError: "",
    taskForm: createEmptyTaskForm(),
    viewModel: {
      calendar: null,
      events: [],
      tasks: [],
    },
  };
}
