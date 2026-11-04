<!--
Sync Impact Report:
- Version change: Unratified (template) → 1.0.0
- List of modified principles:
  - [PRINCIPLE_1_NAME] → I. Clean Architecture e Separação Estrita de Responsabilidades
  - [PRINCIPLE_2_NAME] → II. Test-Driven Development (TDD) Mandatório e Inegociável
  - [PRINCIPLE_3_NAME] → III. Mobile-First e Multiplataforma (Flutter iOS e Android)
  - [PRINCIPLE_4_NAME] → IV. Eficiência Máxima de Custos de Infraestrutura e Hospedagem
  - [PRINCIPLE_5_NAME] → V. Parcimônia Extrema e Justificativa de Dependências Externas
- Added sections:
  - Diretrizes Tecnológicas e Restrições de Engenharia
  - Fluxo de Desenvolvimento e Quality Gates
- Removed sections: Nenhuma (scaffold inicial preenchido integralmente).
- Follow-up TODOs: Nenhum.
-->

# GD Manager Constitution

## Core Principles

### I. Clean Architecture e Separação Estrita de Responsabilidades
Tanto a base de código frontend (Flutter) quanto o backend (Python 3) DEVEM estruturar-se sob os princípios formais da Clean Architecture. As regras de negócio e entidades de domínio DEVEM ser mantidas puras, isoladas de frameworks, bibliotecas visuais de UI, detalhes de persistência e chamadas de rede. O fluxo de dependências DEVE apontar exclusivamente para dentro (em direção ao domínio e casos de uso). Camadas externas (Data, Infrastructure, UI) comunicam-se com o Core somente por meio de abstrações, interfaces ou portas (Ports and Adapters).
*Rationale*: Garante independência tecnológica, estabilidade de regras de negócio, alta testabilidade em isolamento e facilidade de refatoração ou evolução sem acoplamentos nocivos.

### II. Test-Driven Development (TDD) Mandatório e Inegociável
Nenhuma funcionalidade, comportamento ou regra de negócio DEVE ser codificada sem que o teste automatizado correspondente tenha sido previamente escrito e executado com falha comprovada (ciclo Red-Green-Refactor). O desenvolvimento DEVE seguir rigorosamente a sequência: 1. Escrever o teste unitário/de especificação; 2. Confirmar a falha do teste; 3. Implementar a lógica mínima necessária para o teste passar; 4. Refatorar o código preservando os testes verdes. Casos de borda e validações de regras de negócio DEVEM ter cobertura completa demonstrável antes de qualquer mesclagem de código.
*Rationale*: O TDD assegura que os requisitos sejam claramente compreendidos antes da escrita do código de produção, previne regressões precocemente e orienta o design para componentes pequenos, coesos e desacoplados.

### III. Mobile-First e Multiplataforma (Flutter iOS e Android)
O produto GD Manager DEVE ser concebido, desenhado e implementado com mentalidade Mobile-First, assegurando paridade de funcionalidade e experiência fluida e nativa tanto em iOS quanto em Android utilizando Flutter. As interfaces de usuário DEVEM priorizar usabilidade por toque, responsividade a múltiplos formatos e densidades de tela, desempenho constante de renderização (60/120 fps) e tratamento resiliente para cenários de conectividade instável ou offline.
*Rationale*: O acesso principal dos usuários se dá via dispositivos móveis; manter paridade rigorosa entre iOS e Android a partir de uma única base de código Flutter reduz tempo de entrega e evita fragmentação de produto.

### IV. Eficiência Máxima de Custos de Infraestrutura e Hospedagem
O backend e a infraestrutura de suporte DEVEM ser desenhados e executados visando o menor custo financeiro possível de hospedagem e operação. DEVE-SE priorizar arquiteturas leves, computação sob demanda (serverless), modelos de baixo consumo de recursos e planos de hospedagem gratuitos ou de custo mínimo viável. Decisões que envolvam instâncias sobrecarregadas, serviços proprietários caros ou infraestrutura complexa são expressamente PROIBIDAS sem justificativa formal de inviabilidade técnica de alternativas mais econômicas.
*Rationale*: Assegurar a sustentabilidade financeira do projeto, evitando desperdício de recursos computacionais e garantindo que o custo operacional escale proporcionalmente ao valor entregue.

