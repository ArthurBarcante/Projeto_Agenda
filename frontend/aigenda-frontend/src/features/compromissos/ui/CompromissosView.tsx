import { PaginaBase } from "@/shared/components/PaginaBase";

export function CompromissosView() {
  return (
    <PaginaBase
      titulo="Compromissos"
      descricao="Lista, filtros e navegação dos compromissos."
    >
      <section className="rounded-md border p-4 text-sm text-zinc-700 dark:text-zinc-200">
        Área reservada para listagem de compromissos.
      </section>
    </PaginaBase>
  );
}
