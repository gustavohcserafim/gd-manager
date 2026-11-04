# GD Manager

Aplicação **Mobile-First** multi-dispositivos (iOS e Android) em **Flutter** com backend em **Python 3**, desenvolvida estritamente sob os princípios da **Clean Architecture** e orientada a **Test-Driven Development (TDD)**, com foco em custo mínimo viável de infraestrutura e hospedagem e minimização de dependências externas.

---

## 🏛️ Governança e Princípios Arquiteturais

Conforme estabelecido na [Constituição do GD Manager](.specify/memory/constitution.md):

1. **Clean Architecture e Separação de Responsabilidades**: Camada de domínio pura e isolada de frameworks, persistência e UI em ambos os projetos (`backend` e `frontend`).
2. **Test-Driven Development (TDD) Inegociável**: Todo caso de uso, entidade e regra de negócio possui testes automatizados concebidos previamente.
3. **Mobile-First Multiplataforma**: Experiência ergonômica nativa com renderização fluida no Flutter (iOS e Android).
4. **Eficiência Máxima de Custos**: Custo R$ 0,00 de banco de dados e hospedagem por meio de SQLite embutido e FastAPI leve.
5. **Parcimônia de Dependências**: Apenas bibliotecas estritamente essenciais (`fastapi`, `pydantic`, `uvicorn`, `pytest`, `http`).

---

## 🚀 Funcionalidade: Cadastro e Gestão de Membros (CRUD)

- **Tipos de Membros**:
  - `Líder`: Responsável pela liderança e condução do grupo (gestão completa).
  - `Membro do núcleo`: Integrante ativo do núcleo gestor/apoio (gestão completa).
  - `Normal`: Membro regular participante (acesso exclusivo de consulta e leitura).
- **Regras Principais**:
  - **Telefone Único Ativo**: O número de telefone é estritamente único entre membros ativos.
  - **Controle de Acesso Hierárquico (RBAC)**: Apenas Líder e Núcleo podem criar, editar, inativar e reativar membros. Membros normais têm acesso restrito à leitura e botões de escrita permanecem ocultos.
  - **Avatares Visuais por Iniciais**: Não há upload de imagens na v1 para manter a infraestrutura enxuta; avatares coloridos são gerados dinamicamente pelas iniciais do nome.
  - **Inativação Lógica (Soft Delete)**: Confirmação obrigatória em duas etapas; membros inativos podem ser consultados e reativados exclusivamente pela liderança.

---

## 💻 Instruções de Execução

### Backend (Python 3.11+)

1. Acesse o diretório do backend:
   ```bash
   cd backend
   ```
2. Instale as dependências:
   ```bash
   pip install fastapi uvicorn pydantic pytest httpx
   ```
3. Execute a suíte completa de testes automatizados (TDD):
   ```bash
   python -m pytest tests/ -v
   ```
4. Inicie o servidor FastAPI:
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```
   *Documentação interativa OpenAPI / Swagger:* [http://localhost:8000/docs](http://localhost:8000/docs)

### Frontend (Flutter)

1. Acesse o diretório do aplicativo:
   ```bash
   cd frontend
   ```
2. Baixe as dependências:
   ```bash
   flutter pub get
   ```
3. Execute os testes automatizados:
   ```bash
   flutter test
   ```
4. Execute o aplicativo:
   ```bash
   flutter run
   ```

---

## 📁 Estrutura do Projeto

```text
gd-manager/
├── backend/
│   ├── pyproject.toml
│   ├── src/
│   │   ├── main.py                     # FastAPI entrypoint e CORS
│   │   ├── domain/                     # Camada pura de domínio
│   │   │   ├── entities/member.py
│   │   │   ├── enums/member_enums.py
│   │   │   ├── exceptions/member_exceptions.py
│   │   │   └── ports/member_repository.py
│   │   ├── application/                # Casos de uso e DTOs
│   │   │   ├── dtos/
│   │   │   └── use_cases/
│   │   └── infrastructure/             # Adaptadores de banco SQLite e rotas HTTP
│   │       ├── database/
│   │       └── web/
│   └── tests/                          # Suíte TDD (unit, integration, contract, quickstart)
│
├── frontend/
│   ├── pubspec.yaml
│   ├── lib/
│   │   ├── main.dart                   # Inicialização e injeção de dependências
│   │   ├── domain/                     # Entidades, enums e use cases
│   │   ├── data/                       # Models, DTOs e DataSource HTTP
│   │   └── presentation/               # Controllers, Telas e Widgets
│   └── test/                           # Testes unitários e de widgets
│
└── specs/001-member-management/         # Artefatos Spec Kit da funcionalidade
```
