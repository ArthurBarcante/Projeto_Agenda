import Link from "next/link";

import { PaginaBase } from "@/shared/components/PaginaBase";

export function PainelView() {
  return (
    <PaginaBase
      titulo="Painel"
      descricao="Resumo operacional com atalhos para os fluxos principais."
    >
      <section className="flex flex-wrap gap-3">
        <Link className="rounded-md border px-4 py-2" href="/compromissos">
          Ver compromissos
        </Link>
        <Link className="rounded-md border px-4 py-2" href="/perfil">
          Ver perfil
        </Link>
      </section>
    </PaginaBase>
  );
}
