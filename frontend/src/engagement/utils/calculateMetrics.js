// Verifica se duas datas são dias consecutivos
export function saoDiasConsecutivos(dataAnterior, dataAtual) {
  const d1 = new Date(dataAnterior)
  const d2 = new Date(dataAtual)

  const diff = (d2 - d1) / (1000 * 60 * 60 * 24)

  return diff === 1
}


// Atualiza a sequência de consistência
export function atualizarStreak(consistencia, dataAtual) {

  const diasAtivos = [...consistencia.diasAtivos]

  const ultimaData = diasAtivos[diasAtivos.length - 1]

  // se não houver atividade anterior
  if (!ultimaData) {
    return {
      ...consistencia,
      streakAtual: 1,
      melhorStreak: Math.max(consistencia.melhorStreak, 1),
      diasAtivos: [dataAtual]
    }
  }

  // se já registrou hoje
  if (ultimaData === dataAtual) {
    return consistencia
  }

  // se for consecutivo
  if (saoDiasConsecutivos(ultimaData, dataAtual)) {

    const novoStreak = consistencia.streakAtual + 1

    return {
      ...consistencia,
      streakAtual: novoStreak,
      melhorStreak: Math.max(consistencia.melhorStreak, novoStreak),
      diasAtivos: [...diasAtivos, dataAtual]
    }
  }

  // sequência quebrada
  return {
    ...consistencia,
    streakAtual: 1,
    diasAtivos: [...diasAtivos, dataAtual]
  }
}


// Retorna data de hoje formatada
export function hoje() {
  return new Date().toISOString().split("T")[0]
}