import { isAuthenticated } from "../core/configs/auth.js";

if (!isAuthenticated()) {
  if (typeof window.loadPage === "function") {
    window.loadPage("login");
  } else {
    window.location.href = "./index.html#/login";
  }

  throw new Error("Acesso nao autorizado a agenda.");
}
