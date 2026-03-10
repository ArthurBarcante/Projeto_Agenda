import { useState, useEffect } from "react"
import { getConsistencia, salvarConsistencia } from "../services/agendaService"
import { atualizarStreak, hoje } from "../utils/calcularStreak"

export default function useConsistencia() {

  const [consistencia, setConsistencia] = useState({
    streakAtual: 0,
    melhorStreak: 0,
    diasAtivos: []
  })


  // carregar dados ao iniciar
  useEffect(() => {

    const dados = getConsistencia()
    setConsistencia(dados)

  }, [])


  // registrar atividade do dia
  function registrarAtividade() {

    const dataHoje = hoje()

    const novaConsistencia = atualizarStreak(consistencia, dataHoje)

    setConsistencia(novaConsistencia)
    salvarConsistencia(novaConsistencia)

  }


  return {
    streakAtual: consistencia.streakAtual,
    melhorStreak: consistencia.melhorStreak,
    diasAtivos: consistencia.diasAtivos,
    registrarAtividade
  }

}