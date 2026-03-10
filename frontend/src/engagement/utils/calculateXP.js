// Valores de XP para cada ação do usuário

export const XP_VALUES = {
  compromissoConcluido: 10,
  planejamentoDia: 5,
  sequenciaDiaria: 20,
  metaConcluida: 50
}


// Calcula XP ganho por uma ação
export function calcularXP(acao) {
  return XP_VALUES[acao] || 0
}


// Cria registro no histórico de XP
export function criarRegistroXP(motivo, xp) {
  return {
    id: Date.now(),
    motivo: motivo,
    xp: xp,
    data: new Date().toISOString().split("T")[0]
  }
}


// Adiciona XP ao total
export function adicionarXP(estadoXP, motivo, acao) {

  const xpGanho = calcularXP(acao)

  const novoRegistro = criarRegistroXP(motivo, xpGanho)

  return {
    xpTotal: estadoXP.xpTotal + xpGanho,
    historico: [novoRegistro, ...estadoXP.historico]
  }

}