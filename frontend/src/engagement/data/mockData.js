// Dados simulados da aplicação

export const metasMock = [
  {
    id: 1,
    titulo: "Realizar 5 compromissos produtivos",
    tipo: "produtividade",
    objetivo: 5,
    progresso: 2,
    ativa: true
  },
  {
    id: 2,
    titulo: "Planejar agenda por 10 dias",
    tipo: "planejamento",
    objetivo: 10,
    progresso: 4,
    ativa: true
  }
]

export const xpMock = {
  xpTotal: 120,
  historico: [
    {
      id: 1,
      motivo: "Compromisso concluído",
      xp: 10,
      data: "2026-03-01"
    },
    {
      id: 2,
      motivo: "Sequência diária",
      xp: 20,
      data: "2026-03-02"
    }
  ]
}

export const desempenhoMock = {
  compromissosConcluidosSemana: 8,
  compromissosCanceladosSemana: 2
}

export const consistenciaMock = {
  streakAtual: 4,
  melhorStreak: 9,
  diasAtivos: [
    "2026-03-01",
    "2026-03-02",
    "2026-03-03",
    "2026-03-04"
  ]
}