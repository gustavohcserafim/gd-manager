# Igreja Onda — Digital UI & Design System Prompt Guidelines

> **Contexto para Agentes de IA:**  
> Siga rigorosamente este guia técnico extraído do *Brandbook Oficial 2027* em qualquer prototipagem, código (React, Tailwind CSS, HTML/CSS) ou especificação de design.

---

## 1. Filosofia de Marca & Tom de Interface

- **Identidade:** Simples, objetiva, clara e original. Sem ruídos ou excessos religiosos ("sem rodeios").
- **Conceito Visual:** **Onda de Impacto / Choque** (origem, propagação, expansão contínua e transformação).
- **Atmosfera Digital:** Tecnológica, acolhedora, imersiva, moderna e dinâmica.
- **Microcópia (Tone of Voice):** Direta, inspiradora, bíblica e acolhedora (ex.: *"Viva o extraordinário"*, *"Você não precisa caminhar sozinho"*).

---

## 2. Regras do Logotipo em Interfaces

- **Logotipo Principal (Digital):** Wordmark horizontal `"igreja onda"`. **Sempre em minúsculas**.
- **Versão Secundária (Empilhada):** **NÃO USAR EM INTERFACES DIGITAIS.** A versão empilhada é de uso estritamente impresso.
- **Área de Proteção Mínima:** Distância equivalente à letra `$X$` (altura-x do logotipo) em todos os quatro cantos.
- **Proporção da Grelha:** Altura total proporcional de $1{,}78X$ e largura total de $8{,}53X$.
- **Hierarquia Visual:** O logotipo `"igreja onda"` deve ter prioridade máxima de leitura. Grafismos nunca competem com o logotipo nem atuam como assinatura substituta (única exceção prevista: *Onda Store*).
- **Restrição Crucial:** **Nunca** recrie o logo apenas digitando o texto com fontes do sistema. Sempre use SVG vetorial original. Não rotacione, não crie contorno (*outline*), não distorça e garanta alto contraste com o fundo.

---

## 3. Tokens de Cor (Design Tokens)

### 3.1. Paleta Principal (Cores Primárias)

| Nome do Token | HEX | Descrição & Uso Recomendado |
| :--- | :--- | :--- |
| `--color-onda-blue-900` | `#181e5f` | Azul profundo escuro: fundos escuros, base de gradientes, superfícies de alto contraste |
| `--color-onda-blue-800` | `#11187e` | Azul marinho profundo: gradientes, fundos de cartões e barras de navegação |
| `--color-onda-blue-700` | `#2027a7` | Azul real intermediário: estados de foco e gradientes médios |
| `--color-onda-blue-600` | `#1f2bc8` | **Azul Primário Oficial**: botões de ação (CTA), links e destaques principais |
| `--color-onda-blue-500` | `#2537de` | Azul elétrico vibrante: hover states, acentos dinâmicos e brilhos |
| `--color-onda-offwhite` | `#eeeee7` | Superfície clara institucional, fundos alternativos e textos em fundos escuros |
| `--color-onda-dark` | `#161616` | Preto carvão para tipografia escura sobre superfícies claras e temas dark |

### 3.2. Paleta Secundária & Acentos

| Nome do Token | HEX | Função na UI |
| :--- | :--- | :--- |
| `--color-onda-accent-mint` | `#79caab` | Tags de status positivo, badges de confirmação |
| `--color-onda-accent-cream` | `#ffffe6` | Destaques suaves e detalhes de iluminação sutil |
| `--color-onda-cyan-100` | `#e5f4fe` | Fundo de badges sutis, containers informativos |
| `--color-onda-cyan-200` | `#e3f3f7` | Superfícies glassmórficas claras |
| `--color-onda-blue-light` | `#9cc7e4` | Ícones secundários, legendas claras em cards azuis |
| `--color-onda-white` | `#ffffff` | Branco puro para textos de máxima ênfase e contornos translúcidos |

---

## 4. Tipografia & Hierarquia de Texto

| Família Tipográfica | Função | Regras de Estilo | Fallbacks |
| :--- | :--- | :--- | :--- |
| **Space Grotesk** | Títulos gerais, subtítulos, corpo de texto, botões e formulários | Caixa normal / sentence case. Tracking regular | `sans-serif` |
| **Right Grotesk Compact Black** | Títulos de grande impacto (*Hero section*, destaques de eventos, CTAs centrais) | **SEMPRE EM MAIÚSCULAS** (`uppercase`). Peso Black/900 | `"Arial Black"`, `sans-serif` |
| **Right Grotesk Tight Dark** | Títulos condensados, frases de impacto verticais | **SEMPRE EM MAIÚSCULAS** (`uppercase`). Altura condensada | `"Impact"`, `sans-serif` |
| **SF Pro Display** | Legendas, notas de rodapé, timestamps (*"1h ago"*), micro-tags | Caixa normal, peso 400 ou 500, alta legibilidade em pequenas escalas | `-apple-system`, `BlinkMacSystemFont`, `"Inter"`, `sans-serif` |

---

## 5. Linguagem Visual: Glassmorphism & Gradients

