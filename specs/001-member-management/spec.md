# Feature Specification: Cadastro e Gestão de Membros (CRUD)

**Feature Branch**: `001-member-management`

**Created**: 2026-11-03

**Status**: Draft

**Input**: User description: "Desenvolva a função de cadastro de membros, um CRUD classico já integrado frontend do app com o backend. Temos 3 tipos de membros: Lider, Membro do nucleo e normal."

## Clarifications

### Session 2026-11-03
- Q: Como o sistema deve tratar o cadastro ou a atualização de um membro caso o telefone informado já pertença a outro membro? (FR-001) → A: Bloquear cadastro/atualização duplicada; o telefone deve ser estritamente único entre membros ativos.
- Q: Os 3 tipos de membros (Líder, Membro do núcleo e Normal) definem permissões de acesso diferenciadas no aplicativo ou representam apenas uma classificação cadastral? (FR-002) → A: Permissão hierárquica: "Líder" e "Membro do núcleo" podem realizar todas as operações do CRUD (criar/editar/excluir), enquanto membros com perfil "Normal" possuem acesso restrito à consulta e visualização.
- Q: O cadastro e perfil do membro deve incluir upload de foto/avatar nesta primeira versão, ou o escopo contemplará apenas dados textuais? (FR-001) → A: Sem cadastro de foto (apenas dados textuais na v1); o aplicativo deve exibir avatar visual gerado com as iniciais do nome do membro.
- Q: Os membros inativados devem poder ser visualizados e reativados diretamente pelo aplicativo através de um filtro de status? (FR-008) → A: Sim; incluir filtro para visualizar membros "Inativos" e opção de "Reativar membro" acessível exclusivamente para Líder e Membro do núcleo.
- Q: Como o aplicativo móvel deve fornecer o perfil do usuário logado (Líder, Núcleo ou Normal) ao backend para testar as permissões de acesso nesta primeira entrega? (FR-012) → A: Contexto de perfil no app e cabeçalho de requisição simples (ex: X-User-Role), permitindo alternar facilmente entre perfis para validação e testes das permissões sem dependência prematura de login/JWT.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Cadastro de Novo Membro (Priority: P1)

Como Líder ou Membro do núcleo do grupo, desejo registrar novos membros informando seus dados essenciais e classificando seu tipo de atuação, para que façam parte do rol oficial do grupo e possam ser acompanhados.

**Why this priority**: É a funcionalidade primordial que dá origem à existência dos dados. Sem o cadastro, não há membros para consultar, editar ou gerenciar.

**Independent Test**: Pode ser testado de ponta a ponta acessando a tela de cadastro com perfil ativo de Líder ou Núcleo, preenchendo as informações de um membro (ex: nome, contato e tipo "Líder") e confirmando que o registro foi criado com sucesso.

**Acceptance Scenarios**:

1. **Given** que um usuário com perfil ativo de Líder ou Membro do núcleo está na tela de cadastro de membro, **When** preenche um nome válido, número de contato e seleciona o tipo "Líder", **Then** o sistema registra o membro com status ativo e exibe uma mensagem de sucesso, redirecionando para a listagem onde o novo membro aparece com avatar de suas iniciais.
2. **Given** que o usuário autorizado tenta salvar um cadastro sem preencher o nome ou o contato, **When** aciona a opção de salvar, **Then** o sistema impede a gravação e destaca visualmente os campos obrigatórios não preenchidos.
3. **Given** que o usuário preenche os dados válidos e seleciona o tipo "Membro do núcleo" ou "Normal", **When** confirma o salvamento, **Then** o membro é armazenado com o respectivo tipo selecionado.
4. **Given** que já existe um membro ativo cadastrado com o telefone informado, **When** o usuário tenta cadastrar outro membro com esse mesmo número de telefone, **Then** o sistema bloqueia o salvamento e apresenta mensagem clara informando que o telefone já se encontra em uso.
5. **Given** que o aplicativo está alternado para o perfil "Normal", **When** acessa a tela de membros, **Then** a opção de cadastrar novos membros não é exibida e tentativas diretas de envio são bloqueadas no backend com erro de permissão negada.

---

### User Story 2 - Consulta e Listagem de Membros (Priority: P2)

