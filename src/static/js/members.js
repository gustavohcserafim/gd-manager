import { apiFetch } from "./api.js";

const LOCAL_STORAGE_MEMBERS = "gd_cached_members";

let currentFilter = "";
let currentSearch = "";
let membersCache = [];

export function initMembers() {
  const membersList = document.getElementById("members-list");
  const emptyState = document.getElementById("empty-state");
  const membersCount = document.getElementById("members-count");
  const searchInput = document.getElementById("search-input");
  const filterChips = document.querySelectorAll(".filter-chip");

  const btnAddMember = document.getElementById("btn-add-member");
  const memberModal = document.getElementById("member-modal");
  const modalClose = document.getElementById("modal-close");
  const modalCancel = document.getElementById("modal-cancel");
  const memberForm = document.getElementById("member-form");
  const formError = document.getElementById("form-error");

  const formId = document.getElementById("member-id");
  const formName = document.getElementById("form-name");
  const formPhone = document.getElementById("form-phone");
  const formBirthdate = document.getElementById("form-birthdate");
  const formPosition = document.getElementById("form-position");
  const modalTitle = document.getElementById("modal-title");

  // Phone input mask
  formPhone.addEventListener("input", (e) => {
    let val = e.target.value.replace(/\D/g, "").slice(0, 11);
    if (val.length > 10) {
      val = val.replace(/^(\d{2})(\d{5})(\d{4})/, "($1) $2-$3");
    } else if (val.length > 6) {
      val = val.replace(/^(\d{2})(\d{4})(\d{0,4})/, "($1) $2-$3");
    } else if (val.length > 2) {
      val = val.replace(/^(\d{2})(\d{0,5})/, "($1) $2");
    } else if (val.length > 0) {
      val = val.replace(/^(\d*)/, "($1");
    }
    e.target.value = val;
  });

  // Birthday input mask
  formBirthdate.addEventListener("input", (e) => {
    let val = e.target.value.replace(/\D/g, "").slice(0, 8);
    if (val.length > 4) {
      val = val.replace(/^(\d{2})(\d{2})(\d{0,4})/, "$1/$2/$3");
    } else if (val.length > 2) {
      val = val.replace(/^(\d{2})(\d{0,2})/, "$1/$2");
    }
    e.target.value = val;
  });

  // Modal controls
  function openModal(isEdit = false, member = null) {
    formError.classList.add("hidden");
    formError.textContent = "";

    if (isEdit && member) {
      modalTitle.textContent = "Editar Membro";
      formId.value = member.id;
      formName.value = member.name;
      formPhone.value = member.phoneFormatted;
      formBirthdate.value = member.birthDate;
      formPosition.value = member.position;
    } else {
      modalTitle.textContent = "Novo Membro";
      formId.value = "";
      memberForm.reset();
      formPosition.value = "Membro";
    }
    memberModal.classList.remove("hidden");
    formName.focus();
  }

  function closeModal() {
    memberModal.classList.add("hidden");
  }

  btnAddMember.addEventListener("click", () => openModal(false));
  modalClose.addEventListener("click", closeModal);
  modalCancel.addEventListener("click", closeModal);

  // Form submit (Add or Edit)
  memberForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    formError.classList.add("hidden");
    formError.textContent = "";

    const id = formId.value;
    const isEdit = Boolean(id);

    const payload = {
      name: formName.value.trim(),
      phone: formPhone.value.trim(),
      birthDate: formBirthdate.value.trim(),
      position: formPosition.value
    };

    try {
      if (isEdit) {
        await apiFetch(`/api/members/${id}`, {
          method: "PUT",
          body: JSON.stringify(payload)
        });
      } else {
        await apiFetch("/api/members", {
          method: "POST",
          body: JSON.stringify(payload)
        });
      }

      closeModal();
      await fetchMembers();
    } catch (err) {
      formError.textContent = err.message || "Ocorreu um erro ao salvar o membro.";
      formError.classList.remove("hidden");
    }
  });

  // Load and render members
  async function fetchMembers() {
    try {
      const url = new URL("/api/members", window.location.origin);
      if (currentSearch) url.searchParams.set("search", currentSearch);
      if (currentFilter) url.searchParams.set("position", currentFilter);

      const data = await apiFetch(url.toString());
      membersCache = data;
      localStorage.setItem(LOCAL_STORAGE_MEMBERS, JSON.stringify(data));
      renderMembers(data);
    } catch (err) {
      // Fallback to cached members if offline
      const cached = localStorage.getItem(LOCAL_STORAGE_MEMBERS);
      if (cached) {
        try {
          membersCache = JSON.parse(cached);
          renderMembers(filterLocal(membersCache));
        } catch (e) {}
      }
    }
  }

  function filterLocal(list) {
    return list.filter(m => {
      const matchSearch = !currentSearch || m.name.toLowerCase().includes(currentSearch.toLowerCase());
      const matchPos = !currentFilter || m.position === currentFilter;
      return matchSearch && matchPos;
    });
  }

  function renderMembers(members) {
    membersCount.textContent = members.length;
    membersList.innerHTML = "";

    if (members.length === 0) {
      emptyState.classList.remove("hidden");
      return;
    }
    emptyState.classList.add("hidden");

    members.forEach(member => {
      const badgeClass =
        member.position === "Líder" ? "badge-lider" :
        member.position === "Núcleo" ? "badge-nucleo" : "badge-membro";

      const card = document.createElement("div");
      card.className = "glass-card p-4 flex items-center justify-between gap-3 hover:bg-white/[0.13] hover:border-white/25 transition duration-200 text-white";
      card.innerHTML = `
        <div class="flex-1 min-w-0">
          <div class="flex items-center gap-2 mb-1.5">
            <h3 class="text-sm font-sans font-bold text-onda-offwhite truncate">${escapeHtml(member.name)}</h3>
            <span class="badge ${badgeClass} text-[9px] py-0 px-2">${escapeHtml(member.position)}</span>
          </div>
          <div class="flex flex-wrap items-center gap-x-4 gap-y-1 font-system text-xs text-onda-blue-light">
            <span class="flex items-center gap-1.5">
              <svg class="w-3.5 h-3.5 text-onda-blue-light/70" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z"/>
              </svg>
              ${escapeHtml(member.phoneFormatted)}
            </span>
            <span class="flex items-center gap-1.5">
              <svg class="w-3.5 h-3.5 text-onda-blue-light/70" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"/>
              </svg>
              ${escapeHtml(member.birthDate)}
            </span>
          </div>
        </div>

        <div class="flex items-center gap-1.5">
          <!-- WHATSAPP QUICK ACTION -->
          <a href="${member.whatsappUrl}" target="_blank" rel="noopener noreferrer" title="Abrir conversa no WhatsApp" class="p-2 text-onda-mint hover:text-white bg-onda-mint/15 hover:bg-onda-mint/25 border border-onda-mint/30 rounded-xl transition shadow-sm">
            <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24">
              <path d="M12.031 6.172c-3.181 0-5.767 2.586-5.768 5.766-.001 1.298.38 2.27 1.019 3.287l-.582 2.128 2.182-.573c.978.58 1.911.928 3.145.929 3.178 0 5.767-2.587 5.768-5.766.001-3.187-2.575-5.77-5.764-5.771zm3.392 8.244c-.144.405-.837.774-1.17.824-.299.045-.677.063-1.092-.069-.252-.08-.575-.187-.988-.365-1.739-.751-2.874-2.502-2.961-2.617-.087-.116-.708-.94-.708-1.793s.448-1.273.607-1.446c.159-.173.346-.217.462-.217l.332.007c.101.005.237-.038.37.283.138.334.472 1.15.513 1.236.041.086.069.188.012.302-.057.114-.086.185-.171.285l-.26.302c-.087.098-.179.205-.077.38.102.175.454.748.974 1.212.671.597 1.237.783 1.412.87.175.087.278.073.38-.044.103-.117.442-.513.56-.688.118-.175.237-.146.401-.086.164.06 1.042.492 1.22.58.178.088.297.132.341.206.044.074.044.428-.1.833z"/>
            </svg>
          </a>

          <!-- EDIT ACTION -->
          <button data-action="edit" data-id="${member.id}" title="Editar" class="p-2 text-white/70 hover:text-white hover:bg-white/10 rounded-xl transition">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
            </svg>
          </button>

          <!-- DELETE ACTION -->
          <button data-action="delete" data-id="${member.id}" data-name="${escapeHtml(member.name)}" title="Remover" class="p-2 text-white/50 hover:text-rose-400 hover:bg-rose-500/20 rounded-xl transition">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
            </svg>
          </button>
        </div>
      `;
      membersList.appendChild(card);
    });
  }

  function escapeHtml(str) {
    if (!str) return "";
    return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  // Filter chips click
  filterChips.forEach(chip => {
    chip.addEventListener("click", () => {
      filterChips.forEach(c => {
        c.classList.remove("bg-onda-blue-600", "text-white", "font-semibold", "shadow-sm", "bg-amber-500", "text-slate-950", "font-bold");
        c.classList.add("bg-white/10", "text-white/80", "font-medium");
      });
      chip.classList.remove("bg-white/10", "text-white/80", "font-medium", "bg-slate-800", "text-slate-300");
      chip.classList.add("bg-onda-blue-600", "text-white", "font-semibold", "shadow-sm");

      currentFilter = chip.dataset.filter || "";
      fetchMembers();
    });
  });

  // Debounced search
  let searchTimeout = null;
  searchInput.addEventListener("input", (e) => {
    clearTimeout(searchTimeout);
    searchTimeout = setTimeout(() => {
      currentSearch = e.target.value.trim();
      fetchMembers();
    }, 250);
  });

  // Card actions delegation (Edit / Delete)
  membersList.addEventListener("click", (e) => {
    const editBtn = e.target.closest("button[data-action='edit']");
    if (editBtn) {
      const id = parseInt(editBtn.dataset.id, 10);
      const member = membersCache.find(m => m.id === id);
      if (member) openModal(true, member);
      return;
    }

    const deleteBtn = e.target.closest("button[data-action='delete']");
    if (deleteBtn) {
      const id = parseInt(deleteBtn.dataset.id, 10);
      const name = deleteBtn.dataset.name;
      window.dispatchEvent(new CustomEvent("gd:confirm-delete", { detail: { id, name } }));
    }
  });

  // Listen to login event
  window.addEventListener("gd:login-success", () => {
    fetchMembers();
  });

  // Delete modal confirmation
  const deleteModal = document.getElementById("delete-modal");
  const deleteMemberName = document.getElementById("delete-member-name");
  const btnCancelDelete = document.getElementById("btn-cancel-delete");
  const btnConfirmDelete = document.getElementById("btn-confirm-delete");
  let memberToDeleteId = null;

  window.addEventListener("gd:confirm-delete", (e) => {
    const { id, name } = e.detail;
    memberToDeleteId = id;
    deleteMemberName.textContent = name;
    deleteModal.classList.remove("hidden");
  });

  function closeDeleteModal() {
    deleteModal.classList.add("hidden");
    memberToDeleteId = null;
  }

  btnCancelDelete.addEventListener("click", closeDeleteModal);

  btnConfirmDelete.addEventListener("click", async () => {
    if (!memberToDeleteId) return;
    try {
      await apiFetch(`/api/members/${memberToDeleteId}`, {
        method: "DELETE"
      });
      closeDeleteModal();
      await fetchMembers();
    } catch (err) {
      alert(err.message || "Não foi possível remover o membro.");
      closeDeleteModal();
    }
  });

  return {
    fetchMembers,
    openModal
  };

}
