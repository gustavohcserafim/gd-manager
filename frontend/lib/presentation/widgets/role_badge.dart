import 'package:flutter/material.dart';
import '../../domain/enums/member_enums.dart';

class RoleBadge extends StatelessWidget {
  final MemberRole role;

  const RoleBadge({super.key, required this.role});

  @override
  Widget build(BuildContext context) {
    Color bg;
    Color fg;

    switch (role) {
      case MemberRole.leader:
        bg = Colors.amber.shade100;
        fg = Colors.amber.shade900;
        break;
      case MemberRole.core:
        bg = Colors.teal.shade50;
        fg = Colors.teal.shade800;
        break;
      case MemberRole.normal:
      default:
        bg = Colors.grey.shade200;
        fg = Colors.grey.shade800;
        break;
    }

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: bg,
        borderRadius: BorderRadius.circular(12),
        border: Border.all(color: fg.withValues(alpha: 0.3)),
      ),
      child: Text(
        role.label,
        style: TextStyle(
          color: fg,
          fontSize: 11,
          fontWeight: FontWeight.bold,
        ),
      ),
    );
  }
}
