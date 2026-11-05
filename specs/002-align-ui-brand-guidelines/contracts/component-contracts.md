# UI Component Contracts: Align UI & Frontend with Brand Guidelines

**Feature**: `002-align-ui-brand-guidelines`
**Date**: 2026-11-05

This document defines the DOM structure, required CSS classes, and visual contracts for every core UI element in GD Manager, adhering to `igreja_onda_ui_brand_guidelines.md`.

---

## 1. Top Navigation Bar with Authentic Wordmark

```html
<header class="sticky top-0 z-40 bg-onda-blue-900/80 backdrop-blur-md border-b border-white/10 shadow-glass">
  <div class="max-w-4xl mx-auto px-4 h-16 flex items-center justify-between">
    <!-- Brand identity: horizontal lowercase wordmark + sub-label -->
    <div class="flex items-center gap-3">
      <!-- Authentic horizontal vector logo -->
      <svg class="h-6 w-auto text-onda-offwhite" viewBox="0 0 240 48" fill="currentColor">
        <!-- Igreja Onda horizontal lowercase vector path -->
      </svg>
      <div class="border-l border-white/20 pl-2.5">
        <span class="font-display uppercase tracking-tight text-sm font-black text-white">GD Manager</span>
        <p class="font-system text-[10px] text-onda-blue-light leading-none">Onda Mooca</p>
      </div>
    </div>

    <!-- Actions & User Profile -->
    <div class="flex items-center gap-3">
      <!-- Install PWA button -->
      <button id="btn-install-pwa" class="hidden px-3 py-1.5 rounded-full bg-white/10 backdrop-blur-md border border-white/20 text-onda-offwhite hover:bg-white/15 text-xs font-sans font-medium transition">
        Instalar App
      </button>

      <!-- User status -->
      <div class="text-right hidden sm:block">
        <p id="user-greeting" class="text-xs font-sans font-medium text-onda-offwhite">Pr. Pedro</p>
        <span id="user-role-badge" class="badge-lider text-[9px]">Líder</span>
      </div>

      <!-- Logout / Lock -->
      <button id="btn-logout" class="p-2 text-white/60 hover:text-white rounded-xl hover:bg-white/10 transition">
        <!-- SVG lock icon -->
      </button>
    </div>
  </div>

  <!-- Navigation Tabs -->
  <div class="max-w-4xl mx-auto px-4 flex border-t border-white/10">
    <button id="tab-members" class="tab-btn active py-3 px-6 text-xs font-sans font-semibold border-b-2 border-onda-blue-500 text-white flex items-center gap-2">
      Membros (<span id="members-count">0</span>)
    </button>
    <button id="tab-history" class="tab-btn py-3 px-6 text-xs font-sans font-medium border-b-2 border-transparent text-white/60 hover:text-white flex items-center gap-2">
      Histórico de Atividades
    </button>
  </div>
</header>
```

---

## 2. PIN Lock Screen (Access Screen)

