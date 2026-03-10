import { useState, useEffect } from "react"
import { getMetas, salvarMetas } from "../services/agendaService"
import { calcularProgressoMeta, metaConcluida } from "../utils/calcularMetricas"

export default function useMetas() {

  const [metas, setMetas] = useState([])


  // Carregar metas ao iniciar
  useEffect(() => {

    const metasSalvas = getMetas()
    setMetas(metasSalvas)

  }, [])


  // Criar nova meta
  function criarMeta(titulo, tipo, objetivo) {

    const novaMeta = {
      id: Date.now(),
      titulo,
      tipo,
      objetivo,
      progresso: 0,
      ativa: true
    }

    const novasMetas = [...metas, novaMeta]

    setMetas(novasMetas)
    salvarMetas(novasMetas)

  }


  // Atualizar progresso de meta
  function atualizarProgresso(metaId, valor = 1) {

    const novasMetas = metas.map(meta => {

      if (meta.id === metaId) {

        const novoProgresso = meta.progresso + valor

        return {
          ...meta,
          progresso: novoProgresso
        }
      }

      return meta
    })

    setMetas(novasMetas)
    salvarMetas(novasMetas)

  }


  // Verificar progresso em %
  function progressoMeta(meta) {

    return calcularProgressoMeta(meta.progresso, meta.objetivo)

  }


  // Verificar se meta foi concluída
  function estaConcluida(meta) {

    return metaConcluida(meta)

  }


  return {
    metas,
    criarMeta,
    atualizarProgresso,
    progressoMeta,
    estaConcluida
  }

}