import { CompromissosView } from "@/features/compromissos/ui/CompromissosView";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AIGENDA | Compromissos",
  description: "Página responsável pela listagem e navegação dos compromissos.",
};

export default function CompromissosPage() {
  return <CompromissosView />;
}
