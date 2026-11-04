import 'package:flutter/material.dart';
import '../../domain/enums/member_enums.dart';
import '../controllers/member_list_controller.dart';
import '../controllers/session_context_controller.dart';
import '../widgets/member_card.dart';
import '../widgets/user_role_selector_bar.dart';

class MemberListScreen extends StatefulWidget {
  final MemberListController listController;
  final SessionContextController sessionController;
  final Function(String memberId)? onSelectMember;
  final VoidCallback? onAddMember;

  const MemberListScreen({
    super.key,
    required this.listController,
    required this.sessionController,
    this.onSelectMember,
    this.onAddMember,
  });

  @override
  State<MemberListScreen> createState() => _MemberListScreenState();
}

class _MemberListScreenState extends State<MemberListScreen> {
  final TextEditingController _searchController = TextEditingController();

  @override
  void initState() {
    super.initState();
    widget.listController.loadMembers();
    widget.sessionController.addListener(_onSessionChanged);
  }

  void _onSessionChanged() {
    // Se o perfil alternar para Normal e o filtro estiver em Inativo, reseta para Ativo
    if (!widget.sessionController.canManage &&
        widget.listController.selectedStatus == MemberStatus.inactive) {
      widget.listController.setStatus(MemberStatus.active);
    } else {
      widget.listController.loadMembers();
    }
  }

