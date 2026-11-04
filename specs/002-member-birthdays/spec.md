# Feature Specification: Gestão de Aniversários de Membros

**Feature Branch**: `002-member-birthdays`

**Created**: 2026-11-04

**Status**: Draft

**Input**: User description: "Atualize a feature 002, para que o preenchimento e exibição da data de aniversario/nascimento seja preenchida e exibida no formato \"dd/mm/YYYY\""

## Clarifications

### Session 2026-11-04
- Q: Como os aniversários devem ser consultados e destacados no aplicativo? (FR-006) → A: Ambos — incluir uma seção de destaque no topo da listagem com os aniversariantes dos próximos 30 dias e também um filtro por mês de aniversário para permitir planejamento e consulta de qualquer período do ano.
- Q: Como a data de nascimento e a idade do integrante devem ser apresentadas para os membros no app? (FR-005) → A: O card do membro na listagem exibe o dia e mês com indicador amigável (ex: "🎂 15 de Maio"), enquanto a tela de detalhes cadastrais apresenta a data de nascimento completa e a idade calculada atualizada.
- Q: Qual o formato esperado para preenchimento e exibição da data de nascimento em telas e formulários? → A: O formato padrão adotado para entrada de dados (digitação manual ou seletor de data) e exibição em todas as interfaces do usuário é estritamente `DD/MM/AAAA` (`dd/mm/YYYY`).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Obrigatoriedade e Formato no Cadastro e Edição (Priority: P1)

Como Líder ou Membro do núcleo do grupo, ao registrar um novo membro ou atualizar o cadastro de um membro existente, sou obrigado a informar a data de nascimento no formato padrão brasileiro `DD/MM/AAAA` (`dd/mm/YYYY`), seja através de digitação assistida com máscara ou de seletor visual de calendário, garantindo captura íntegra, legível e validada.

**Why this priority**: É o requisito mandatório central da gestão de membros. A padronização no formato `DD/MM/AAAA` garante a experiência natural dos usuários no Brasil e evita ambiguidades entre dia e mês na digitação ou visualização.

**Independent Test**: Pode ser testado tentando salvar um membro sem preencher a data de nascimento (o sistema deve bloquear com aviso claro); digitando uma data válida no formato `DD/MM/AAAA` ou selecionando via calendário (o registro deve ser gravado e exibido formatado em `DD/MM/AAAA`); e testando formatos inválidos ou datas futuras (devem ser rejeitados com mensagem amigável).

**Acceptance Scenarios**:

1. **Given** que um Líder ou Membro do núcleo está na tela de cadastro de membro, **When** preenche os dados e deixa o campo de data de nascimento em branco, **Then** o sistema bloqueia o salvamento e destaca visualmente o campo de data de nascimento como obrigatório.
2. **Given** o campo de data de nascimento com indicação do formato `DD/MM/AAAA`, **When** o usuário digita a data diretamente ou seleciona uma data no calendário visual, **Then** o campo exibe a data formatada como `DD/MM/AAAA` (ex: `15/05/1990`) e valida os limites cronológicos (não futura e ano >= 1900).
3. **Given** que o usuário digita manualmente uma data em formato inválido ou incompleto (ex: `32/01/1990`, `15/13/1990`, `1505` ou caracteres não numéricos), **When** tenta submeter ou sair do campo, **Then** o sistema exibe mensagem orientando a inserção de uma data válida no formato `DD/MM/AAAA`.
4. **Given** que o usuário tenta informar uma data de nascimento posterior à data de hoje (data futura), **When** confirma o formulário, **Then** o sistema rejeita a operação com aviso de que a data de nascimento não pode estar no futuro.
5. **Given** um membro previamente existente que ainda não possuía data de nascimento cadastrada, **When** um gestor edita esse membro, **Then** o sistema exige o preenchimento obrigatório da data no formato `DD/MM/AAAA` para permitir a gravação.
6. **Given** que o usuário preenche nome, telefone, tipo e uma data de nascimento válida no formato `DD/MM/AAAA`, **When** confirma a criação ou edição, **Then** os dados são persistidos com sucesso e a data passa a compor o cadastro oficial do membro.