Como integrante do grupo (Líder, Membro do núcleo ou Normal), desejo visualizar a lista de todos os membros cadastrados, podendo pesquisar por nome e filtrar por tipo de membro, para localizar rapidamente os integrantes e verificar sua composição.

**Why this priority**: É essencial para o dia a dia de todos os integrantes poder consultar quem são os membros e filtrar por suas funções (Líder, Núcleo, Normal).

**Independent Test**: Pode ser testado criando membros de diferentes tipos, abrindo a tela de listagem e aplicando filtros por tipo e buscas textuais por nome, conferindo se os itens exibidos correspondem aos critérios.

**Acceptance Scenarios**:

1. **Given** que existem membros cadastrados no grupo, **When** qualquer membro (Líder, Núcleo ou Normal) acessa a tela principal de membros, **Then** todos os membros ativos são exibidos com avatar gerado pelas iniciais, nome e indicação visual de seu tipo.
2. **Given** uma lista de membros cadastrados com tipos diversos, **When** o integrante filtra pelo tipo "Membro do núcleo", **Then** a listagem exibe exclusivamente os membros dessa categoria.
3. **Given** que o integrante digita parte do nome de um membro no campo de busca, **When** o texto é inserido, **Then** a listagem filtra dinamicamente exibindo apenas os membros correspondentes.
4. **Given** que não há membros cadastrados ou a busca não localiza correspondências, **When** a tela é exibida, **Then** o sistema apresenta uma mensagem informativa de estado vazio com orientação clara.
5. **Given** que existem membros inativados no sistema, **When** um Líder ou Membro do núcleo aciona o filtro de status "Inativos", **Then** a listagem exibe exclusivamente os membros inativados com indicador visual de inatividade.

---

### User Story 3 - Visualização e Edição de Dados do Membro (Priority: P3)

Como Líder ou Membro do núcleo do grupo, desejo visualizar o detalhamento cadastral de um membro e atualizar suas informações ou alterar seu tipo de membro, para refletir mudanças de função ou atualizações de contato.

**Why this priority**: Membros mudam de telefone ou são promovidos de função (ex: de Normal para Membro do núcleo ou Líder). Manter os dados atualizados é essencial para a operação contínua.

**Independent Test**: Pode ser testado selecionando um membro existente com um usuário autorizado, alterando seu tipo de membro e telefone, salvando e verificando se os novos dados persistem na tela de detalhes e na listagem.

**Acceptance Scenarios**:

1. **Given** um membro já cadastrado como "Normal", **When** um Líder ou Membro do núcleo abre a edição, altera a categoria para "Membro do núcleo" e salva, **Then** os dados são atualizados com confirmação visual e refletem imediatamente na listagem.
2. **Given** a tela de edição de membro, **When** o usuário autorizado limpa o campo obrigatório de nome e tenta salvar, **Then** o sistema exibe alerta de campo obrigatório e não persiste a alteração inválida.
3. **Given** um membro em edição, **When** o usuário altera o número de telefone para um contato que já pertence a outro membro ativo, **Then** o sistema impede a atualização e informa o conflito de duplicidade de telefone.
4. **Given** que o perfil ativo no app é "Normal", **When** visualiza a tela de detalhes de um membro, **Then** as opções de edição são ocultadas e qualquer tentativa de atualização é rejeitada com erro de autorização.

---

### User Story 4 - Remoção / Inativação e Reativação de Membro (Priority: P4)

Como Líder ou Membro do núcleo do grupo, desejo inativar membros que saíram do grupo ou reativar membros que retornaram, mediante confirmação explícita, para manter o rol de membros atualizado sem risco de inconsistências.

**Why this priority**: Necessário para a integridade do cadastro a longo prazo, controle de participantes ativos e reintegração ágil de membros que retornam.

**Independent Test**: Pode ser testado com perfil ativo de Líder ou Núcleo, inativando um membro ativo e posteriormente filtrando inativos e executando a reativação com sucesso.

**Acceptance Scenarios**:

