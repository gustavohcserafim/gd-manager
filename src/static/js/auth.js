import { apiFetch, setSession, clearSession, getStoredToken, getStoredUser } from "./api.js";

let currentPin = "";
let lockoutInterval = null;

export function initAuth({ onLoginSuccess, onLogout }) {
  const pinScreen = document.getElementById("pin-screen");
  const pinDisplay = document.getElementById("pin-dots");
  const pinError = document.getElementById("pin-error");
  const keypad = document.getElementById("pin-keypad");

  // Check if session already exists
  const token = getStoredToken();
  const user = getStoredUser();
  if (token && user) {
    onLoginSuccess(user);
    return;
  }

  function updatePinDisplay() {
    pinDisplay.innerHTML = "";
    for (let i = 0; i < 4; i++) {
      const dot = document.createElement("div");
      dot.className = `w-4 h-4 rounded-full border-2 border-slate-400 ${i < currentPin.length ? "bg-amber-500 border-amber-500 scale-110" : "bg-transparent"} transition-all duration-150`;
      pinDisplay.appendChild(dot);
    }
  }

  async function submitPin() {
    pinError.classList.add("hidden");
    pinError.textContent = "";

    try {
      const data = await apiFetch("/api/auth/pin", {
        method: "POST",
        body: JSON.stringify({ pin: currentPin })
      });

      setSession(data.token, data.user);
      currentPin = "";
      updatePinDisplay();
      onLoginSuccess(data.user);
    } catch (err) {
      currentPin = "";
      updatePinDisplay();

      if (err.status === 429) {
        startLockout(30);
      } else {
        pinError.textContent = err.message || "PIN inválido. Tente novamente.";
        pinError.classList.remove("hidden");
        // Shake animation
        pinDisplay.classList.add("animate-shake");
        setTimeout(() => pinDisplay.classList.remove("animate-shake"), 500);
      }
    }
  }

  function startLockout(seconds) {
    let remaining = seconds;
    pinError.textContent = `Muitas tentativas. Aguarde ${remaining}s.`;
    pinError.classList.remove("hidden");
    disableKeypad(true);

    if (lockoutInterval) clearInterval(lockoutInterval);
    lockoutInterval = setInterval(() => {
      remaining--;
      if (remaining <= 0) {
        clearInterval(lockoutInterval);
        pinError.classList.add("hidden");
        disableKeypad(false);
      } else {
        pinError.textContent = `Muitas tentativas. Aguarde ${remaining}s.`;
      }
    }, 1000);
  }

  function disableKeypad(disabled) {
    const buttons = keypad.querySelectorAll("button");
    buttons.forEach(btn => btn.disabled = disabled);
  }

  // Keypad click handler
  keypad.addEventListener("click", (e) => {
    const btn = e.target.closest("button");
    if (!btn || btn.disabled) return;

    const val = btn.dataset.val;
    if (val === "backspace") {
      currentPin = currentPin.slice(0, -1);
      updatePinDisplay();
    } else if (val === "clear") {
      currentPin = "";
      updatePinDisplay();
    } else if (val && currentPin.length < 4) {
      currentPin += val;
      updatePinDisplay();
      if (currentPin.length === 4) {
        submitPin();
      }
    }
  });

  // Physical keyboard support
  window.addEventListener("keydown", (e) => {
    if (!pinScreen.classList.contains("hidden")) {
      if (e.key >= "0" && e.key <= "9" && currentPin.length < 4) {
        currentPin += e.key;
        updatePinDisplay();
        if (currentPin.length === 4) submitPin();
      } else if (e.key === "Backspace") {
        currentPin = currentPin.slice(0, -1);
        updatePinDisplay();
      }
    }
  });

  updatePinDisplay();

  // Return logout trigger
  return {
    logout: () => {
      clearSession();
      currentPin = "";
      updatePinDisplay();
      onLogout();
    }
  };
}
