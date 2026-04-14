export function getLocalItem(key) {
  return localStorage.getItem(key);
}

export function setLocalItem(key, value) {
  localStorage.setItem(key, value);
}

export function removeLocalItem(key) {
  localStorage.removeItem(key);
}

export function getSessionItem(key) {
  return sessionStorage.getItem(key);
}

export function setSessionItem(key, value) {
  sessionStorage.setItem(key, value);
}

export function removeSessionItem(key) {
  sessionStorage.removeItem(key);
}

export function getLocalJson(key) {
  const value = getLocalItem(key);

  if (!value) {
    return null;
  }

  try {
    return JSON.parse(value);
  } catch (error) {
    console.error("Falha ao ler valor salvo:", error);
    removeLocalItem(key);
    return null;
  }
}

export function setLocalJson(key, value) {
  setLocalItem(key, JSON.stringify(value));
}