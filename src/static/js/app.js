import { initAuth } from "./auth.js";
import { initMembers } from "./members.js";
import { initHistory } from "./history.js";

document.addEventListener("DOMContentLoaded", () => {
  const pinScreen = document.getElementById("pin-screen");
  const appScreen = document.getElementById("app-screen");
  const userGreeting = document.getElementById("user-greeting");
  const userRoleBadge = document.getElementById("user-role-badge");
  const btnLogout = document.getElementById("btn-logout");
  const offlineBanner = document.getElementById("offline-banner");
  const installBtn = document.getElementById("btn-install-pwa");

  const membersController = initMembers();
  const historyController = initHistory();

  const authController = initAuth({
    onLoginSuccess: (user) => {
      pinScreen.classList.add("hidden");
      appScreen.classList.remove("hidden");
      if (userGreeting) userGreeting.textContent = user.name;
      if (userRoleBadge) {
        userRoleBadge.textContent = user.role;
        const roleClass = user.role === 'Líder' ? 'badge-lider' : user.role === 'Núcleo' ? 'badge-nucleo' : 'badge-membro';
        userRoleBadge.className = `badge ${roleClass} text-[9px] py-0 px-2`;
      }
      membersController.fetchMembers();
    },
    onLogout: () => {
      appScreen.classList.add("hidden");
      pinScreen.classList.remove("hidden");
    }
  });

  if (btnLogout) {
    btnLogout.addEventListener("click", () => {
      authController.logout();
    });
  }

  // 1. Online / Offline Connectivity Detection
  function updateOnlineStatus() {
    if (offlineBanner) {
      if (navigator.onLine) {
        offlineBanner.classList.add("hidden");
      } else {
        offlineBanner.classList.remove("hidden");
      }
    }
  }

  window.addEventListener("online", updateOnlineStatus);
  window.addEventListener("offline", updateOnlineStatus);
  updateOnlineStatus();

  // 2. Official Glassmorphic Toast Notification System
  window.showToast = function (message, type = "success") {
    let container = document.getElementById("toast-container");
    if (!container) {
      container = document.createElement("div");
      container.id = "toast-container";
      container.className = "fixed bottom-5 right-5 z-50 flex flex-col gap-2 pointer-events-none";
      document.body.appendChild(container);
    }

    const toast = document.createElement("div");
    toast.className = "pointer-events-auto inline-flex items-center gap-3 px-4 py-2.5 rounded-2xl bg-white/10 backdrop-blur-md border border-white/20 shadow-glass text-white transition-all transform duration-300 opacity-0 translate-y-2";
    
    const dotColor = type === "error" ? "bg-rose-400" : "bg-onda-mint";
    const label = type === "error" ? "Aviso" : "Sucesso";

    toast.innerHTML = `
      <div class="w-7 h-7 rounded-full bg-gradient-to-tr from-onda-blue-800 to-onda-blue-500 flex items-center justify-center shrink-0 shadow-inner">
        <div class="w-2.5 h-2.5 rounded-full ${dotColor}"></div>
      </div>
      <div class="flex flex-col text-left pr-2">
        <span class="text-[10px] font-system font-medium text-onda-blue-light uppercase tracking-wider">${label}</span>
        <span class="text-xs font-sans font-medium text-white">${message}</span>
      </div>
    `;

    container.appendChild(toast);
    requestAnimationFrame(() => {
      toast.classList.remove("opacity-0", "translate-y-2");
      toast.classList.add("opacity-100", "translate-y-0");
    });

    setTimeout(() => {
      toast.classList.remove("opacity-100", "translate-y-0");
      toast.classList.add("opacity-0", "translate-y-2");
      setTimeout(() => toast.remove(), 300);
    }, 3500);
  };

  // 3. Service Worker Registration
  if ("serviceWorker" in navigator) {
    window.addEventListener("load", () => {
      navigator.serviceWorker
        .register("/sw.js")
        .then((registration) => {
          console.log("Service Worker registrado com sucesso:", registration.scope);
        })
        .catch((err) => {
          console.warn("Falha ao registrar Service Worker:", err);
        });
    });
  }

  // 4. PWA Installation Prompt (beforeinstallprompt)
  let deferredPrompt = null;
  window.addEventListener("beforeinstallprompt", (e) => {
    e.preventDefault();
    deferredPrompt = e;
    if (installBtn) {
      installBtn.classList.remove("hidden");
      installBtn.addEventListener("click", async () => {
        installBtn.classList.add("hidden");
        if (deferredPrompt) {
          deferredPrompt.prompt();
          const choiceResult = await deferredPrompt.userChoice;
          console.log("Install prompt result:", choiceResult.outcome);
          deferredPrompt = null;
        }
      });
    }
  });

  window.addEventListener("appinstalled", () => {
    console.log("PWA instalada com sucesso");
    if (installBtn) installBtn.classList.add("hidden");
  });
});
