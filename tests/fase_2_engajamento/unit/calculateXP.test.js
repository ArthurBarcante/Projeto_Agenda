import { afterEach, beforeEach, describe, expect, it, vi } from "vitest"
import {
  XP_VALUES,
  adicionarXP,
  calcularXP,
  criarRegistroXP
} from "../../../frontend/src/engagement/utils/calculateXP.js"

describe("engagement/utils/calculateXP", () => {
  beforeEach(() => {
    vi.useFakeTimers()
    vi.setSystemTime(new Date("2026-03-10T12:00:00Z"))
    vi.spyOn(Date, "now").mockReturnValue(123456)
  })

  afterEach(() => {
    vi.restoreAllMocks()
    vi.useRealTimers()
  })

  it("retorna o valor correto de XP por acao", () => {
    expect(XP_VALUES.compromissoConcluido).toBe(10)
    expect(calcularXP("metaConcluida")).toBe(50)
    expect(calcularXP("acaoInvalida")).toBe(0)
  })

  it("cria registro de XP com estrutura esperada", () => {
    const registro = criarRegistroXP("Compromisso concluido", 10)

    expect(registro).toEqual({
      id: 123456,
      motivo: "Compromisso concluido",
      xp: 10,
      data: "2026-03-10"
    })
  })

  it("adiciona XP ao total e insere novo registro no inicio", () => {
    const estadoInicial = {
      xpTotal: 120,
      historico: [{ id: 1, motivo: "Anterior", xp: 5, data: "2026-03-09" }]
    }

    const novoEstado = adicionarXP(
      estadoInicial,
      "Planejamento do dia",
      "planejamentoDia"
    )

    expect(novoEstado.xpTotal).toBe(125)
    expect(novoEstado.historico).toHaveLength(2)
    expect(novoEstado.historico[0]).toMatchObject({
      id: 123456,
      motivo: "Planejamento do dia",
      xp: 5,
      data: "2026-03-10"
    })
    expect(novoEstado.historico[1]).toEqual(estadoInicial.historico[0])
    expect(estadoInicial.xpTotal).toBe(120)
  })
})
