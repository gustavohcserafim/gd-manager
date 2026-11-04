# 📱 GD Manager

Aplicação **Mobile-First** multi-dispositivos (iOS e Android) em **Flutter** com backend em **Python 3**, desenvolvida estritamente sob os princípios da **Clean Architecture** e orientada a **Test-Driven Development (TDD)**. Projetada com foco em **custo mínimo viável de infraestrutura e hospedagem** e **parcimônia extrema de dependências externas**.

---

## 🏛️ Governança e Princípios Constitucionais

Conforme estabelecido na [Constituição do GD Manager](.specify/memory/constitution.md):

1. **Clean Architecture e Separação de Responsabilidades**: Camada de domínio pura e isolada de frameworks, persistência e interfaces visuais tanto no backend quanto no mobile.
2. **Test-Driven Development (TDD) Inegociável**: Todo comportamento, caso de uso, validação e regra de negócio possui testes automatizados concebidos previamente (ciclo Red-Green-Refactor).
3. **Mobile-First Multiplataforma**: Foco primordial na experiência móvel fluida (60/120 fps) com paridade entre iOS e Android via Flutter.
4. **Eficiência Máxima de Custos**: Custo R$ 0,00 de banco de dados e hospedagem por meio de SQLite embutido e FastAPI leve (<50MB RAM).
5. **Parcimônia de Dependências**: Apenas bibliotecas estritamente essenciais (`fastapi`, `pydantic`, `uvicorn`, `pytest`, `http`), onde qualquer inclusão exige justificativa técnica prévia.

---

## 🎯 Funcionalidade: Cadastro e Gestão de Membros (CRUD)

- **Classificação dos Integrantes**:
  - `Líder`: Responsável pela liderança e condução do grupo (permissão total de leitura e escrita).
  - `Membro do núcleo`: Integrante ativo do núcleo gestor/apoio (permissão total de leitura e escrita).
  - `Normal`: Membro regular participante (acesso exclusivo de leitura e consulta).
- **Regras de Negócio e Domínio**:
  - **Telefone Único Ativo**: O número de telefone é estritamente único entre membros ativos (garantido por índice parcial e regra de domínio).
  - **Controle de Acesso Hierárquico (RBAC)**: Apenas Líder e Núcleo podem cadastrar, editar, inativar e reativar membros. Membros normais têm acesso restrito à leitura; botões de escrita permanecem ocultos na interface e requisições diretas são bloqueadas no backend com código HTTP 403.
  - **Avatares Visuais por Iniciais**: Não há upload de imagens na v1 para manter a infraestrutura enxuta e custo zero; avatares coloridos são gerados dinamicamente pelas iniciais do nome.
  - **Inativação Lógica (Soft Delete)**: Diálogo de confirmação obrigatório em duas etapas para evitar perdas acidentais. Membros inativos podem ser consultados e reativados exclusivamente pela liderança.

---

## 🛠️ Pré-requisitos do Ambiente

Para executar e testar o projeto localmente, certifique-se de ter instalado:

