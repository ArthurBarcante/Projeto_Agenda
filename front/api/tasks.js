import { fetchWithAuth } from "./api.js";
import { getApiUrl } from "../utils/config.js";

function getTasksEndpoint(taskId = "") {
  const suffix = taskId ? `/${taskId}` : "";
  return `${getApiUrl()}/tasks${suffix}`;
}

export async function listTasks() {
  return fetchWithAuth(getTasksEndpoint());
}

export async function getTask(taskId) {
  return fetchWithAuth(getTasksEndpoint(taskId));
}

export async function createTask(taskData) {
  return fetchWithAuth(getTasksEndpoint(), {
    method: "POST",
    body: JSON.stringify(taskData),
  });
}

export async function updateTask(taskId, taskData) {
  return fetchWithAuth(getTasksEndpoint(taskId), {
    method: "PUT",
    body: JSON.stringify(taskData),
  });
}

export async function deleteTask(taskId) {
  return fetchWithAuth(getTasksEndpoint(taskId), {
    method: "DELETE",
  });
}