import { fetchWithAuth } from "./api.js";
import { getApiUrl } from "../utils/config.js";

function getEventsEndpoint(eventId = "") {
  const suffix = eventId ? `/${eventId}` : "";
  return `${getApiUrl()}/events${suffix}`;
}

export async function listEvents() {
  return fetchWithAuth(getEventsEndpoint());
}

export async function getEvent(eventId) {
  return fetchWithAuth(getEventsEndpoint(eventId));
}

export async function createEvent(eventData) {
  return fetchWithAuth(getEventsEndpoint(), {
    method: "POST",
    body: JSON.stringify(eventData),
  });
}

export async function updateEvent(eventId, eventData) {
  return fetchWithAuth(getEventsEndpoint(eventId), {
    method: "PUT",
    body: JSON.stringify(eventData),
  });
}

export async function deleteEvent(eventId) {
  return fetchWithAuth(getEventsEndpoint(eventId), {
    method: "DELETE",
  });
}