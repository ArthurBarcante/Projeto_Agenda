import { beforeEach, describe, expect, it } from "vitest"
import {
  consistenciaMock,
  metasMock,
  xpMock
} from "../../../frontend/src/engagement/data/mockData.js"
import {
  getConsistencia,
  getMetas,
  getXP,
  salvarConsistencia,
  salvarMetas,
  salvarXP
} from "../../../frontend/src/engagement/services/agendaService.js"

describe("engagement/services/agendaService", () => {
  beforeEach(() => {
    localStorage.clear()
  })

  it("inicializa e retorna metas quando storage esta vazio", () => {
    const metas = getMetas()

    expect(metas).toEqual(metasMock)
    expect(JSON.parse(localStorage.getItem("agenda_metas"))).toEqual(metasMock)
  })

  it("salva metas no storage", () => {
    const novasMetas = [{ id: 99, titulo: "Nova meta", ativa: true }]

    salvarMetas(novasMetas)

    expect(JSON.parse(localStorage.getItem("agenda_metas"))).toEqual(novasMetas)
    expect(getMetas()).toEqual(novasMetas)
  })

  it("inicializa e retorna dados de XP", () => {
    const xp = getXP()

    expect(xp).toEqual(xpMock)
    expect(JSON.parse(localStorage.getItem("agenda_xp"))).toEqual(xpMock)
  })

  it("salva dados de XP", () => {
    const novoXP = { xpTotal: 999, historico: [] }

    salvarXP(novoXP)

    expect(JSON.parse(localStorage.getItem("agenda_xp"))).toEqual(novoXP)
    expect(getXP()).toEqual(novoXP)
  })

  it("inicializa e retorna consistencia", () => {
    const consistencia = getConsistencia()

    expect(consistencia).toEqual(consistenciaMock)
    expect(JSON.parse(localStorage.getItem("agenda_consistencia"))).toEqual(
      consistenciaMock
    )
  })

  it("salva consistencia", () => {
    const novaConsistencia = {
      streakAtual: 10,
      melhorStreak: 10,
      diasAtivos: ["2026-03-10"]
    }

    salvarConsistencia(novaConsistencia)

    expect(JSON.parse(localStorage.getItem("agenda_consistencia"))).toEqual(
      novaConsistencia
    )
    expect(getConsistencia()).toEqual(novaConsistencia)
  })
})
