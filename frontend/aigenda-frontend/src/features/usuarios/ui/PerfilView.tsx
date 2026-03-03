import { PaginaBase } from "@/shared/components/PaginaBase";

export function PerfilView() {
  return (
    <PaginaBase
      titulo="Perfil"
      descricao="Dados do usuário autenticado e preferências básicas."
    >
      <section className="rounded-md border p-4 text-sm text-zinc-700 dark:text-zinc-200">
        Área reservada para perfil do usuário.
      </section>
    </PaginaBase>
  );
}
