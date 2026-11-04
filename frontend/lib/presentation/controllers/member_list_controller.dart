import 'package:flutter/foundation.dart';
import '../../domain/entities/member.dart';
import '../../domain/enums/member_enums.dart';
import '../../domain/use_cases/get_members.dart';

class MemberListController extends ChangeNotifier {
  final GetMembers getMembersUseCase;

  List<Member> _members = [];
  bool _isLoading = false;
  String? _errorMessage;

  MemberStatus _selectedStatus = MemberStatus.active;
  MemberRole? _selectedRole;
  String _searchQuery = '';

  MemberListController({required this.getMembersUseCase});

  List<Member> get members => _members;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;
  MemberStatus get selectedStatus => _selectedStatus;
  MemberRole? get selectedRole => _selectedRole;
  String get searchQuery => _searchQuery;

  Future<void> loadMembers() async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      _members = await getMembersUseCase(
        status: _selectedStatus,
        role: _selectedRole,
        search: _searchQuery.trim().isEmpty ? null : _searchQuery.trim(),
      );
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _isLoading = false;
      _errorMessage = e.toString().replaceAll('Exception:', '').trim();
      notifyListeners();
    }
  }

  void setStatus(MemberStatus status) {
    if (_selectedStatus == status) return;
    _selectedStatus = status;
    loadMembers();
  }

  void setRole(MemberRole? role) {
    if (_selectedRole == role) return;
    _selectedRole = role;
    loadMembers();
  }

  void setSearch(String query) {
    _searchQuery = query;
    loadMembers();
  }
}
