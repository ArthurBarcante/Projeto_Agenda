import React from "react"

export default function XpCard({ xpTotal, historico }) {

  return (
    <div style={styles.card}>

      <h3 style={styles.titulo}>
        XP Total
      </h3>

      <h1 style={styles.xp}>
        {xpTotal} XP
      </h1>

      <div style={styles.historico}>

        <p style={styles.subtitulo}>
          Histórico recente
        </p>

        {historico.length === 0 ? (
          <p style={styles.vazio}>
            Nenhum XP ganho ainda
          </p>
        ) : (
          historico.slice(0, 5).map(registro => (
            <div key={registro.id} style={styles.item}>

              <span>
                +{registro.xp} XP
              </span>

              <small style={styles.motivo}>
                {registro.motivo}
              </small>

            </div>
          ))
        )}

      </div>

    </div>
  )
}

const styles = {

  card: {
    border: "1px solid #ddd",
    borderRadius: "10px",
    padding: "20px",
    backgroundColor: "#fff",
    boxShadow: "0 2px 6px rgba(0,0,0,0.05)",
    width: "250px"
  },

  titulo: {
    marginBottom: "8px"
  },

  xp: {
    marginBottom: "16px",
    color: "#4CAF50"
  },

  historico: {
    marginTop: "10px"
  },

  subtitulo: {
    fontSize: "14px",
    marginBottom: "8px"
  },

  item: {
    display: "flex",
    justifyContent: "space-between",
    marginBottom: "6px"
  },

  motivo: {
    color: "#666"
  },

  vazio: {
    fontSize: "14px",
    color: "#999"
  }

}