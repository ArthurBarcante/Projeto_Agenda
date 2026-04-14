function defaultEscapeHtml(value = "") {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function defaultFormatDateTimeLabel(_, fallback = "Sem data definida") {
  return fallback;
}

export function renderEventCard(
  calendarEvent,
  { escapeHtml = defaultEscapeHtml, formatDateTimeLabel = defaultFormatDateTimeLabel } = {},
) {
  return `
    <article class="agenda-list-item">
      <div class="agenda-list-content">
        <div class="agenda-list-header">
          <h3>${escapeHtml(calendarEvent?.title || "Sem titulo")}</h3>
          <span class="agenda-pill agenda-pill-accent">Evento</span>
        </div>
        <p>${escapeHtml(calendarEvent?.description || "Sem descricao.")}</p>
        <div class="agenda-meta">
          <span><i class="fas fa-play"></i> ${escapeHtml(formatDateTimeLabel(calendarEvent?.start_at, "Sem inicio"))}</span>
          <span><i class="fas fa-stop"></i> ${escapeHtml(formatDateTimeLabel(calendarEvent?.end_at, "Sem fim"))}</span>
          <span><i class="fas fa-location-dot"></i> ${escapeHtml(calendarEvent?.location || "Sem local")}</span>
        </div>
      </div>
      <div class="agenda-actions">
        <button type="button" data-event-action="edit" data-event-id="${calendarEvent?.id}">Editar</button>
        <button type="button" class="agenda-button-danger" data-event-action="delete" data-event-id="${calendarEvent?.id}">Excluir</button>
      </div>
    </article>
  `;
}
