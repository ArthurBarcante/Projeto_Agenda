const EMAIL_PATTERN = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export function formatBirthdateInput(value) {
  if (!value) {
    return "";
  }

  const rawValue = String(value).trim();
  if (/^\d{4}-\d{2}-\d{2}$/.test(rawValue)) {
    return rawValue;
  }

  const parsed = new Date(rawValue);
  if (Number.isNaN(parsed.getTime())) {
    return "";
  }

  return parsed.toISOString().slice(0, 10);
}

export function formatBirthdateLabel(value) {
  const normalizedValue = formatBirthdateInput(value);
  if (!normalizedValue) {
    return "Nao informado";
  }

  const [year, month, day] = normalizedValue.split("-");
  return `${day}/${month}/${year}`;
}

export function sanitizePhone(value = "") {
  return String(value).replace(/\D/g, "");
}

export function normalizeProfilePayload(rawPayload = {}) {
  return {
    name: String(rawPayload.name || "").trim(),
    email: String(rawPayload.email || "").trim().toLowerCase(),
    phone: String(rawPayload.phone || "").trim(),
    birthdate: formatBirthdateInput(rawPayload.birthdate),
  };
}

export function validateProfilePayload(rawPayload, currentUser = {}) {
  const payload = normalizeProfilePayload(rawPayload);
  const errors = {};

  if (payload.name.length < 3) {
    errors.name = "Informe um nome com pelo menos 3 caracteres.";
  }

  if (!EMAIL_PATTERN.test(payload.email)) {
    errors.email = "Informe um email valido.";
  }

  const phoneDigits = sanitizePhone(payload.phone);
  if (phoneDigits.length < 10 || phoneDigits.length > 11) {
    errors.phone = "Informe um telefone com DDD e 10 ou 11 digitos.";
  }

  if (!payload.birthdate) {
    errors.birthdate = "Informe uma data de nascimento valida.";
  } else {
    const birthdate = new Date(`${payload.birthdate}T00:00:00`);
    const now = new Date();
    if (birthdate > now) {
      errors.birthdate = "A data de nascimento nao pode estar no futuro.";
    }
  }

  const currentPayload = normalizeProfilePayload({
    name: currentUser.name,
    email: currentUser.email,
    phone: currentUser.phone,
    birthdate: currentUser.birthdate,
  });

  const hasChanges = Object.keys(payload).some((key) => payload[key] !== currentPayload[key]);

  return {
    errors,
    hasChanges,
    isValid: Object.keys(errors).length === 0,
    payload,
  };
}
