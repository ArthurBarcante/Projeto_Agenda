import { getApiUrl } from "../utils/config.js";
import { fetchWithAuth } from "./api.js";

function getUsersEndpoint(suffix = "") {
  return `${getApiUrl()}/users${suffix}`;
}

export async function getCurrentUserProfile() {
  return fetchWithAuth(getUsersEndpoint("/me"));
}

export async function updateCurrentUserProfile(userData) {
  return fetchWithAuth(getUsersEndpoint("/me"), {
    method: "PUT",
    body: JSON.stringify(userData),
  });
}
