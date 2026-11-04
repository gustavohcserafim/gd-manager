import 'package:flutter/material.dart';
import '../../domain/enums/member_enums.dart';
import '../controllers/session_context_controller.dart';

class UserRoleSelectorBar extends StatelessWidget {
  final SessionContextController sessionController;

  const UserRoleSelectorBar({
    super.key,
    required this.sessionController,
  });

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: sessionController,
      builder: (context, _) {
        final activeRole = sessionController.activeRole;
        return Container(
          color: Colors.blueGrey.shade900,
          padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
          child: Row(
            children: [
              const Icon(Icons.shield_outlined, color: Colors.amberAccent, size: 20),
              const SizedBox(width: 8),
              const Text(
                'Perfil Ativo:',
                style: TextStyle(color: Colors.white, fontWeight: FontWeight.bold, fontSize: 13),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Row(
                    children: MemberRole.values.map((role) {
                      final isSelected = role == activeRole;
                      return Padding(
                        padding: const EdgeInsets.only(right: 8.0),
                        child: ChoiceChip(
                          label: Text(role.label),
                          selected: isSelected,
                          selectedColor: Colors.amberAccent,
                          labelStyle: TextStyle(
                            color: isSelected ? Colors.black87 : Colors.white70,
                            fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                            fontSize: 12,
                          ),
                          backgroundColor: Colors.blueGrey.shade800,
                          onSelected: (_) => sessionController.switchRole(role),
                        ),
                      );
                    }).toList(),
                  ),
                ),
              ),
            ],
          ),
        );
      },
    );
  }
}
