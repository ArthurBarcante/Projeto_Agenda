import { describe, expect, it } from "vitest"
import {
  atualizarStreak,
  hoje,
  saoDiasConsecutivos
} from "../../../frontend/src/engagement/utils/calculateStreak.js"

describe("engagement/utils/calculateStreak", () => {
  it("identifica dias consecutivos corretamente", () => {
    expect(saoDiasConsecutivos("2026-03-09", "2026-03-10")).toBe(true)
    expect(saoDiasConsecutivos("2026-03-09", "2026-03-11")).toBe(false)
  })

  it("inicia streak quando nao ha atividade anterior", () => {
    const consistencia = {
      streakAtual: 0,
      melhorStreak: 0,
      diasAtivos: []
    }

    const atualizado = atualizarStreak(consistencia, "2026-03-10")

    expect(atualizado).toEqual({
      streakAtual: 1,
      melhorStreak: 1,
      diasAtivos: ["2026-03-10"]
    })
  })

  it("nao altera estado quando data ja foi registrada", () => {
    const consistencia = {
      streakAtual: 2,
      melhorStreak: 3,
      diasAtivos: ["2026-03-09", "2026-03-10"]
    }

    const atualizado = atualizarStreak(consistencia, "2026-03-10")

    expect(atualizado).toBe(consistencia)
  })

  it("incrementa streak em dia consecutivo e atualiza melhorStreak", () => {
    const consistencia = {
      streakAtual: 2,
      melhorStreak: 2,
      diasAtivos: ["2026-03-08", "2026-03-09"]
    }

    const atualizado = atualizarStreak(consistencia, "2026-03-10")

    expect(atualizado).toEqual({
      streakAtual: 3,
      melhorStreak: 3,
      diasAtivos: ["2026-03-08", "2026-03-09", "2026-03-10"]
    })
  })

  it("reinicia streak quando ha quebra de sequencia", () => {
    const consistencia = {
      streakAtual: 4,
      melhorStreak: 7,
      diasAtivos: ["2026-03-02", "2026-03-03", "2026-03-04", "2026-03-05"]
    }

    const atualizado = atualizarStreak(consistencia, "2026-03-10")

    expect(atualizado).toEqual({
      streakAtual: 1,
      melhorStreak: 7,
      diasAtivos: [
        "2026-03-02",
        "2026-03-03",
        "2026-03-04",
        "2026-03-05",
        "2026-03-10"
      ]
    })
  })

  it("retorna hoje no formato YYYY-MM-DD", () => {
    const valor = hoje()
    expect(valor).toMatch(/^\d{4}-\d{2}-\d{2}$/)
  })
})
