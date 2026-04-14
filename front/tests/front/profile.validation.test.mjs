import assert from "node:assert/strict";
import test from "node:test";

import {
  formatBirthdateInput,
  formatBirthdateLabel,
  normalizeProfilePayload,
  sanitizePhone,
  validateProfilePayload,
} from "../../pages/profile/validation.mjs";

test("normalizeProfilePayload normaliza email e birthdate", () => {
  const payload = normalizeProfilePayload({
    name: "  Arthur  ",
    email: " USER@Example.COM ",
    phone: "(11) 99999-0000",
    birthdate: "2000-01-02T12:00:00Z",
  });

  assert.deepEqual(payload, {
    name: "Arthur",
    email: "user@example.com",
    phone: "(11) 99999-0000",
    birthdate: "2000-01-02",
  });
});

test("sanitizePhone remove caracteres nao numericos", () => {
  assert.equal(sanitizePhone("(11) 99999-0000"), "11999990000");
});

test("formatBirthdateLabel converte para dd/mm/aaaa", () => {
  assert.equal(formatBirthdateLabel("2000-01-02"), "02/01/2000");
  assert.equal(formatBirthdateInput("2000-01-02T10:30:00Z"), "2000-01-02");
});

test("validateProfilePayload rejeita email invalido e telefone curto", () => {
  const result = validateProfilePayload({
    name: "Ar",
    email: "invalido",
    phone: "123",
    birthdate: "2050-01-01",
  });

  assert.equal(result.isValid, false);
  assert.equal(result.errors.name, "Informe um nome com pelo menos 3 caracteres.");
  assert.equal(result.errors.email, "Informe um email valido.");
  assert.equal(result.errors.phone, "Informe um telefone com DDD e 10 ou 11 digitos.");
  assert.equal(result.errors.birthdate, "A data de nascimento nao pode estar no futuro.");
});

test("validateProfilePayload detecta ausencia de mudancas", () => {
  const currentUser = {
    name: "Arthur",
    email: "arthur@example.com",
    phone: "(11) 99999-0000",
    birthdate: "2000-01-02",
  };

  const result = validateProfilePayload({ ...currentUser }, currentUser);

  assert.equal(result.isValid, true);
  assert.equal(result.hasChanges, false);
});

test("validateProfilePayload aceita payload valido com mudancas", () => {
  const currentUser = {
    name: "Arthur",
    email: "arthur@example.com",
    phone: "(11) 99999-0000",
    birthdate: "2000-01-02",
  };

  const result = validateProfilePayload({
    name: "Arthur Silva",
    email: "arthur.silva@example.com",
    phone: "(11) 98888-7777",
    birthdate: "2000-01-02",
  }, currentUser);

  assert.equal(result.isValid, true);
  assert.equal(result.hasChanges, true);
  assert.deepEqual(result.payload, {
    name: "Arthur Silva",
    email: "arthur.silva@example.com",
    phone: "(11) 98888-7777",
    birthdate: "2000-01-02",
  });
});