  @override
  void dispose() {
    _searchController.dispose();
    widget.sessionController.removeListener(_onSessionChanged);
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: Listenable.merge([widget.listController, widget.sessionController]),
      builder: (context, _) {
        final canManage = widget.sessionController.canManage;
        final isInactiveFilter = widget.listController.selectedStatus == MemberStatus.inactive;

        return Scaffold(
          appBar: AppBar(
            title: const Text('Membros do GD'),
            backgroundColor: Colors.blueGrey.shade900,
            foregroundColor: Colors.white,
            actions: [
              IconButton(
                icon: const Icon(Icons.refresh),
                tooltip: 'Atualizar',
                onPressed: () => widget.listController.loadMembers(),
              ),
            ],
          ),
          body: Column(
            children: [
              UserRoleSelectorBar(sessionController: widget.sessionController),

              // Barra de pesquisa
              Padding(
                padding: const EdgeInsets.fromLTRB(16, 12, 16, 8),
                child: TextField(
                  controller: _searchController,
                  decoration: InputDecoration(
                    hintText: 'Pesquisar membro por nome...',
                    prefixIcon: const Icon(Icons.search),
                    suffixIcon: _searchController.text.isNotEmpty
                        ? IconButton(
                            icon: const Icon(Icons.clear),
                            onPressed: () {
                              _searchController.clear();
                              widget.listController.setSearch('');
                            },
                          )
                        : null,
                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(10)),
                    contentPadding: const EdgeInsets.symmetric(horizontal: 16),
                  ),
                  onChanged: (text) => widget.listController.setSearch(text),
                ),
              ),

              // Chips de filtros de Tipo e Status
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 4),
                child: Row(
                  children: [
                    FilterChip(
                      label: const Text('Todos'),
                      selected: widget.listController.selectedRole == null,
                      onSelected: (_) => widget.listController.setRole(null),
                    ),
                    const SizedBox(width: 8),
                    FilterChip(
                      label: const Text('Líder'),
                      selected: widget.listController.selectedRole == MemberRole.leader,
                      onSelected: (_) => widget.listController.setRole(MemberRole.leader),
                    ),
                    const SizedBox(width: 8),
                    FilterChip(
                      label: const Text('Membro do Núcleo'),
                      selected: widget.listController.selectedRole == MemberRole.core,
                      onSelected: (_) => widget.listController.setRole(MemberRole.core),
                    ),
                    const SizedBox(width: 8),
                    FilterChip(
                      label: const Text('Normal'),
                      selected: widget.listController.selectedRole == MemberRole.normal,
                      onSelected: (_) => widget.listController.setRole(MemberRole.normal),
                    ),
                    if (canManage) ...[
                      const SizedBox(width: 12),
                      const VerticalDivider(width: 1),
                      const SizedBox(width: 12),
                      ChoiceChip(
                        avatar: Icon(
                          isInactiveFilter ? Icons.visibility_off : Icons.check_circle,
                          size: 16,
                          color: isInactiveFilter ? Colors.white : Colors.blueGrey,
                        ),
                        label: Text(isInactiveFilter ? 'Inativos' : 'Ativos'),
                        selected: isInactiveFilter,
                        selectedColor: Colors.red.shade700,
                        labelStyle: TextStyle(
                          color: isInactiveFilter ? Colors.white : Colors.black87,
                          fontWeight: FontWeight.bold,
                        ),
                        onSelected: (val) {
                          widget.listController.setStatus(
                            val ? MemberStatus.inactive : MemberStatus.active,
                          );
                        },
                      ),
                    ],
                  ],
                ),
              ),

              const Divider(height: 16),

              // Lista ou Empty State
              Expanded(
                child: widget.listController.isLoading
                    ? const Center(child: CircularProgressIndicator())
                    : widget.listController.errorMessage != null
                        ? Center(
                            child: Padding(
                              padding: const EdgeInsets.all(24),
                              child: Column(
                                mainAxisAlignment: MainAxisAlignment.center,
                                children: [
                                  const Icon(Icons.cloud_off, size: 48, color: Colors.grey),
                                  const SizedBox(height: 12),
                                  Text(
                                    widget.listController.errorMessage!,
                                    textAlign: TextAlign.center,
                                    style: TextStyle(color: Colors.grey.shade800),
                                  ),
                                  const SizedBox(height: 16),
                                  ElevatedButton(
                                    onPressed: () => widget.listController.loadMembers(),
                                    child: const Text('Tentar Novamente'),
                                  ),
                                ],
                              ),
                            ),
                          )
                        : widget.listController.members.isEmpty
                            ? Center(
                                child: Padding(
                                  padding: const EdgeInsets.all(32),
                                  child: Column(
                                    mainAxisAlignment: MainAxisAlignment.center,
                                    children: [
                                      Icon(
                                        isInactiveFilter ? Icons.person_off_outlined : Icons.people_outline,
                                        size: 64,
                                        color: Colors.grey.shade400,
                                      ),
                                      const SizedBox(height: 16),
                                      Text(
                                        isInactiveFilter
                                            ? 'Nenhum membro inativo encontrado.'
                                            : 'Nenhum membro cadastrado.',
                                        style: TextStyle(
                                          fontSize: 16,
                                          fontWeight: FontWeight.bold,
                                          color: Colors.grey.shade700,
                                        ),
                                      ),
                                      const SizedBox(height: 8),
                                      Text(
                                        isInactiveFilter
                                            ? 'Membros que forem inativados aparecerão neste filtro.'
                                            : 'Adicione o primeiro membro do seu grupo tocando no botão abaixo.',
                                        textAlign: TextAlign.center,
                                        style: TextStyle(color: Colors.grey.shade600, fontSize: 13),
                                      ),
                                    ],
                                  ),
                                ),
                              )
                            : ListView.builder(
                                itemCount: widget.listController.members.length,
                                itemBuilder: (context, index) {
                                  final member = widget.listController.members[index];
                                  return MemberCard(
                                    member: member,
                                    onTap: () {
                                      if (widget.onSelectMember != null) {
                                        widget.onSelectMember!(member.id);
                                      }
                                    },
                                  );
                                },
                              ),
              ),
            ],
          ),
          floatingActionButton: canManage && !isInactiveFilter
              ? FloatingActionButton.extended(
                  onPressed: widget.onAddMember,
                  backgroundColor: Colors.blueGrey.shade900,
                  foregroundColor: Colors.white,
                  icon: const Icon(Icons.person_add),
                  label: const Text('Novo Membro'),
                )
              : null,
        );
      },
    );
  }
}