```html
<div id="pin-screen" class="fixed inset-0 z-50 bg-gradient-to-br from-onda-blue-900 via-onda-blue-800 to-onda-blue-900 flex flex-col items-center justify-center p-6">
  <!-- Concentric waves background graphics with low opacity -->
  <div class="absolute inset-0 pointer-events-none opacity-10 flex items-center justify-center">
    <!-- SVG concentric rings pattern -->
  </div>

  <!-- Glassmorphic Keypad Container -->
  <div class="relative w-full max-w-xs flex flex-col items-center text-center p-6 rounded-3xl bg-white/10 backdrop-blur-xl border border-white/15 shadow-glass">
    <!-- Glowing brand wave emblem -->
    <div class="w-16 h-16 rounded-full bg-gradient-to-tr from-onda-blue-800 to-onda-blue-500 flex items-center justify-center shadow-glass-glow mb-4">
      <div class="w-7 h-7 rounded-full bg-onda-blue-900 border border-white/40 flex items-center justify-center">
        <!-- Lock icon -->
      </div>
    </div>

    <!-- Title with Right Grotesk uppercase -->
    <h1 class="font-display uppercase text-2xl tracking-tight text-white mb-1">GD Manager</h1>
    <p class="font-system text-xs text-onda-blue-light mb-6">Igreja Onda Mooca • Acesso de Líderes</p>

    <!-- PIN dots -->
    <div id="pin-dots" class="flex gap-4 justify-center mb-6 h-6"></div>

    <!-- Error message -->
    <div id="pin-error" class="hidden text-rose-400 text-xs font-sans font-medium mb-4 min-h-[1.25rem]"></div>

    <!-- Keypad numbers -->
    <div id="pin-keypad" class="grid grid-cols-3 gap-3 w-full">
      <button data-val="1" class="h-13 rounded-2xl bg-white/10 hover:bg-white/20 active:bg-white/30 border border-white/10 text-2xl font-sans font-semibold text-white transition-all">1</button>
      <!-- Numbers 2-9, Clear, 0, Backspace -->
    </div>
  </div>
</div>
```

---

## 3. Glassmorphic Member Card

```html
<article class="relative overflow-hidden rounded-2xl bg-white/10 backdrop-blur-md border border-white/15 p-4 shadow-glass hover:bg-white/[0.13] transition text-white">
  <div class="flex items-start justify-between gap-3">
    <div class="flex items-center gap-3">
      <!-- Member Avatar with subtle wave ring -->
      <div class="w-10 h-10 rounded-full bg-gradient-to-tr from-onda-blue-800 to-onda-blue-600 flex items-center justify-center text-sm font-bold text-white border border-white/30">
        JM
      </div>
      <div>
        <h4 class="font-sans font-semibold text-sm text-onda-offwhite">João Mendes</h4>
        <span class="badge-lider text-[9px] mt-0.5">Líder</span>
      </div>
    </div>

    <!-- Action buttons -->
    <div class="flex items-center gap-1">
      <button class="btn-edit p-1.5 rounded-lg hover:bg-white/15 text-white/70 hover:text-white transition">
        <!-- Edit icon -->
      </button>
      <button class="btn-delete p-1.5 rounded-lg hover:bg-rose-500/20 text-white/50 hover:text-rose-400 transition">
        <!-- Trash icon -->
      </button>
    </div>
  </div>

  <div class="mt-3 pt-3 border-t border-white/10 grid grid-cols-2 gap-2 font-system text-xs text-onda-blue-light">
    <div>📞 (11) 98765-4321</div>
    <div class="text-right">📅 Membro desde 2024</div>
  </div>
</article>
```

---

## 4. Primary Action Button & Notification Pill

```html
<!-- Primary Action Button (Onda Blue 600 CTA) -->
<button class="py-2.5 px-4 rounded-xl bg-onda-blue-600 hover:bg-onda-blue-500 active:bg-onda-blue-700 font-sans font-semibold text-xs text-white shadow-md transition-all duration-200 flex items-center justify-center gap-2">
  <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="2.5" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" d="M12 4v16m8-8H4"/>
  </svg>
  <span>Novo Membro</span>
</button>

<!-- Official Notification Pill -->
<div class="inline-flex items-center gap-3 px-4 py-2.5 rounded-2xl bg-white/10 backdrop-blur-md border border-white/20 shadow-glass text-white">
  <div class="w-7 h-7 rounded-full bg-gradient-to-tr from-onda-blue-800 to-onda-blue-500 flex items-center justify-center shrink-0">
    <div class="w-3 h-3 rounded-full bg-onda-mint"></div>
  </div>
  <div class="flex flex-col text-left">
    <div class="flex items-center gap-2">
      <span class="text-xs font-system font-medium text-onda-blue-light">Sucesso</span>
      <span class="text-[10px] font-system text-white/50">agora</span>
    </div>
    <span class="text-xs font-sans font-medium text-white">Membro cadastrado com sucesso</span>
  </div>
</div>
```
