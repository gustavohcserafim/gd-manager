import 'package:flutter/foundation.dart';
import '../../data/datasources/api_client.dart';
import '../../domain/enums/member_enums.dart';

class SessionContextController extends ChangeNotifier {
  final ApiClient apiClient;
  MemberRole _activeRole;

  SessionContextController({
    required this.apiClient,
    MemberRole initialRole = MemberRole.leader,
  }) : _activeRole = initialRole {
    apiClient.updateRole(_activeRole);
  }

  MemberRole get activeRole => _activeRole;
  bool get canManage => _activeRole.canManageMembers;

  void switchRole(MemberRole newRole) {
    if (_activeRole == newRole) return;
    _activeRole = newRole;
    apiClient.updateRole(newRole);
    notifyListeners();
  }
}
