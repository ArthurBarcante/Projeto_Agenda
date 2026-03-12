export type AppointmentStatus = "scheduled" | "cancelled" | "completed";

export type AppointmentApi = {
  id: string;
  company_id: string;
  creator_id: string;
  title: string;
  description: string | null;
  start_time: string;
  end_time: string;
  status: AppointmentStatus;
  created_at: string;
  updated_at: string;
};

export type Appointment = {
  id: string;
  title: string;
  startAt: string;
  endAt: string;
  status: AppointmentStatus;
};
