import { apiFetch } from "./api.js";

export function initHistory() {
  const tabMembers = document.getElementById("tab-members");
  const tabHistory = document.getElementById("tab-history");
  const viewMembers = document.getElementById("view-members");
  const viewHistory = document.getElementById("view-history");
  const timeline = document.getElementById("history-timeline");
  const historyEmpty = document.getElementById("history-empty");

  function switchTab(target) {
    if (target === "history") {
      tabMembers.classList.remove("border-onda-blue-500", "text-white", "font-semibold");
      tabMembers.classList.add("border-transparent", "text-white/60", "font-medium");

      tabHistory.classList.remove("border-transparent", "text-white/60", "font-medium");
      tabHistory.classList.add("border-onda-blue-500", "text-white", "font-semibold");

      viewMembers.classList.add("hidden");
      viewHistory.classList.remove("hidden");
      fetchHistory();
    } else {
      tabHistory.classList.remove("border-onda-blue-500", "text-white", "font-semibold");
      tabHistory.classList.add("border-transparent", "text-white/60", "font-medium");

      tabMembers.classList.remove("border-transparent", "text-white/60", "font-medium");
      tabMembers.classList.add("border-onda-blue-500", "text-white", "font-semibold");

      viewHistory.classList.add("hidden");
      viewMembers.classList.remove("hidden");
    }
  }

  tabMembers.addEventListener("click", () => switchTab("members"));
  tabHistory.addEventListener("click", () => switchTab("history"));

  async function fetchHistory() {
    try {
      const logs = await apiFetch("/api/history?limit=50");
      renderHistory(logs);
    } catch (err) {
      timeline.innerHTML = `<div class="text-xs text-rose-400 p-3 bg-rose-500/10 rounded-xl">Não foi possível carregar o histórico: ${err.message}</div>`;
    }
  }

  function renderHistory(logs) {
    timeline.innerHTML = "";

    if (!logs || logs.length === 0) {
      historyEmpty.classList.remove("hidden");
      return;
    }
    historyEmpty.classList.add("hidden");

    logs.forEach(item => {
      const isCreate = item.actionType === "CREATE_MEMBER";
      const isUpdate = item.actionType === "UPDATE_MEMBER";
      const isDelete = item.actionType === "DELETE_MEMBER";

      const badgeColor = isCreate ? "bg-onda-mint/20 text-onda-mint border-onda-mint/40" :
                         isUpdate ? "bg-onda-blue-600/30 text-onda-blue-light border-onda-blue-500/50" :
                         "bg-rose-500/20 text-rose-300 border-rose-500/40";

      const actionLabel = isCreate ? "Novo Membro" :
                          isUpdate ? "Edição" : "Remoção";

      const dateStr = formatDate(item.timestamp);

      const entry = document.createElement("div");
      entry.className = "glass-card p-3.5 flex items-start justify-between gap-3 text-white";
      entry.innerHTML = `
        <div class="flex-1 min-w-0">
          <div class="flex items-center gap-2 mb-1">
            <span class="badge ${badgeColor} text-[9px] py-0 px-2">${actionLabel}</span>
            <span class="font-sans text-xs font-bold text-white">${escapeHtml(item.memberName)}</span>
          </div>
          <p class="font-sans text-xs text-onda-offwhite/90">${escapeHtml(item.details || "")}</p>
          <div class="flex items-center gap-2 mt-1.5 font-system text-[11px] text-onda-blue-light">
            <span>Por <strong class="text-white">${escapeHtml(item.userName)}</strong></span>
            <span>•</span>
            <span>${dateStr}</span>
          </div>
        </div>
      `;
      timeline.appendChild(entry);
    });
  }

  function formatDate(isoStr) {
    if (!isoStr) return "";
    try {
      const d = new Date(isoStr);
      return d.toLocaleDateString("pt-BR", {
        day: "2-digit",
        month: "2-digit",
        year: "numeric",
        hour: "2-digit",
        minute: "2-digit"
      });
    } catch (e) {
      return isoStr;
    }
  }

  function escapeHtml(str) {
    if (!str) return "";
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  return {
    fetchHistory,
    switchTab
  };
}
