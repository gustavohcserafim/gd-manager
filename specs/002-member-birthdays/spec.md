# Feature Specification: Gestão de Aniversários de Membros

**Feature Branch**: `002-member-birthdays`

**Created**: 2026-11-04

**Status**: Draft

**Input**: User description: "Implemente a função de aniversario dos membros. Ao editr ou cadastrar um novo membro é obrigatório informar a data de nascimento."

## Clarifications

### Session 2026-11-04
- Q: Como os aniversários devem ser consultados e destacados no aplicativo? (FR-006) → A: Ambos — incluir uma seção de destaque no topo da listagem com os aniversariantes dos próximos 30 dias e também um filtro por mês de aniversário para permitir planejamento e consulta de qualquer período do ano.
- Q: Como a data de nascimento e a idade do integrante devem ser apresentadas para os membros no app? (FR-005) → A: O card do membro na listagem exibe o dia e mês com indicador amigável (ex: "🎂 15 de Maio"), enquanto a tela de detalhes cadastrais apresenta a data de nascimento completa e a idade calculada atualizada.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Obrigatoriedade da Data de Nascimento no Cadastro e Edição (Priority: P1)

Como Líder ou Membro do núcleo do grupo, ao registrar um novo membro ou atualizar o cadastro de um membro existente, sou obrigado a informar a data de nascimento do integrante através de um seletor amigável ou digitação formatada, garantindo que nenhum membro seja cadastrado ou atualizado sem essa informação vital.

**Why this priority**: É o requisito mandatório central solicitado pelo usuário. Sem a garantia da captura consistente e validação da data de nascimento no momento da entrada ou edição de dados, as funcionalidades de consulta, filtro e celebração de aniversários ficam inviabilizadas.

**Independent Test**: Pode ser testado de ponta a ponta tentando salvar um novo membro ou editar um membro existente sem preencher a data de nascimento (o sistema deve bloquear com aviso claro); e preenchendo uma data de nascimento válida (o registro deve ser gravado com sucesso com a data persistida).

**Acceptance Scenarios**:

1. **Given** que um Líder ou Membro do núcleo está na tela de cadastro de membro, **When** preenche todos os dados e deixa o campo de data de nascimento em branco, **Then** o sistema bloqueia o salvamento e destaca visualmente o campo de data de nascimento como obrigatório.
2. **Given** que o usuário autorizado aciona o campo de data de nascimento, **When** seleciona uma data no calendário visual ou insere uma data no formato padrão, **Then** a data é validada (não pode ser data futura e deve representar idade humana válida entre 0 e 120 anos) e exibida formatada na tela.
3. **Given** que um usuário autorizado tenta salvar uma data de nascimento posterior à data de hoje (data futura), **When** confirma o formulário, **Then** o sistema rejeita a operação e exibe mensagem de erro orientando que a data de nascimento não pode estar no futuro.
4. **Given** um membro previamente existente que ainda não possuía data de nascimento cadastrada, **When** um gestor abre a edição desse membro e tenta salvar alterações sem preencher a data de nascimento, **Then** o sistema exige o preenchimento obrigatório da data para permitir a gravação.
5. **Given** que o usuário preenche nome, telefone, tipo e uma data de nascimento válida, **When** confirma a criação ou edição, **Then** os dados são persistidos com sucesso e a data de nascimento passa a compor o registro oficial do membro.

---

### User Story 2 - Exibição do Aniversário nos Detalhes e Cartão do Membro (Priority: P2)

Como integrante do grupo (Líder, Núcleo ou Normal), desejo visualizar a data de aniversário e a idade do membro na tela de detalhes cadastrais e na listagem, para saber prontamente quando parabenizar o integrante.

**Why this priority**: Garante visibilidade da informação cadastrada para todos os membros que possuem acesso de leitura aos integrantes do grupo.

**Independent Test**: Pode ser testado acessando o detalhe de um membro com data de nascimento cadastrada e verificando a apresentação correta da data formatada e da idade calculada.

**Acceptance Scenarios**:

1. **Given** um membro cadastrado com data de nascimento válida, **When** qualquer usuário com acesso ao grupo visualiza a tela de detalhes do membro, **Then** a data de nascimento completa formatada (DD/MM/AAAA) e a idade calculada atualizada (ex: "15/05/1990 (34 anos)") são apresentadas com clareza na seção de informações cadastrais.
2. **Given** a listagem de membros, **When** os cards dos membros são exibidos, **Then** cada card apresenta um indicador amigável com o dia e mês de aniversário do integrante (ex: "🎂 15 de Maio").
3. **Given** um membro ativo cujo aniversário é no dia atual, **When** visualizado no app, **Then** o sistema apresenta um destaque visual comemorativo discreto (ex: badge ou ícone temático de aniversário) indicando que o integrante é aniversariante do dia.

---

### User Story 3 - Consulta e Filtro de Aniversariantes do Mês (Priority: P3)

Como integrante do grupo (Líder, Núcleo ou Normal), desejo visualizar os próximos aniversariantes em destaque e filtrar membros pelo mês de aniversário, para facilitar o planejamento de comemorações e homenagens comunitárias.

**Why this priority**: Agrega alto valor comunitário à gestão de pessoas do grupo, permitindo planejar eventos mensais sem ter que consultar membro por membro individualmente.

**Independent Test**: Pode ser testado cadastrando membros com aniversários em meses distintos, verificando a seção de destaque de aniversários nos próximos 30 dias no topo da tela e aplicando o filtro por mês.

**Acceptance Scenarios**:

