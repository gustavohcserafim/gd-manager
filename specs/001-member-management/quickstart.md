# Quickstart Validation Guide: Cadastro e Gestão de Membros (CRUD)

**Feature**: `001-member-management`  
**Date**: 2026-11-03  
**Status**: Ready for Validation  

---

## 1. Pré-requisitos do Ambiente

- **Python**: Versão 3.11 ou superior com `pip` e `venv`.
- **Flutter SDK**: Versão 3.19 ou superior com `dart`.
- **Navegador / Emulador / Dispositivo**: Chrome, emulador Android ou simulador iOS.

---

## 2. Configuração e Inicialização

### Backend (Python FastAPI)

1. Acessar o diretório do backend:
   ```bash
   cd backend
   ```
2. Criar e ativar o ambiente virtual:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Linux/macOS:
   source .venv/bin/activate
   ```
3. Instalar dependências enxutas:
   ```bash
   pip install fastapi uvicorn pytest pydantic
   ```
4. Executar os testes automatizados (TDD):
   ```bash
   pytest tests/
   ```
5. Iniciar o servidor de desenvolvimento:
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```
   *Documentação interativa Swagger disponível em:* `http://localhost:8000/docs`

### Frontend (Flutter)

1. Acessar o diretório do aplicativo móvel:
   ```bash
   cd frontend
   ```
2. Baixar as dependências:
   ```bash
   flutter pub get
   ```
3. Executar os testes automatizados (TDD):
   ```bash
   flutter test
   ```
4. Executar o app no dispositivo/navegador:
   ```bash
   flutter run -d chrome
   # ou para dispositivo móvel conectado:
   flutter run
   ```

---

## 3. Cenários de Validação Ponta a Ponta (End-to-End)

### Cenário 1: Cadastro de Líder com Sucesso (P1)
1. No aplicativo, verifique se o perfil ativo está selecionado como **Líder** (barra superior ou seletor).
2. Toque no botão de ação flutuante `+` (Novo Membro).
3. Preencha:
   - **Nome**: `Carlos Eduardo`
   - **Telefone**: `11999990001`
   - **Tipo**: `Líder`
4. Toque em **Salvar**.
5. **Resultado Esperado**: O formulário fecha com mensagem de confirmação e a lista exibe o cartão com avatar `CE`, nome `Carlos Eduardo`, tag `Líder` e status `Ativo`.

### Cenário 2: Bloqueio de Telefone Duplicado (Regra de Negócio)
1. Ainda como **Líder**, toque em `+` (Novo Membro).
2. Preencha:
   - **Nome**: `Marcos Souza`
   - **Telefone**: `11999990001` *(mesmo número do Carlos)*
   - **Tipo**: `Normal`
3. Toque em **Salvar**.
4. **Resultado Esperado**: O sistema impede a gravação e exibe aviso de erro no campo de telefone: *"Este número de telefone já está cadastrado para outro membro ativo."*

### Cenário 3: Consulta, Filtro e Busca (P2)
1. Na barra de busca, digite `Carlos`. A lista deve filtrar e exibir apenas `Carlos Eduardo`.
2. Limpe a busca.
3. Alterne o chip de filtro para `Membro do núcleo`. Caso não haja registros nessa categoria, a tela deve exibir a mensagem amigável de estado vazio (*empty state*).
4. Alterne para o filtro `Todos` para restaurar a visualização.

### Cenário 4: Edição de Membro (P3)
1. Toque no membro `Carlos Eduardo` para abrir os detalhes.
2. Toque no ícone de **Editar**.
3. Altere o tipo de `Líder` para `Membro do núcleo`.
4. Toque em **Salvar**.
5. **Resultado Esperado**: Os dados são salvos com sucesso e o cartão passa a exibir o badge `Membro do núcleo`.

### Cenário 5: Inativação e Reativação (P4)
1. Na tela de detalhes de `Carlos Eduardo`, toque em **Inativar Membro**.
2. O sistema exibe o diálogo de confirmação *"Deseja inativar este membro?"*. Toque em **Confirmar**.
3. **Resultado Esperado**: O membro desaparece da listagem principal de ativos.
4. Alterne o filtro de status para **Inativos**. O membro `Carlos Eduardo` deve constar na lista com indicador de inatividade.
5. Toque no membro inativo e acione **Reativar Membro**.
6. **Resultado Esperado**: O membro retorna para a lista de membros ativos.

### Cenário 6: Controle de Acesso para Perfil Normal (RBAC)
1. No seletor de perfil do aplicativo, alterne para **Normal**.
2. **Resultado Esperado**: O botão `+` de adicionar novo membro desaparece da tela.
3. Ao tocar em um membro para visualizar detalhes, os botões de **Editar** e **Inativar** não estão visíveis nem acessíveis.
4. Qualquer tentativa de requisição direta de escrita (via cURL ou Postman) enviando `X-User-Role: normal` para endpoints `POST`, `PUT`, `DELETE` ou `PATCH` deve retornar código `HTTP 403 Forbidden`.
