import { useState, useEffect } from "react"
import { getXP, salvarXP } from "../services/agendaService"
import { adicionarXP } from "../utils/calcularXP"

export default function useXP() {

  const [xpData, setXpData] = useState({
    xpTotal: 0,
    historico: []
  })


  // carregar XP ao iniciar
  useEffect(() => {

    const xpSalvo = getXP()
    setXpData(xpSalvo)

  }, [])


  // adicionar XP por uma ação
  function ganharXP(motivo, acao) {

    const novoEstado = adicionarXP(xpData, motivo, acao)

    setXpData(novoEstado)
    salvarXP(novoEstado)

  }


  return {
    xpTotal: xpData.xpTotal,
    historicoXP: xpData.historico,
    ganharXP
  }

}