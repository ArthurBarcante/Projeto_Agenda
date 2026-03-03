import { EntrarView } from "@/features/autenticacao/ui/EntrarView";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AIGENDA | Entrar",
  description: "Página responsável pelo fluxo de autenticação do usuário.",
};

export default function EntrarPage() {
  return <EntrarView />;
}