1. **Given** um membro selecionado na listagem ou na tela de detalhes por um Líder ou Membro do núcleo, **When** o usuário clica para inativar, **Then** o sistema apresenta um diálogo de confirmação solicitando aprovação da operação.
2. **Given** o diálogo de confirmação de inativação exibido, **When** o usuário autorizado confirma a inativação, **Then** o membro passa para o status "Inativo", sai da listagem ativa padrão e uma mensagem de confirmação é exibida.
3. **Given** o diálogo de confirmação de inativação exibido, **When** o usuário clica em cancelar, **Then** nenhuma alteração é feita e o membro permanece inalterado.
4. **Given** um membro inativo selecionado na lista de inativos por um Líder ou Núcleo, **When** o usuário aciona a opção "Reativar Membro" e confirma, **Then** o sistema reativa o membro para o status "Ativo", valida que seu telefone continua sem duplicidade entre membros ativos e o exibe novamente na lista principal.
5. **Given** um membro inativo cujo telefone passou a ser utilizado por outro membro ativo, **When** o usuário tenta reativá-lo, **Then** o sistema bloqueia a reativação informando que o telefone está em conflito e orienta a edição do contato.
6. **Given** que o perfil ativo no app é "Normal", **When** visualiza os membros, **Then** nenhuma ação de inativação ou reativação está visível ou acessível.

---

### Edge Cases

- **Tentativa de Ação de Modificação por Membro Normal**: Caso um usuário com perfil "Normal" tente forçar uma requisição de criação, edição, inativação ou reativação, o backend deve bloquear a operação retornando erro de autorização (acesso negado) e o frontend deve garantir que botões de escrita permaneçam ocultos.
- **Tentativa de Reativação com Telefone em Conflito**: Ao tentar reativar um membro inativo cujo telefone passou a pertencer a outro membro ativo, a operação deve ser impedida no domínio com mensagem explícita orientando a atualização do número.
- **Tentativa de Cadastro ou Atualização com Telefone Duplicado**: O sistema deve validar no domínio e persistência a unicidade do telefone entre membros ativos, bloqueando duplicidades e retornando feedback explicativo na interface.
- **Instabilidade de Conexão durante o Envio**: Se a conexão falhar durante a gravação de um novo membro ou edição, o sistema deve manter os dados preenchidos na tela, alertar o usuário sobre a falha de comunicação e permitir uma nova tentativa sem perda das informações digitadas.
- **Validação de Tamanho e Formato de Campos**: Nomes com menos de 3 caracteres ou excessivamente longos (mais de 150 caracteres) devem ser rejeitados com feedback claro na tela.
- **Tentativa de Atribuição de Tipo Inválido**: O sistema deve rejeitar terminantemente qualquer tipo de membro que não seja um dos três tipos pré-estabelecidos: "Líder", "Membro do núcleo" e "Normal".
- **Tentativa de Ação sobre Registro Excluído/Inativo Inexistente**: Se um gestor tentar editar um membro que foi modificado em outra sessão, o sistema deve informar amigavelmente que o registro foi atualizado e recarregar os dados.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: O sistema DEVE permitir a criação de um novo membro capturando exclusivamente dados textuais: Nome Completo (obrigatório), Contato/Telefone (obrigatório), E-mail (opcional) e Tipo de Membro (obrigatório).
- **FR-002**: O sistema DEVE suportar estritamente três categorias para o Tipo de Membro: `Líder`, `Membro do núcleo` e `Normal`.
- **FR-003**: O sistema DEVE validar o preenchimento de todos os campos obrigatórios antes de persistir as informações, rejeitando nomes em branco ou com menos de 3 caracteres.
- **FR-004**: O sistema DEVE listar todos os membros ativos por padrão, exibindo avatar visual com as iniciais do nome, nome completo, categoria de membro e status de forma visualmente diferenciada.
- **FR-005**: O sistema DEVE permitir filtrar a listagem de membros por Tipo de Membro (`Todos`, `Líder`, `Membro do núcleo`, `Normal`) e por Status (`Ativos`, `Inativos` — com acesso ao filtro de inativos restrito a Líder e Membro do núcleo).
- **FR-006**: O sistema DEVE fornecer mecanismo de busca textual em tempo real ou por acionamento, filtrando membros cujo nome contenha o termo pesquisado.
- **FR-007**: O sistema DEVE permitir a edição de todos os dados cadastrais e a alteração da categoria de um membro existente por usuários autorizados.
- **FR-008**: O sistema DEVE permitir a inativação (*soft delete*) de um membro por usuários autorizados, exigindo confirmação explícita em janela/diálogo antes de efetivar a ação.
- **FR-009**: O sistema DEVE apresentar um estado vazio amigável (*empty state*) quando não existirem membros registrados ou quando uma busca/filtro não retornar resultados.
- **FR-010**: O sistema DEVE fornecer mensagens claras de feedback ao usuário após cada ação de criação, edição, exclusão ou falha de comunicação.
- **FR-011**: O sistema DEVE garantir a unicidade do número de telefone entre membros com status ativo, rejeitando operações de cadastro ou atualização que tentem associar um telefone já cadastrado.
- **FR-012**: O sistema DEVE aplicar controle de acesso hierárquico nas operações de escrita: apenas usuários com perfil ativo de `Líder` ou `Membro do núcleo` têm permissão para criar, editar, inativar e reativar membros; usuários com perfil `Normal` possuem acesso restrito à consulta e visualização da listagem. O perfil ativo é transmitido via contexto/cabeçalho de requisição para fins de autorização.
- **FR-013**: O sistema NÃO DEVE realizar upload nem armazenamento de arquivos de foto de membro nesta versão; a interface DEVE apresentar componentes de avatar gerados dinamicamente com as iniciais do integrante.
- **FR-014**: O sistema DEVE permitir a reativação de membros inativos exclusivamente por usuários autorizados (Líder e Membro do núcleo), revalidando a regra de unicidade de telefone ativo antes de restaurar o membro ao rol regular.

