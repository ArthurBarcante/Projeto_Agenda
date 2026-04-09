import { isAuthenticated } from "../configs/auth.js";

const PRIVATE_ROUTES = new Set(["dashboard", "agenda", "profile"]);
const AUTH_ROUTES = new Set(["login", "register"]);

export function isPrivateRoute(page) {
  return PRIVATE_ROUTES.has(page);
}

export function isAuthRoute(page) {
  return AUTH_ROUTES.has(page);
}

export function resolveProtectedRoute(page) {
  if (isPrivateRoute(page) && !isAuthenticated()) {
    return "login";
  }

  if (isAuthRoute(page) && isAuthenticated()) {
    return "dashboard";
  }

  return page;
}

export function PrivateRoute(page) {
  return resolveProtectedRoute(page);
}

