import { metasMock, xpMock, desempenhoMock, consistenciaMock } from "../data/mockData"


const STORAGE_KEYS = {
  metas: "agenda_metas",
  xp: "agenda_xp",
  consistencia: "agenda_consistencia"
}


// Inicializa dados no localStorage se não existirem
function inicializarDados() {

  if (!localStorage.getItem(STORAGE_KEYS.metas)) {
    localStorage.setItem(STORAGE_KEYS.metas, JSON.stringify(metasMock))
  }

  if (!localStorage.getItem(STORAGE_KEYS.xp)) {
    localStorage.setItem(STORAGE_KEYS.xp, JSON.stringify(xpMock))
  }

  if (!localStorage.getItem(STORAGE_KEYS.consistencia)) {
    localStorage.setItem(STORAGE_KEYS.consistencia, JSON.stringify(consistenciaMock))
  }

}


// ====================
// METAS
// ====================

export function getMetas() {

  inicializarDados()

  const metas = localStorage.getItem(STORAGE_KEYS.metas)

  return JSON.parse(metas)
}


export function salvarMetas(metas) {

  localStorage.setItem(STORAGE_KEYS.metas, JSON.stringify(metas))

}


// ====================
// XP
// ====================

export function getXP() {

  inicializarDados()

  const xp = localStorage.getItem(STORAGE_KEYS.xp)

  return JSON.parse(xp)
}


export function salvarXP(xp) {

  localStorage.setItem(STORAGE_KEYS.xp, JSON.stringify(xp))

}


// ====================
// CONSISTÊNCIA
// ====================

export function getConsistencia() {

  inicializarDados()

  const consistencia = localStorage.getItem(STORAGE_KEYS.consistencia)

  return JSON.parse(consistencia)
}


export function salvarConsistencia(consistencia) {

  localStorage.setItem(
    STORAGE_KEYS.consistencia,
    JSON.stringify(consistencia)
  )

}