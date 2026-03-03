import { PaginaBase } from "@/shared/components/PaginaBase";

export function EntrarView() {
  return (
    <PaginaBase
      titulo="Entrar"
      descricao="Autenticação por empresa, e-mail e senha."
    >
      <section className="rounded-md border p-4 text-sm text-zinc-700 dark:text-zinc-200">
        Área reservada para formulário de autenticação.
      </section>
    </PaginaBase>
  );
}
