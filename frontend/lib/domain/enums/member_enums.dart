enum MemberRole {
  leader('leader', 'Líder'),
  core('core', 'Membro do Núcleo'),
  normal('normal', 'Normal');

  final String value;
  final String label;

  const MemberRole(this.value, this.label);

  static MemberRole fromString(String val) {
    final normalized = val.toLowerCase().trim();
    for (final role in MemberRole.values) {
      if (role.value == normalized) return role;
    }
    return MemberRole.normal;
  }

  bool get canManageMembers => this == MemberRole.leader || this == MemberRole.core;
}

enum MemberStatus {
  active('active', 'Ativo'),
  inactive('inactive', 'Inativo');

  final String value;
  final String label;

  const MemberStatus(this.value, this.label);

  static MemberStatus fromString(String val) {
    final normalized = val.toLowerCase().trim();
    for (final status in MemberStatus.values) {
      if (status.value == normalized) return status;
    }
    return MemberStatus.active;
  }
}
