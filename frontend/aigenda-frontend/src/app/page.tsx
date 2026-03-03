import type { Metadata } from "next";
import Link from "next/link";

export const metadata: Metadata = {
  title: "AIGENDA | Início",
  description: "Página de entrada e navegação para autenticação e área interna.",
};

export default function Home() {
  return (
    <main className="mx-auto flex min-h-screen w-full max-w-3xl flex-col justify-center gap-6 px-6 py-16">
      <h1 className="text-3xl font-semibold tracking-tight">AIGENDA</h1>
      <p className="text-sm text-zinc-600 dark:text-zinc-400">
        Página de entrada para direcionar o usuário aos fluxos de autenticação
        e área autenticada.
      </p>

      <div className="flex flex-wrap gap-3">
        <Link className="rounded-md border px-4 py-2" href="/entrar">
          Entrar
        </Link>
        <Link className="rounded-md border px-4 py-2" href="/painel">
          Painel
        </Link>
        <Link className="rounded-md border px-4 py-2" href="/compromissos">
          Compromissos
        </Link>
        <Link className="rounded-md border px-4 py-2" href="/perfil">
          Perfil
        </Link>
      </div>
    </main>
  );
}