### 5.1. Diretrizes de Glassmorphism (Assinatura UI da Marca)
A identidade da Igreja Onda adota o **Glassmorphism** como elemento visual central para cartões, pills de notificação, modais e barras flutuantes:
- **Translucidez:** Fundos com opacidade entre $10\%$ e $30\%$ sobre fundos de gradiente azul.
- **Desfoque (*Backdrop Blur*):** Mínimo de `backdrop-blur-md` ($12\text{px}$) a `backdrop-blur-xl` ($24\text{px}$).
- **Borda de Contorno Sutil:** Bordas finas ($1\text{px}$) translúcidas brancas (`rgba(255, 255, 255, 0.15)`) ou azul claro para criar o efeito de aresta vítrea.
- **Raios de Arredondamento:** Cantos arredondados orgânicos e elegantes:
  - Pills e Notificações: `rounded-full` ($9999\text{px}$) ou `rounded-2xl` ($16\text{px}$).
  - Cards e Modais: `rounded-2xl` ($16\text{px}$) a `rounded-3xl` ($24\text{px}$).

### 5.2. Gradientes de Propagação
Simulam a propagação contínua da onda:
- **Fundo Principal (Dark Wave):** Linear ou Mesh de `#181e5f` $\rightarrow$ `#11187e` $\rightarrow$ `#1f2bc8`.
- **Destaque Dinâmico:** Radiais de `#2537de` com opacidade difusa posicionados em cantos superiores ou como *glow* sob cards vítreos.

### 5.3. Grafismo de Apoio (Ondas Concêntricas)
- Padrão de anéis esféricos e círculos concêntricos descentralizados que representam origem, propagação e impacto.
- Aplicar com opacidade suave ($5\%$ a $20\%$) em fundos de seção, mantendo o contraste dos textos intacto.

---

## 6. Configuração para Tailwind CSS (v3 / v4)

Incorpore este bloco no arquivo `tailwind.config.js`:

```javascript
/** @type {import('tailwindcss').Config} */
module.exports = {
  theme: {
    extend: {
      colors: {
        onda: {
          blue: {
            900: '#181e5f',
            800: '#11187e',
            700: '#2027a7',
            600: '#1f2bc8', // Primário
            500: '#2537de', // Elétrico / Accent
            light: '#9cc7e4',
          },
          offwhite: '#eeeee7',
          dark: '#161616',
          mint: '#79caab',
          cream: '#ffffe6',
          cyan: {
            50: '#e5f4fe',
            100: '#e3f3f7',
          }
        }
      },
      fontFamily: {
        sans: ['"Space Grotesk"', 'sans-serif'],
        display: ['"Right Grotesk Compact Black"', '"Space Grotesk"', 'sans-serif'],
        condensed: ['"Right Grotesk Tight Dark"', '"Space Grotesk"', 'sans-serif'],
        system: ['"SF Pro Display"', '-apple-system', 'BlinkMacSystemFont', 'sans-serif'],
      },
      boxShadow: {
        'glass': '0 8px 32px 0 rgba(0, 0, 0, 0.25)',
        'glass-glow': '0 0 24px rgba(37, 55, 222, 0.35)',
      }
    }
  }
}
```

---

## 7. Exemplos de Componentes UI Canônicos

### 7.1. Pill de Notificação / Lembrete (Estilo Glassmorphism Oficial)

```html
<div class="inline-flex items-center gap-3 px-4 py-3 rounded-2xl bg-white/10 backdrop-blur-md border border-white/20 shadow-glass text-white transition hover:bg-white/15">
  <!-- Ícone de onda esférica -->
  <div class="w-8 h-8 rounded-full bg-gradient-to-tr from-onda-blue-800 to-onda-blue-500 flex items-center justify-center shrink-0 shadow-inner">
    <div class="w-3.5 h-3.5 rounded-full bg-onda-blue-900 border border-white/40"></div>
  </div>
  
  <div class="flex flex-col text-left">
    <div class="flex items-center gap-2">
      <span class="text-xs font-system font-medium text-onda-blue-light">Lembrete</span>
      <span class="text-[10px] font-system text-white/50">1h atrás</span>
    </div>
    <span class="text-sm font-sans font-medium text-white">Domingo 18h, culto igreja onda</span>
  </div>

  <svg class="w-4 h-4 ml-auto text-white/60" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
  </svg>
</div>
```

### 7.2. Card de Culto / Programação

```html
<div class="relative overflow-hidden rounded-3xl bg-white/10 backdrop-blur-lg border border-white/15 p-6 shadow-glass text-white">
  <!-- Horário com Right Grotesk -->
  <div class="flex items-baseline justify-between mb-4">
    <h3 class="font-display uppercase text-4xl tracking-tight text-white">19h</h3>
    <span class="px-3 py-1 rounded-full text-xs font-system bg-onda-blue-600/80 text-white backdrop-blur-sm border border-white/20">
      Ao Vivo
    </span>
  </div>
  
  <p class="text-base font-sans font-medium text-white/90 mb-1">Pregação com Pastor Lipão</p>
  <p class="text-xs font-system text-onda-blue-light mb-6">Batismos após o culto</p>
  
  <!-- Botão de Ação -->
  <button class="w-full py-3 px-5 rounded-xl bg-onda-blue-600 hover:bg-onda-blue-500 font-sans font-semibold text-sm transition-all duration-200 shadow-md flex items-center justify-center gap-2">
    Definir Lembrete
  </button>
</div>
```

---

## 8. Checklist de Validação para a IA

Antes de entregar qualquer código de interface, verifique:
1. [ ] O logo `"igreja onda"` está em caixa baixa e na horizontal?
2. [ ] A tipografia dos títulos principais está usando Space Grotesk ou Right Grotesk (em caixa alta)?
3. [ ] Os containers de destaque aplicam a estética de *Glassmorphism* (`backdrop-blur`, fundo translúcido e borda translúcida sutil)?
4. [ ] O contraste mínimo de acessibilidade (WCAG AA) está garantido entre os azuis e o texto?
5. [ ] Elementos gráficos concêntricos estão atuando apenas como apoio e não competem com a legibilidade?