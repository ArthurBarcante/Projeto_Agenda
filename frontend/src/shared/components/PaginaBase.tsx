type PaginaBaseProps = {
  titulo: string;
  descricao: string;
  children?: React.ReactNode;
};

export function PaginaBase({ titulo, descricao, children }: PaginaBaseProps) {
  return (
    <main className="mx-auto flex min-h-screen w-full max-w-4xl flex-col gap-6 px-6 py-10">
      <header className="space-y-2">
        <h1 className="text-2xl font-semibold tracking-tight">{titulo}</h1>
        <p className="text-sm text-zinc-600 dark:text-zinc-400">{descricao}</p>
      </header>
      {children}
    </main>
  );
}
