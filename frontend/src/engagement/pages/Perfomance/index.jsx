import React, { useEffect } from "react"

export default function XpToast({ mensagem, xp, onClose }) {

  useEffect(() => {

    const timer = setTimeout(() => {
      onClose()
    }, 3000)

    return () => clearTimeout(timer)

  }, [onClose])


  return (
    <div style={styles.toast}>

      <strong style={styles.xp}>
        +{xp} XP
      </strong>

      <p style={styles.mensagem}>
        {mensagem}
      </p>

    </div>
  )
}


const styles = {

  toast: {
    position: "fixed",
    bottom: "20px",
    right: "20px",
    backgroundColor: "#333",
    color: "#fff",
    padding: "16px",
    borderRadius: "10px",
    boxShadow: "0 4px 10px rgba(0,0,0,0.2)",
    minWidth: "180px",
    animation: "fadeIn 0.3s ease"
  },

  xp: {
    color: "#4CAF50",
    fontSize: "18px"
  },

  mensagem: {
    marginTop: "4px",
    fontSize: "14px"
  }

}