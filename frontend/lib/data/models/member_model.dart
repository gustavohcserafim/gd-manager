import '../../domain/entities/member.dart';
import '../../domain/enums/member_enums.dart';

class MemberModel extends Member {
  const MemberModel({
    required super.id,
    required super.name,
    required super.phone,
    super.email,
    required super.role,
    required super.status,
    required super.initials,
    super.birthDate,
    required super.createdAt,
    required super.updatedAt,
  });

  factory MemberModel.fromJson(Map<String, dynamic> json) {
    DateTime? parsedBirthDate;
    if (json['birth_date'] != null && (json['birth_date'] as String).trim().isNotEmpty) {
      parsedBirthDate = DateTime.parse(json['birth_date'] as String);
    }

    return MemberModel(
      id: json['id'] as String,
      name: json['name'] as String,
      phone: json['phone'] as String,
      email: json['email'] as String?,
      role: MemberRole.fromString(json['role'] as String? ?? 'normal'),
      status: MemberStatus.fromString(json['status'] as String? ?? 'active'),
      initials: json['initials'] as String? ?? _calculateInitials(json['name'] as String? ?? ''),
      birthDate: parsedBirthDate,
      createdAt: DateTime.parse(json['created_at'] as String),
      updatedAt: DateTime.parse(json['updated_at'] as String),
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'phone': phone,
      'email': email,
      'role': role.value,
      'status': status.value,
      'initials': initials,
      'birth_date': birthDate != null
          ? "${birthDate!.year.toString().padLeft(4, '0')}-${birthDate!.month.toString().padLeft(2, '0')}-${birthDate!.day.toString().padLeft(2, '0')}"
          : null,
      'created_at': createdAt.toIso8601String(),
      'updated_at': updatedAt.toIso8601String(),
    };
  }

  static String _calculateInitials(String name) {
    final parts = name.trim().split(RegExp(r'\s+'));
    if (parts.isEmpty || parts[0].isEmpty) return '';
    if (parts.length == 1) return parts[0][0].toUpperCase();
    return (parts[0][0] + parts.last[0]).toUpperCase();
  }
}
