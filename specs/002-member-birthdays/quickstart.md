# Quickstart: Validação E2E de Gestão de Aniversários de Membros

**Feature**: `002-member-birthdays` | **Date**: 2026-11-04 (Atualizado com formato `DD/MM/AAAA`)

Este guia fornece os cenários de teste ponta a ponta (E2E) para comprovar a funcionalidade de gestão de aniversários de acordo com a especificação e os contratos de API, validando preenchimento e exibição em `DD/MM/AAAA`.

---

## Pré-requisitos & Ambiente

1. Backend Python ativo em `http://localhost:8000`:
   ```bash
   cd backend
   python -m pytest tests/ -v -p no:cacheprovider
   uvicorn src.main:app --reload --port 8000
   ```
2. Frontend Flutter ativo no navegador ou dispositivo móvel:
   ```bash
   cd frontend
   flutter run -d chrome
   ```

---

## Cenários de Teste e Validação

### Cenário 1: Cadastro de Membro com Data de Nascimento Válida em DD/MM/AAAA (P1)
1. Com perfil ativo de **Líder** no app, toque no botão flutuante **"Novo Membro"**.
2. Preencha Nome: `Lucas Nogueira`, Telefone: `11988881234`, Tipo: `Normal`.
3. No campo de **Data de Nascimento (DD/MM/AAAA)**, teste uma das duas formas:
   - Digite diretamente `15/05/1995` (a máscara automática posiciona as barras `/`).
   - Ou toque no ícone de calendário e selecione a data no calendário visual (o campo é preenchido com `15/05/1995`).
4. Toque em **"Salvar Membro"**.
5. **Resultado Esperado**:
   - Membro cadastrado com sucesso (HTTP 201).
   - O card na lista exibe `Lucas Nogueira` com a tag comemorativa `🎂 15 de Maio`.
   - Ao abrir os detalhes, a seção cadastral exibe a data completa estritamente como `15/05/1995` e a idade calculada `(31 anos)`.

### Cenário 2: Bloqueio de Cadastro sem Data, Formato Inválido ou Data Futura (P1)
1. Abra o formulário de novo membro.
2. Preencha nome e telefone, mas deixe a **Data de Nascimento vazia**.
3. Toque em **"Salvar Membro"**.
4. **Resultado Esperado**:
   - O formulário bloqueia a submissão e exibe o alerta: *"Data de nascimento é obrigatória."*
5. Digite uma data com formato inválido (ex: `32/01/1990` ou `15/13/1990`) e tente salvar.
6. **Resultado Esperado**:
   - O formulário exibe aviso indicando data inválida no formato `DD/MM/AAAA`.
7. Tente selecionar ou digitar uma data de nascimento no futuro (ex: ano que vem).
8. **Resultado Esperado**:
   - O sistema bloqueia a gravação e informa: *"A data de nascimento não pode estar no futuro."*

### Cenário 3: Destaque de Próximos Aniversariantes no Topo (P3)
1. Cadastre um membro cujo aniversário seja daqui a 5 dias.
2. Cadastre outro membro cujo aniversário seja daqui a 45 dias.
3. Acesse a tela principal de membros.
4. **Resultado Esperado**:
   - O membro que faz aniversário em 5 dias aparece em destaque na seção de topo **"Próximos Aniversários"**.
   - O membro cujo aniversário ocorre em 45 dias não aparece no destaque de 30 dias, mas é exibido na lista geral.

### Cenário 4: Filtro por Mês de Aniversário (P3)
1. Na barra de filtros da listagem de membros, acione o filtro de mês e selecione **"Maio"**.
2. **Resultado Esperado**:
   - Apenas os membros que fazem aniversário no mês de Maio são exibidos.
   - Selecionar um mês sem nenhum aniversariante exibe o empty state informativo: *"Nenhum aniversariante encontrado neste mês."*

### Cenário 5: Edição de Membro Legado Exigindo Data no Formato DD/MM/AAAA (P1)
1. Selecione um membro histórico que foi cadastrado anteriormente sem data de nascimento ("Data não informada").
2. Toque em **"Editar Dados"**.
3. Tente salvar sem informar a data de nascimento.
4. **Resultado Esperado**:
   - O formulário bloqueia a atualização e exige o preenchimento da data de nascimento.
5. Preencha a data `20/10/1988` e confirme o salvamento.
6. **Resultado Esperado**:
   - Os dados são atualizados com sucesso e os detalhes exibem `20/10/1988` com a idade calculada.