---

### User Story 2 - Exibição da Data de Nascimento no Formato DD/MM/AAAA e Idade (Priority: P2)

Como integrante do grupo (Líder, Núcleo ou Normal), desejo visualizar a data de nascimento no formato `DD/MM/AAAA` e a idade calculada do membro na tela de detalhes cadastrais e na listagem, para consultar as informações no formato usual brasileiro sem esforço de conversão.

**Why this priority**: A consistência visual de apresentação assegura clareza imediata para todos os membros que consultam as informações cadastrais.

**Independent Test**: Pode ser testado acessando o detalhe de um membro com data cadastrada e verificando a apresentação da data estritamente no padrão `DD/MM/AAAA` acompanhada da idade calculada.

**Acceptance Scenarios**:

1. **Given** um membro cadastrado com data de nascimento válida, **When** qualquer integrante do grupo acessa a tela de detalhes do membro, **Then** a data de nascimento é exibida no formato `DD/MM/AAAA` acompanhada da idade calculada atualizada (ex: `15/05/1990 (34 anos)`).
2. **Given** a listagem de membros, **When** os cards dos membros são exibidos, **Then** cada card apresenta um indicador amigável com o dia e mês de aniversário do integrante (ex: "🎂 15 de Maio").
3. **Given** um membro ativo cujo aniversário é no dia atual, **When** visualizado no aplicativo, **Then** o sistema apresenta um destaque visual comemorativo discreto (ícone ou badge de aniversariante do dia).

---

### User Story 3 - Consulta e Filtro de Aniversariantes do Mês (Priority: P3)

Como integrante do grupo (Líder, Núcleo ou Normal), desejo visualizar os próximos aniversariantes em destaque e filtrar membros pelo mês de aniversário, para planejar comemorações e homenagens comunitárias.

**Why this priority**: Agrega valor comunitário à rotina do grupo, permitindo planejar comemorações mensais de forma centralizada.

**Independent Test**: Pode ser testado cadastrando membros com aniversários em diferentes meses, verificando a seção de aniversariantes dos próximos 30 dias no topo e utilizando o filtro por mês.

**Acceptance Scenarios**:

1. **Given** membros cadastrados com data de nascimento, **When** o usuário abre a listagem principal de membros, **Then** o sistema exibe no topo uma seção destacando os aniversariantes dos próximos 30 dias ordenados cronologicamente pelo dia do aniversário.
2. **Given** membros com aniversários em diferentes meses, **When** o usuário seleciona um mês específico no filtro de aniversariantes, **Then** a listagem exibe exclusivamente os membros cujo aniversário ocorre no mês selecionado.
3. **Given** um mês selecionado sem nenhum aniversariante, **When** a consulta é executada, **Then** o sistema apresenta um estado vazio amigável informando que não há aniversariantes no período.

---

### Edge Cases

