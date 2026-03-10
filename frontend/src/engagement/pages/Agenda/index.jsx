import React from "react"
import useConsistencia from "../../hooks/useConsistencia"

export default function ConsistenciaPage() {

  const {
    streakAtual,
    melhorStreak,
    diasAtivos,
    registrarAtividade
  } = useConsistencia()


  return (

    <div style={styles.container}>

      <h1>Consistência</h1>


      <div style={styles.cards}>

        <div style={styles.card}>
          <p>🔥 Sequência atual</p>
          <h2>{streakAtual} dias</h2>
        </div>

        <div style={styles.card}>
          <p>🏆 Melhor sequência</p>
          <h2>{melhorStreak} dias</h2>
        </div>

      </div>


      <button
        style={styles.botao}
        onClick={registrarAtividade}
      >
        Registrar atividade de hoje
      </button>


      <div style={styles.historico}>

        <h3>Dias ativos</h3>

        {diasAtivos.length === 0 ? (
          <p>Nenhuma atividade registrada</p>
        ) : (
          <ul>

            {diasAtivos.map((dia, index) => (
              <li key={index}>{dia}</li>
            ))}

          </ul>
        )}

      </div>

    </div>

  )
}


const styles = {

  container: {
    padding: "30px",
    maxWidth: "700px",
    margin: "0 auto"
  },

  cards: {
    display: "flex",
    gap: "20px",
    marginTop: "20px",
    marginBottom: "30px"
  },

  card: {
    border: "1px solid #ddd",
    borderRadius: "10px",
    padding: "20px",
    width: "200px",
    backgroundColor: "#fff",
    boxShadow: "0 2px 6px rgba(0,0,0,0.05)"
  },

  botao: {
    padding: "10px 16px",
    border: "none",
    borderRadius: "6px",
    backgroundColor: "#4CAF50",
    color: "#fff",
    cursor: "pointer",
    marginBottom: "30px"
  },

  historico: {
    marginTop: "20px"
  }

}