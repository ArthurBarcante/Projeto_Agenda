export type StatusCompromisso = "scheduled" | "cancelled" | "completed";

export type CompromissoApi = {
  id: string;
  company_id: string;
  creator_id: string;
  title: string;
  description: string | null;
  start_time: string;
  end_time: string;
  starts_at?: string;
  ends_at?: string;
  status: StatusCompromisso;
  created_at: string;
  updated_at: string;
};
