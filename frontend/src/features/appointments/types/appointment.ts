export type AppointmentStatusAlias = "scheduled" | "cancelled" | "completed";

export type AppointmentApi = {
  id: string;
  company_id: string;
  creator_id: string;
  title: string;
  description: string | null;
  start_time: string;
  end_time: string;
  start_time?: string;
  end_time?: string;
  status: AppointmentStatusAlias;
  created_at: string;
  updated_at: string;
};
