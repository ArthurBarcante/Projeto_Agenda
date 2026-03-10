import React from "react"

export default function ProgressBar({ valor }) {

  return (
    <div style={styles.container}>

      <div
        style={{
          ...styles.progresso,
          width: `${valor}%`
        }}
      />

    </div>
  )
}

const styles = {

  container: {
    width: "100%",
    height: "10px",
    backgroundColor: "#eee",
    borderRadius: "10px",
    overflow: "hidden"
  },

  progresso: {
    height: "100%",
    backgroundColor: "#4CAF50",
    transition: "width 0.3s ease"
  }

}