- **Python**: Versão 3.11 ou superior ([python.org](https://www.python.org/)) com `pip`.
- **Flutter SDK**: Versão 3.19 ou superior ([flutter.dev](https://flutter.dev/)) com `dart`.
- **Navegador / Emulador**: Google Chrome (para Flutter Web), emulador Android (Android Studio) ou simulador iOS (Xcode no macOS).

---

## 🚀 Como Rodar Localmente para Testar

O projeto é dividido em dois diretórios independentes: `backend/` (API em Python) e `frontend/` (App em Flutter).

### 1. Inicializando e Testando o Backend (Python 3)

#### Passo 1.1: Acessar a pasta e criar o ambiente virtual

**No Windows (PowerShell):**
```powershell
cd backend
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**No Linux / macOS (Bash/Zsh):**
```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
```

#### Passo 1.2: Instalar as dependências enxutas
```bash
pip install fastapi uvicorn pydantic pytest httpx
```

#### Passo 1.3: Executar a suíte de testes automatizados (TDD)
O backend possui **38 testes automatizados** cobrindo testes unitários de domínio, testes de repositório SQLite, testes de contrato OpenAPI e a validação ponta a ponta:
```bash
python -m pytest tests/ -v -p no:cacheprovider
```
*Saída esperada: `38 passed in ~0.6s`.*

#### Passo 1.4: Iniciar o servidor da API
```bash
uvicorn src.main:app --reload --port 8000
```
- A API estará rodando em: `http://localhost:8000`
- **Documentação Interativa Swagger / OpenAPI**: Acesse [http://localhost:8000/docs](http://localhost:8000/docs) para testar os endpoints interativamente pelo navegador!

---

### 2. Inicializando e Testando o Frontend (Flutter)

Abra uma nova janela de terminal para o frontend:

#### Passo 2.1: Acessar a pasta do app
```bash
cd frontend
```

#### Passo 2.2: Baixar os pacotes
```bash
flutter pub get
```

#### Passo 2.3: Executar os testes automatizados do Flutter
```bash
flutter test
```

#### Passo 2.4: Executar o aplicativo móvel

- **No Navegador (Flutter Web / Chrome)** — *mais rápido para testes*:
  ```bash
  flutter run -d chrome
  ```
- **No Emulador Android ou Dispositivo Físico**:
  ```bash
  flutter run
  ```
  > 💡 **Nota para Emulador Android**: No emulador Android, a máquina local é acessada via IP `http://10.0.2.2:8000/api/v1`. Se necessário, ajuste o `baseUrl` no arquivo `frontend/lib/data/datasources/api_client.dart` ou mantenha `http://localhost:8000/api/v1` para testes no Chrome / Desktop / iOS Simulator.

---

## 🧪 Roteiro de Testes Manuais (Validação Ponta a Ponta)

Ao abrir o aplicativo móvel, você verá a interface com a barra de controle superior **"Perfil Ativo"**. Siga os passos abaixo para validar todas as histórias de usuário:

### 1. Testando a Alternância de Perfil (RBAC)
No topo da tela do app, observe o componente **Perfil Ativo** com os botões `Líder`, `Membro do Núcleo` e `Normal`:
- Quando selecionado como **Líder** ou **Membro do Núcleo**: o botão flutuante `+ Novo Membro` fica visível no canto inferior direito.
- Quando alternado para **Normal**: o botão `+ Novo Membro` desaparece e todas as ações de escrita (editar, inativar) ficam ocultas.

### 2. Cadastrando um Novo Membro (User Story 1 - P1)
1. Certifique-se de que o perfil ativo está como **Líder**.
2. Toque no botão flutuante `+ Novo Membro`.
3. Preencha o formulário:
   - **Nome Completo**: `Carlos Eduardo`
   - **Telefone / WhatsApp**: `11999990001`
   - **E-mail**: `carlos@exemplo.com`
   - **Tipo de Membro**: selecione `Líder`
4. Toque em **Salvar Membro**.
5. **Resultado**: O membro é salvo com sucesso e exibido na listagem com o avatar circular `CE`, badge de `Líder` e status `Ativo`.

### 3. Testando a Regra de Unicidade de Telefone (Bloqueio de Duplicidade)
1. Como **Líder**, toque novamente em `+ Novo Membro`.
2. Preencha com o nome `Marcos Souza`, selecione o tipo `Normal` e insira o **mesmo telefone** do Carlos (`11999990001`).
3. Toque em **Salvar Membro**.
4. **Resultado**: O sistema bloqueia o cadastro e exibe um alerta vermelho na tela: *"O telefone '11999990001' já está cadastrado para outro membro ativo."*

### 4. Consultando, Pesquisando e Filtrando (User Story 2 - P2)
1. Na barra de pesquisa superior, digite `Carlos`. A lista atualizará instantaneamente exibindo apenas o Carlos Eduardo.
2. Limpe a busca tocando no ícone `X`.
3. Toque no chip de filtro `Membro do Núcleo`. Como não há membros desse tipo cadastrados, a tela exibirá o estado vazio (*empty state*) amigável.
4. Toque no chip `Todos` para restaurar a lista completa.

### 5. Visualizando Detalhes e Editando Dados (User Story 3 - P3)
1. Toque no cartão do membro `Carlos Eduardo` para abrir a tela de detalhes.
2. Toque no botão **Editar Dados** (ou no ícone de lápis na barra superior).
3. Altere o tipo de `Líder` para `Membro do Núcleo`.
4. Toque em **Salvar Alterações**.
5. **Resultado**: Os dados são atualizados e o cartão passa a exibir o badge azul/verde de `Membro do Núcleo`.

### 6. Inativando e Reativando um Membro (User Story 4 - P4)
1. Na tela de detalhes do membro, toque em **Inativar Membro**.
2. O aplicativo exibirá um diálogo de confirmação em duas etapas: *"Tem certeza que deseja inativar o membro...?"*.
3. Toque em **Sim, Inativar**.
4. **Resultado**: O membro deixa de ser exibido na listagem de ativos padrão.
5. Na barra de filtros, selecione a opção **Inativos**. O membro aparecerá listado com a etiqueta vermelha `Inativo`.
6. Toque no membro inativo e acione o botão verde **Reativar Membro**.
7. **Resultado**: O membro é restaurado ao status `Ativo` e retorna à listagem regular.

### 7. Validando a Segurança para Membro "Normal"
1. No seletor de perfil no topo da tela, selecione **Normal**.
2. O botão de adicionar novo membro desaparece.
3. Ao tocar em qualquer membro para ver detalhes, os botões de edição e inativação não são exibidos.
4. O chip de filtro para visualizar membros inativos fica inacessível.
5. Qualquer tentativa de requisição direta de escrita (via cURL/Postman com header `X-User-Role: normal`) é bloqueada pelo backend com código `HTTP 403 Forbidden`.

---

## 📁 Estrutura da Arquitetura (Clean Architecture)

```text
gd-manager/
├── backend/
│   ├── pyproject.toml
│   ├── src/
│   │   ├── main.py                     # Entrypoint FastAPI, CORS e DI
│   │   ├── domain/                     # Camada pura de Domínio (sem frameworks)
│   │   │   ├── entities/member.py      # Entidade Member e validações de invariantes
│   │   │   ├── enums/member_enums.py   # MemberRole e MemberStatus
│   │   │   ├── exceptions/             # Exceções de negócio (DomainException, etc.)
│   │   │   └── ports/                  # Interface abstrata do repositório
│   │   ├── application/                # Casos de Uso e DTOs (Pydantic v2)
│   │   │   ├── dtos/                   # CreateMemberRequest, UpdateMemberRequest, etc.
│   │   │   └── use_cases/              # CreateMember, GetMembers, Update, Lifecycle
│   │   └── infrastructure/             # Adaptadores de Banco e Web
│   │       ├── database/               # SQLite Connection e SqliteMemberRepository
│   │       └── web/                    # Rotas REST e Middleware de autorização RBAC
│   └── tests/                          # Suíte TDD completa (unit, integration, contract, quickstart)
│
├── frontend/
│   ├── pubspec.yaml
│   ├── lib/
│   │   ├── main.dart                   # Inicialização e injeção de dependências
│   │   ├── domain/                     # Camada pura de Domínio em Dart
│   │   │   ├── entities/member.dart
│   │   │   ├── enums/member_enums.dart
│   │   │   ├── repositories/           # Interface MemberRepository
│   │   │   └── use_cases/              # Casos de uso do aplicativo
│   │   ├── data/                       # Camada de Dados
│   │   │   ├── models/member_model.dart # DTO com serialização JSON e iniciais
│   │   │   ├── datasources/            # ApiClient e MemberRemoteDataSource
│   │   │   └── repositories/           # Implementação MemberRepositoryImpl
│   │   └── presentation/               # Camada de Apresentação
│   │       ├── controllers/            # SessionContext, MemberList, MemberForm
│   │       ├── screens/                # MemberListScreen, MemberFormScreen, MemberDetailScreen
│   │       └── widgets/                # MemberAvatar, RoleBadge, MemberCard, Dialogs
│   └── test/                           # Testes unitários e de widgets
│
└── specs/001-member-management/         # Artefatos Spec Kit do ciclo de engenharia
    ├── spec.md                         # Especificação funcional e regras de negócio
    ├── plan.md                         # Plano técnico e arquitetural
    ├── research.md                     # Justificativas técnicas e decisões de stack
    ├── data-model.md                   # Modelo de dados e DDL do SQLite
    ├── contracts/                      # Contrato OpenAPI 3.1 da API REST
    ├── quickstart.md                   # Guia de validação ponta a ponta
    └── tasks.md                        # Lista ordenada de 82 tarefas com TDD
```

---

## 📜 Artefatos de Especificação e Design

- [Constituição do Projeto](.specify/memory/constitution.md)
- [Especificação da Feature (spec.md)](specs/001-member-management/spec.md)
- [Plano de Implementação (plan.md)](specs/001-member-management/plan.md)
- [Pesquisa Técnica e Decisões (research.md)](specs/001-member-management/research.md)
- [Modelo de Dados (data-model.md)](specs/001-member-management/data-model.md)
- [Contrato OpenAPI REST (contracts/members-api.yaml)](specs/001-member-management/contracts/members-api.yaml)
- [Roteiro de Validação (quickstart.md)](specs/001-member-management/quickstart.md)
- [Matriz de Tarefas TDD (tasks.md)](specs/001-member-management/tasks.md)
