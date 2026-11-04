import 'package:flutter/foundation.dart';
import '../../domain/entities/member.dart';
import '../../domain/enums/member_enums.dart';
import '../../domain/use_cases/get_members.dart';
import '../../domain/use_cases/get_upcoming_birthdays.dart';

class MemberListController extends ChangeNotifier {
  final GetMembers getMembersUseCase;
  final GetUpcomingBirthdays? getUpcomingBirthdaysUseCase;

  List<Member> _members = [];
  List<Member> _upcomingBirthdays = [];
  bool _isLoading = false;
  String? _errorMessage;

  MemberStatus _selectedStatus = MemberStatus.active;
  MemberRole? _selectedRole;
  int? _selectedBirthdayMonth;
  String _searchQuery = '';

  MemberListController({
    required this.getMembersUseCase,
    this.getUpcomingBirthdaysUseCase,
  });

  List<Member> get members => _members;
  List<Member> get upcomingBirthdays => _upcomingBirthdays;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;
  MemberStatus get selectedStatus => _selectedStatus;
  MemberRole? get selectedRole => _selectedRole;
  int? get selectedBirthdayMonth => _selectedBirthdayMonth;
  String get searchQuery => _searchQuery;

  Future<void> loadMembers() async {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      final membersFuture = getMembersUseCase(
        status: _selectedStatus,
        role: _selectedRole,
        search: _searchQuery.trim().isEmpty ? null : _searchQuery.trim(),
        birthdayMonth: _selectedBirthdayMonth,
      );

      final upcomingFuture = getUpcomingBirthdaysUseCase != null
          ? getUpcomingBirthdaysUseCase!(days: 30)
          : Future.value(<Member>[]);

      final results = await Future.wait([membersFuture, upcomingFuture]);
      _members = results[0];
      _upcomingBirthdays = results[1];

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

  Future<void> setBirthdayMonth(int? month) async {
    if (_selectedBirthdayMonth == month) return;
    _selectedBirthdayMonth = month;
    await loadMembers();
  }

  void setSearch(String query) {
    _searchQuery = query;
    loadMembers();
  }
}