### Key Entities

- **Membro (Member)**:
  - **Identificador**: Código único representativo do membro no sistema.
  - **Nome Completo**: Nome e sobrenome do integrante (texto obrigatório, mínimo 3 caracteres).
  - **Contato/Telefone**: Número telefônico ou WhatsApp para comunicação (texto obrigatório, único entre membros ativos).
  - **E-mail**: Endereço eletrônico de contato (texto opcional).
  - **Tipo de Membro**: Categoria de pertencimento, com valores válidos restritos a:
    - `Líder`: Responsável pela liderança e condução do grupo (possui permissão de gestão completa).
    - `Membro do núcleo`: Integrante que compõe o núcleo ativo/apoio (possui permissão de gestão completa).
    - `Normal`: Membro participante regular do grupo (possui acesso somente leitura).
  - **Status**: Estado do registro (`Ativo` ou `Inativo`).
  - **Data de Ingresso/Cadastro**: Data e hora em que o registro foi criado.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: O usuário autorizado consegue preencher os campos e concluir o cadastro de um novo membro em menos de 40 segundos no aplicativo.
- **SC-002**: A lista inicial de membros é carregada e exibida na tela do dispositivo em menos de 1 segundo sob condições normais de conexão.
- **SC-003**: 100% das tentativas de cadastro, edição ou reativação com campos obrigatórios ausentes, tipos inválidos, telefones duplicados ou sem permissão de acesso são bloqueadas com avisos claros ao usuário.
- **SC-004**: O usuário consegue localizar qualquer membro cadastrado utilizando a busca por nome ou filtro de tipo com no máximo 2 toques ou ações na tela.
- **SC-005**: Zero exclusões acidentais relatadas, garantido pelo diálogo de confirmação mandatório em duas etapas para qualquer remoção.

## Assumptions

- O aplicativo móvel é o ponto de interação principal, comunicando-se de forma transparente com o serviço backend para armazenamento e consulta dos dados via payloads JSON enxutos.
- O tipo de membro padrão pré-selecionado no formulário de inclusão é "Normal", permitindo que o gestor altere caso deseje cadastrar um "Líder" ou "Membro do núcleo".
- A exclusão de um membro é tratada como inativação lógica (*soft delete*) para salvaguardar o histórico da organização, ocultando o membro da listagem ativa padrão, com possibilidade de visualização e restauração por usuários autorizados.
- O controle de acesso ao gerenciamento de membros é baseado no papel do usuário ativo: "Líder" e "Membro do núcleo" possuem privilégios de escrita (criação, edição, inativação e reativação), enquanto "Normal" tem acesso somente leitura.
- Para os testes e integração inicial do CRUD, o perfil do usuário é fornecido através de um contexto de perfil/cabeçalho de requisição (sem exigir previamente a implementação de um subsistema completo de login com credenciais/JWT).
- O armazenamento e upload de fotos está fora de escopo para a v1 para garantir conformidade com os princípios constitucionais de custo mínimo e stack enxuta.