- **Entrada Manual de Formato Inválido**: Entradas como `31/02/1990`, `00/05/1990` ou com separadores incorretos devem ser interceptadas com validação amigável indicando a necessidade de uma data real no formato `DD/MM/AAAA`.
- **Aniversariante do dia 29 de Fevereiro (Ano Bissexto)**: Em anos não bissextos, membros nascidos em 29 de fevereiro devem ser considerados aniversariantes no dia 28 de fevereiro para fins de listagens e notificações.
- **Data no Futuro**: O sistema rejeita terminantemente qualquer data de nascimento posterior à data corrente do calendário.
- **Idade Fora dos Limites Biológicos**: O sistema rejeita datas de nascimento que resultem em idade superior a 120 anos ou anos anteriores a 1900.
- **Membros Históricos sem Data de Nascimento**: Registros legados sem data continuam legíveis com indicador "Data não informada", sendo obrigatório o preenchimento no formato `DD/MM/AAAA` no próximo salvamento do membro.
- **Trânsito e Recepção de Dados na API**: O sistema deve aceitar e validar a data no formato `DD/MM/AAAA` (bem como preservar suporte a `AAAA-MM-DD` para compatibilidade entre serviços), garantindo integridade de persistência.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema DEVE exigir obrigatoriamente o preenchimento de uma data de nascimento válida no momento do cadastro de qualquer novo membro, suportando digitação direta ou seleção visual no formato `DD/MM/AAAA` (`dd/mm/YYYY`).
- **FR-002**: O sistema DEVE exigir obrigatoriamente o preenchimento de uma data de nascimento válida no momento da edição ou atualização de qualquer membro existente, no formato `DD/MM/AAAA` (`dd/mm/YYYY`).
- **FR-003**: O sistema DEVE validar que a data de nascimento seja estritamente anterior ou igual à data corrente (proibindo datas no futuro) e não anterior ao ano de 1900.
- **FR-004**: O sistema DEVE receber e transitar a data de nascimento no formato `DD/MM/AAAA` nas operações de cadastro e edição, garantindo sua persistência consistente e confiável no armazenamento de dados.
- **FR-005**: O sistema DEVE exibir a data completa de nascimento estritamente no formato `DD/MM/AAAA` acompanhada da idade calculada atualizada na tela de detalhes cadastrais, e exibir o dia e mês de aniversário nos cards da listagem principal.
- **FR-006**: O sistema DEVE fornecer destaque no topo da listagem principal com os aniversariantes dos próximos 30 dias e filtro por mês de aniversário para consulta antecipada de qualquer período do ano.
- **FR-007**: A interface móvel DEVE disponibilizar campo de entrada formatado/assistido no padrão `DD/MM/AAAA` e seletor visual de data (*Date Picker*) integrado para preenchimento de dia, mês e ano, exibindo o valor no formato `DD/MM/AAAA`.
- **FR-008**: O sistema DEVE exibir mensagens de validação claras caso o usuário tente salvar o formulário com o campo de data de nascimento vazio, incompleto, fora do formato `DD/MM/AAAA`, no futuro ou anterior a 1900.
- **FR-009**: O sistema DEVE manter compatibilidade com registros de membros legados sem data, exibindo "Data não informada" e exigindo o preenchimento no formato `DD/MM/AAAA` quando o registro for editado.

### Key Entities

- **Membro (Member)** *(atualização de entidade existente)*:
  - **Identificador**: Código único representativo do membro no sistema.
  - **Nome Completo**: Nome e sobrenome do integrante (texto obrigatório).
  - **Contato/Telefone**: Número telefônico (obrigatório, único entre ativos).
  - **E-mail**: Endereço eletrônico (opcional).
  - **Tipo de Membro**: Categoria (`Líder`, `Membro do núcleo`, `Normal`).
  - **Status**: Estado do registro (`Ativo` ou `Inativo`).
  - **Data de Nascimento (Birth Date)**: Data de nascimento do membro (campo obrigatório, preenchida e apresentada em `DD/MM/AAAA`).
  - **Data de Cadastro**: Data e hora em que o registro foi criado.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% dos formulários de cadastro e edição de membros utilizam o formato `DD/MM/AAAA` para captura e validação da data de nascimento, rejeitando envios com formatos inválidos ou vazios.
- **SC-002**: O usuário autorizado consegue informar a data de nascimento completa no formulário móvel (via digitação direta no formato `DD/MM/AAAA` ou via seletor visual) em menos de 10 segundos.
- **SC-003**: 100% das telas e componentes que exibem a data completa de nascimento do membro apresentam-na estritamente no formato `DD/MM/AAAA`.
- **SC-004**: Zero falhas de cálculo de idade ou inconsistências em anos bissextos reportadas no sistema.

## Assumptions

- O padrão `DD/MM/AAAA` (`dd/mm/YYYY`) é a convenção visual e de digitação adotada em conformidade com os costumes dos usuários no Brasil.
- A persistência interna e o processamento de regras de negócio realizam o parsing e tratamento seguro entre o formato visual `DD/MM/AAAA` e a data de calendário sem perda de precisão cronológica.
- O seletor de data (*Date Picker*) da interface móvel respeitará os limites válidos entre 1900 e a data presente, populando o campo diretamente no padrão `DD/MM/AAAA`.
