import { PainelView } from "@/features/compromissos/ui/PainelView";
import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "AIGENDA | Painel",
  description: "Página responsável pela visão geral da área autenticada.",
};

export default function PainelPage() {
  return <PainelView />;
}
