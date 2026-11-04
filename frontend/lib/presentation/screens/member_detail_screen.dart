import 'package:flutter/material.dart';
import '../../domain/entities/member.dart';
import '../controllers/session_context_controller.dart';
import '../widgets/member_avatar.dart';
import '../widgets/role_badge.dart';

class MemberDetailScreen extends StatelessWidget {
  final Member member;
  final SessionContextController sessionController;
  final VoidCallback? onEdit;
  final VoidCallback? onDeactivate;
  final VoidCallback? onReactivate;

  const MemberDetailScreen({
    super.key,
    required this.member,
    required this.sessionController,
    this.onEdit,
    this.onDeactivate,
    this.onReactivate,
  });

  String _formatBirthDate(DateTime dt) {
    final d = dt.day.toString().padLeft(2, '0');
    final m = dt.month.toString().padLeft(2, '0');
    final y = dt.year.toString().padLeft(4, '0');
    return '$d/$m/$y';
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: sessionController,
      builder: (context, _) {
        final canManage = sessionController.canManage;

        return Scaffold(
          appBar: AppBar(
            title: const Text('Detalhes do Membro'),
            backgroundColor: Colors.blueGrey.shade900,
            foregroundColor: Colors.white,
            actions: [
              if (canManage && member.isActive && onEdit != null)
                IconButton(
                  icon: const Icon(Icons.edit),
                  tooltip: 'Editar',
                  onPressed: onEdit,
                ),
            ],
          ),
          body: SingleChildScrollView(
            padding: const EdgeInsets.all(20),
            child: Column(
              children: [
                // Header com avatar grande e badges
                Center(
                  child: Column(
                    children: [
                      MemberAvatar(
                        initials: member.initials,
                        role: member.role,
                        radius: 40,
                      ),
                      const SizedBox(height: 12),
                      Text(
                        member.name,
                        style: const TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: 8),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          RoleBadge(role: member.role),
                          const SizedBox(width: 8),
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                            decoration: BoxDecoration(
                              color: member.isActive ? Colors.green.shade50 : Colors.red.shade50,
                              borderRadius: BorderRadius.circular(12),
                              border: Border.all(
                                color: member.isActive ? Colors.green.shade600 : Colors.red.shade600,
                              ),
                            ),
                            child: Text(
                              member.status.label,
                              style: TextStyle(
                                color: member.isActive ? Colors.green.shade800 : Colors.red.shade800,
                                fontSize: 11,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                          ),
                          if (member.isBirthdayToday) ...[
                            const SizedBox(width: 8),
                            Container(
                              padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
                              decoration: BoxDecoration(
                                color: Colors.amber.shade100,
                                borderRadius: BorderRadius.circular(12),
                                border: Border.all(color: Colors.amber.shade500),
                              ),
                              child: Text(
                                '🎂 Hoje!',
                                style: TextStyle(
                                  color: Colors.amber.shade900,
                                  fontSize: 11,
                                  fontWeight: FontWeight.bold,
                                ),
                              ),
                            ),
                          ],
                        ],
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 24),

                // Cartão de dados de contato e aniversário
                Card(
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                  elevation: 1,
                  child: Padding(
                    padding: const EdgeInsets.all(16),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text(
                          'Informações do Membro',
                          style: TextStyle(fontWeight: FontWeight.bold, fontSize: 15),
                        ),
                        const Divider(height: 20),
                        ListTile(
                          contentPadding: EdgeInsets.zero,
                          leading: const Icon(Icons.cake_outlined, color: Colors.blueGrey),
                          title: const Text('Data de Nascimento & Idade', style: TextStyle(fontSize: 12, color: Colors.grey)),
                          subtitle: Text(
                            member.birthDate != null
                                ? '${_formatBirthDate(member.birthDate!)} (${member.age ?? 0} anos)'
                                : 'Data não informada',
                            style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w600),
                          ),
                        ),
                        ListTile(
                          contentPadding: EdgeInsets.zero,
                          leading: const Icon(Icons.phone_outlined, color: Colors.blueGrey),
                          title: const Text('Telefone / WhatsApp', style: TextStyle(fontSize: 12, color: Colors.grey)),
                          subtitle: Text(
                            member.phone,
                            style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w600),
                          ),
                        ),
                        if (member.email != null)
                          ListTile(
                            contentPadding: EdgeInsets.zero,
                            leading: const Icon(Icons.email_outlined, color: Colors.blueGrey),
                            title: const Text('E-mail', style: TextStyle(fontSize: 12, color: Colors.grey)),
                            subtitle: Text(
                              member.email!,
                              style: const TextStyle(fontSize: 15, fontWeight: FontWeight.w600),
                            ),
                          ),
                      ],
                    ),
                  ),
                ),
                const SizedBox(height: 24),

                // Ações do gestor
                if (canManage) ...[
                  if (member.isActive) ...[
                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton.icon(
                        icon: const Icon(Icons.edit_outlined),
                        label: const Text('Editar Dados'),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.blueGrey.shade800,
                          foregroundColor: Colors.white,
                          padding: const EdgeInsets.symmetric(vertical: 14),
                        ),
                        onPressed: onEdit,
                      ),
                    ),
                    const SizedBox(height: 12),
                    SizedBox(
                      width: double.infinity,
                      child: OutlinedButton.icon(
                        icon: const Icon(Icons.person_off_outlined, color: Colors.red),
                        label: const Text('Inativar Membro', style: TextStyle(color: Colors.red)),
                        style: OutlinedButton.styleFrom(
                          side: const BorderSide(color: Colors.red),
                          padding: const EdgeInsets.symmetric(vertical: 14),
                        ),
                        onPressed: onDeactivate,
                      ),
                    ),
                  ] else ...[
                    SizedBox(
                      width: double.infinity,
                      child: ElevatedButton.icon(
                        icon: const Icon(Icons.replay_outlined),
                        label: const Text('Reativar Membro'),
                        style: ElevatedButton.styleFrom(
                          backgroundColor: Colors.green.shade800,
                          foregroundColor: Colors.white,
                          padding: const EdgeInsets.symmetric(vertical: 14),
                        ),
                        onPressed: onReactivate,
                      ),
                    ),
                  ],
                ],
              ],
            ),
          ),
        );
      },
    );
  }
}
