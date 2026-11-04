import '../enums/member_enums.dart';

class Member {
  final String id;
  final String name;
  final String phone;
  final String? email;
  final MemberRole role;
  final MemberStatus status;
  final String initials;
  final DateTime createdAt;
  final DateTime updatedAt;

  const Member({
    required this.id,
    required this.name,
    required this.phone,
    this.email,
    required this.role,
    required this.status,
    required this.initials,
    required this.createdAt,
    required this.updatedAt,
  });

  bool get isActive => status == MemberStatus.active;
}
