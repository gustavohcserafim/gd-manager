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
        userRoleBadge.className = `badge ${user.role === 'Líder' ? 'badge-lider' : 'badge-nucleo'} text-[9px] py-0 px-1.5`;
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

  // 2. Service Worker Registration
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

  // 3. PWA Installation Prompt (beforeinstallprompt)
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