### V. Parcimônia Extrema e Justificativa de Dependências Externas
A inclusão de qualquer nova dependência externa (seja via pubspec.yaml no ecossistema Dart/Flutter, seja via requirements/pyproject no ecossistema Python) DEVE ser minimizada ao estritamente essencial. Toda e qualquer nova dependência EXIGE justificativa técnica formal documentada, demonstrando por que o problema não pode ou não deve ser resolvido utilizando recursos nativos da linguagem ou da biblioteca padrão. Pacotes que tragam peso desnecessário, histórico de abandono ou vulnerabilidades de segurança não serão aceitos.
*Rationale*: Reduz dramaticamente a superfície de ataque, riscos de quebra de compatibilidade em atualizações, tempos de build, tamanho do executável e a dívida técnica decorrente de dependências órfãs.

## Diretrizes Tecnológicas e Restrições de Engenharia

- **Frontend**: Flutter (Dart) com Clean Architecture, controle rigoroso de estado sem overhead de bibliotecas desnecessárias e total conformidade com diretrizes visuais e operacionais de iOS e Android.
- **Backend**: Python 3 moderno, com uso obrigatório de tipagem estática (type hints), validações estruturadas e separação estrita de camadas (Domain, Application/UseCases, Infrastructure/Adapters).
- **Comunicação e Protocolos**: APIs RESTful/JSON concisas e eficientes, com payloads mínimos para economizar largura de banda e processamento em dispositivos móveis.
- **Segurança e Conformidade**: Práticas de segurança defensiva por padrão (armazenamento seguro no dispositivo móvel, proteção de variáveis de ambiente no backend e sanitização estrita de entradas) sem dependência de ferramentas terceiras onerosas.

## Fluxo de Desenvolvimento e Quality Gates

- **Gate de TDD**: Pull Requests DEVEM comprovar que os testes unitários acompanham ou antecedem o código da funcionalidade e que nenhum código de produção sem cobertura de teste correspondente foi introduzido.
- **Gate de Dependências**: Qualquer alteração em manifestos de pacotes (`pubspec.yaml`, `requirements.txt`, etc.) DEVE conter no commit/PR a justificativa técnica detalhada e avaliação de alternativas nativas.
- **Gate de Arquitetura**: Todo código produzido DEVE respeitar os limites de camadas da Clean Architecture. Violações de acesso direto de UI ou Controller para infraestrutura/banco de dados sem passar por casos de uso ou abstrações serão rejeitadas.
- **Pipeline de Integração Contínua**: Execução de linters e suítes de testes automatizados com sucesso absoluto em cada alteração antes do merge.

## Governança

Esta Constituição define os padrões arquiteturais, técnicos e de qualidade fundamentais do GD Manager e tem precedência sobre quaisquer práticas ou convenções informais.

- **Conformidade Obrigatória**: Todas as especificações, planos de implementação, tarefas e pull requests DEVEM ser verificados quanto à conformidade com os princípios desta Constituição.
- **Processo de Emenda**: Alterações, acréscimos ou remoções de princípios exigem proposta documentada, justificativa técnica, avaliação de impacto arquitetural e aprovação formal.
- **Política de Versionamento Semântico**:
  - **MAJOR**: Alterações ou remoções incompatíveis de princípios ou regras de governança.
  - **MINOR**: Adição de novos princípios, seções ou diretrizes complementares substantivas.
  - **PATCH**: Refinamentos redacionais, correções tipográficas e esclarecimentos pontuais sem alteração semântica.

**Version**: 1.0.0 | **Ratified**: 2026-11-03 | **Last Amended**: 2026-11-03