1. **Given** que existem membros cadastrados com data de nascimento, **When** o usuário abre a tela principal de membros, **Then** o sistema exibe no topo uma seção destacando os aniversariantes dos próximos 30 dias ordenados cronologicamente pelo dia do aniversário.
2. **Given** membros cadastrados com datas de nascimento em diferentes meses do ano, **When** o usuário seleciona um mês específico no filtro de aniversariantes, **Then** a listagem exibe exclusivamente os membros cujo aniversário ocorre no mês selecionado.
3. **Given** um mês selecionado que não possui nenhum membro aniversariante cadastrado, **When** a consulta é executada, **Then** o sistema apresenta uma mensagem informativa de estado vazio amigável orientando que não há aniversariantes no período.

---

### Edge Cases

- **Aniversariante do dia 29 de Fevereiro (Ano Bissexto)**: Em anos não bissextos, membros nascidos em 29 de fevereiro devem ser considerados aniversariantes no dia 28 de fevereiro para efeitos de cálculo e filtros do mês de fevereiro.
- **Data no Futuro**: O sistema deve rejeitar terminantemente qualquer data de nascimento maior que a data atual do calendário.
- **Idade Biológica Fora dos Limites**: O sistema deve rejeitar datas de nascimento que resultem em idade superior a 120 anos ou datas inconsistentes (ano menor que 1900).
- **Membros Históricos sem Data de Nascimento**: Membros antigos já salvos no banco antes desta versão continuam visíveis na listagem regular com indicador "Data não informada", porém tornam-se estritamente obrigados a preencher a data de nascimento no momento em que qualquer edição em seu cadastro for submetida.
- **Tentativa de Forçar Envio sem Data via API**: Se uma requisição de criação ou edição for enviada sem o campo de data de nascimento ou com valor nulo/inválido, o backend deve responder imediatamente com código de erro de validação (HTTP 400 Bad Request) e mensagem descritiva.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema DEVE exigir obrigatoriamente o preenchimento de uma data de nascimento válida no momento do cadastro de qualquer novo membro.
- **FR-002**: O sistema DEVE exigir obrigatoriamente o preenchimento de uma data de nascimento válida no momento da edição ou atualização de qualquer membro existente.
- **FR-003**: O sistema DEVE validar que a data de nascimento seja estritamente anterior à data corrente (proibindo datas no futuro) e não anterior ao ano de 1900.
- **FR-004**: O sistema DEVE persistir a data de nascimento do membro associada ao seu registro de dados no formato de data padrão de calendário (ano, mês e dia no padrão ISO AAAA-MM-DD).
- **FR-005**: O sistema DEVE exibir a data completa de nascimento e a idade calculada do membro na tela de detalhes cadastrais, e exibir o dia e mês de aniversário nos cards da listagem principal.
- **FR-006**: O sistema DEVE fornecer destaque no topo da listagem principal com os aniversariantes dos próximos 30 dias e filtro por mês de aniversário para consulta antecipada de aniversariantes de qualquer mês do ano.
- **FR-007**: A interface móvel DEVE disponibilizar um seletor visual de data (*Date Picker*) integrado para facilitar a seleção de dia, mês e ano de nascimento pelo usuário em dispositivos de toque.
- **FR-008**: O sistema DEVE exibir mensagens de validação claras na interface caso o usuário tente salvar o formulário com o campo de data de nascimento vazio ou com valor inválido.
- **FR-009**: O sistema DEVE manter compatibilidade com registros de membros previamente existentes, permitindo sua visualização e exigindo a adição da data de nascimento no próximo ciclo de edição do registro.

### Key Entities

- **Membro (Member)** *(atualização de entidade existente)*:
  - **Identificador**: Código único representativo do membro no sistema.
  - **Nome Completo**: Nome e sobrenome do integrante (texto obrigatório).
  - **Contato/Telefone**: Número telefônico (obrigatório, único entre ativos).
  - **E-mail**: Endereço eletrônico (opcional).
  - **Tipo de Membro**: Categoria (`Líder`, `Membro do núcleo`, `Normal`).
  - **Status**: Estado do registro (`Ativo` ou `Inativo`).
  - **Data de Nascimento (Birth Date)**: Data de nascimento do membro (campo obrigatório, composto por ano, mês e dia).
  - **Data de Cadastro**: Data e hora em que o registro foi criado.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: 100% dos novos cadastros e edições de membros submetidos sem data de nascimento são bloqueados na interface e validados no backend com mensagens de orientação claras.
- **SC-002**: O usuário autorizado consegue selecionar a data de nascimento completa no formulário móvel em menos de 10 segundos utilizando o seletor visual de data.
- **SC-003**: O usuário consegue visualizar os próximos aniversariantes diretamente na tela principal e consultar aniversariantes de qualquer mês com no máximo 2 toques.
- **SC-004**: Zero falhas de cálculo de idade ou inconsistências em anos bissextos reportadas no sistema.

## Assumptions

- A data de nascimento armazena dia, mês e ano, sendo o ano essencial para o cálculo automático e fidedigno da idade do integrante.
- Usuários com perfil "Normal" podem visualizar as datas de aniversário e consultar os aniversariantes do mês, mantendo a permissão de escrita e edição restrita a "Líder" e "Membro do núcleo", alinhado ao modelo de controle de acesso hierárquico já estabelecido.
- A interface apresentará seletor de data adaptado para toque (*Date Picker*) com limites predefinidos entre 1900 e o ano corrente.
- Em anos não bissextos, membros nascidos no dia 29 de fevereiro são considerados aniversariantes no dia 28 de fevereiro para fins de listagem e alertas.
