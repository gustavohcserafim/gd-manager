import 'package:flutter/material.dart';
import '../../domain/enums/member_enums.dart';

class MemberAvatar extends StatelessWidget {
  final String initials;
  final MemberRole? role;
  final double radius;

  const MemberAvatar({
    super.key,
    required this.initials,
    this.role,
    this.radius = 24,
  });

  Color _getColorForRole(MemberRole? role) {
    switch (role) {
      case MemberRole.leader:
        return Colors.indigo.shade700;
      case MemberRole.core:
        return Colors.teal.shade700;
      case MemberRole.normal:
      default:
        return Colors.blueGrey.shade600;
    }
  }

  @override
  Widget build(BuildContext context) {
    return CircleAvatar(
      radius: radius,
      backgroundColor: _getColorForRole(role),
      child: Text(
        initials.toUpperCase(),
        style: TextStyle(
          color: Colors.white,
          fontWeight: FontWeight.bold,
          fontSize: radius * 0.75,
        ),
      ),
    );
  }
}
