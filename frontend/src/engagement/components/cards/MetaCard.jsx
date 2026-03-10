import React from "react"
import ProgressBar from "../progress/ProgressBar"

export default function MetaCard({
  meta,
  progresso,
  concluida,
  onProgresso
}) {

  return (
    <div style={styles.card}>

      <h3 style={styles.titulo}>
        {meta.titulo}
      </h3>

      <p style={styles.info}>
        Progresso: {meta.progresso} / {meta.objetivo}
      </p>

      <ProgressBar valor={progresso} />

      {concluida ? (
        <p style={styles.concluida}>
          ✅ Meta concluída
        </p>
      ) : (
        <button
          style={styles.botao}
          onClick={() => onProgresso(meta.id)}
        >
          + Progresso
        </button>
      )}

    </div>
  )
}


const styles = {

  card: {
    border: "1px solid #ddd",
    padding: "16px",
    borderRadius: "10px",
    marginBottom: "16px",
    backgroundColor: "#fff",
    boxShadow: "0 2px 6px rgba(0,0,0,0.05)"
  },

  titulo: {
    marginBottom: "8px"
  },

  info: {
    fontSize: "14px",
    marginBottom: "10px"
  },

  botao: {
    marginTop: "10px",
    padding: "8px 12px",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
    backgroundColor: "#4CAF50",
    color: "#fff"
  },

  concluida: {
    marginTop: "10px",
    color: "green",
    fontWeight: "bold"
  }

}