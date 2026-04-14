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

export function renderTaskCard(
  task,
  { escapeHtml = defaultEscapeHtml, formatDateTimeLabel = defaultFormatDateTimeLabel } = {},
) {
  const completionLabel = task?.completed ? "Concluida" : "Pendente";
  const toggleLabel = task?.completed ? "Reabrir" : "Concluir";

  return `
    <article class="agenda-list-item ${task?.completed ? "agenda-list-item-completed" : ""}">
      <div class="agenda-list-content">
        <div class="agenda-list-header">
          <h3>${escapeHtml(task?.title || "Sem titulo")}</h3>
          <span class="agenda-pill ${task?.completed ? "agenda-pill-success" : ""}">${completionLabel}</span>
        </div>
        <p>${escapeHtml(task?.description || "Sem descricao.")}</p>
        <div class="agenda-meta"><span><i class="fas fa-clock"></i> ${escapeHtml(formatDateTimeLabel(task?.due_date, "Sem prazo"))}</span></div>
      </div>
      <div class="agenda-actions">
        <button type="button" data-task-action="edit" data-task-id="${task?.id}">Editar</button>
        <button type="button" data-task-action="toggle" data-task-id="${task?.id}">${toggleLabel}</button>
        <button type="button" class="agenda-button-danger" data-task-action="delete" data-task-id="${task?.id}">Excluir</button>
      </div>
    </article>
  `;
}
