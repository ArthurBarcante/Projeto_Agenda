import { useState, useEffect } from "react"
import { calcularResumoSemana } from "../utils/calcularMetricas"

export default function useDesempenho(compromissos = []) {

  const [metricas, setMetricas] = useState({
    concluidos: 0,
    cancelados: 0,
    taxaSucesso: 0
  })


  // recalcular métricas sempre que compromissos mudarem
  useEffect(() => {

    const resumo = calcularResumoSemana(compromissos)

    setMetricas(resumo)

  }, [compromissos])


  return {
    compromissosConcluidos: metricas.concluidos,
    compromissosCancelados: metricas.cancelados,
    taxaSucesso: metricas.taxaSucesso
  }

}