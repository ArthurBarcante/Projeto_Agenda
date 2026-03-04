import { useEffect, useState } from "react";

import { listarCompromissos } from "@/features/compromissos/services/compromissosService";
import type { CompromissoApi } from "@/features/compromissos/types/compromisso";

export function useCompromissos() {
  const [itens, setItens] = useState<CompromissoApi[]>([]);
  const [carregando, setCarregando] = useState<boolean>(true);

  useEffect(() => {
    let ativo = true;

    async function carregarCompromissos() {
      try {
        const resposta = await listarCompromissos();
        if (ativo) {
          setItens(resposta);
        }
      } finally {
        if (ativo) {
          setCarregando(false);
        }
      }
    }

    void carregarCompromissos();

    return () => {
      ativo = false;
    };
  }, []);

  return { itens, carregando };
}
