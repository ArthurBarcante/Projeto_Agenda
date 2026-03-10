import React from "react"

export default function MetricCard({ titulo, valor }) {

  return (
    <div style={styles.card}>

      <p style={styles.titulo}>
        {titulo}
      </p>

      <h2 style={styles.valor}>
        {valor}
      </h2>

    </div>
  )
}

const styles = {

  card: {
    border: "1px solid #ddd",
    borderRadius: "10px",
    padding: "16px",
    width: "180px",
    backgroundColor: "#fff",
    boxShadow: "0 2px 6px rgba(0,0,0,0.05)",
    textAlign: "center"
  },

  titulo: {
    fontSize: "14px",
    marginBottom: "8px",
    color: "#666"
  },

  valor: {
    fontSize: "28px",
    fontWeight: "bold"
  }

}