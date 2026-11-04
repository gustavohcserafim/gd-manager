# Quickstart: Validação E2E de Gestão de Aniversários de Membros

**Feature**: `002-member-birthdays` | **Date**: 2026-11-04

Este guia fornece os cenários de teste ponta a ponta (E2E) para comprovar a funcionalidade de gestão de aniversários de acordo com a especificação e os contratos de API.

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

### Cenário 1: Cadastro de Membro com Data de Nascimento Válida (P1)
1. Com perfil ativo de **Líder** no app, toque no botão flutuante **"Novo Membro"**.
2. Preencha Nome: `Lucas Nogueira`, Telefone: `11988881234`, Tipo: `Normal`.
3. Toque no campo de **Data de Nascimento** e selecione a data `15/05/1995` no calendário.
4. Toque em **"Salvar Membro"**.
5. **Resultado Esperado**:
   - Membro cadastrado com sucesso (HTTP 201).
   - O card na lista exibe `Lucas Nogueira` com a tag comemorativa `🎂 15 de Maio`.
   - Ao abrir os detalhes, a seção cadastral exibe a data completa `15/05/1995` e a idade calculada `(31 anos)`.

### Cenário 2: Bloqueio de Cadastro sem Data ou com Data Futura (P1)
1. Abra o formulário de novo membro.
2. Preencha nome e telefone, mas deixe a **Data de Nascimento vazia**.
3. Toque em **"Salvar Membro"**.
4. **Resultado Esperado**:
   - O formulário bloqueia a submissão e exibe o alerta: *"Data de nascimento é obrigatória."*
5. Agora tente selecionar ou forçar uma data de nascimento no futuro (ex: ano que vem).
6. **Resultado Esperado**:
   - O sistema impede a seleção de datas futuras no DatePicker e a API rejeita com erro HTTP 400 Bad Request (*"A data de nascimento não pode estar no futuro."*).

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

### Cenário 5: Edição de Membro Legado Exigindo Data de Nascimento (P1)
1. Selecione um membro histórico que foi cadastrado anteriormente sem data de nascimento.
2. Toque em **"Editar Dados"**.
3. Tente salvar sem informar a data de nascimento.
4. **Resultado Esperado**:
   - O formulário bloqueia a atualização e exige o preenchimento da data de nascimento.
5. Preencha a data e confirme o salvamento.
6. **Resultado Esperado**:
   - Os dados são atualizados com sucesso e o membro passa a ter seu aniversário e idade calculados.
