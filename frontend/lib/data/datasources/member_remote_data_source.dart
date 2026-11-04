import '../../domain/enums/member_enums.dart';
import '../models/member_model.dart';
import 'api_client.dart';

abstract class MemberRemoteDataSource {
  Future<MemberModel> createMember({
    required String name,
    required String phone,
    String? email,
    required MemberRole role,
    required DateTime birthDate,
  });

  Future<List<MemberModel>> getMembers({
    MemberStatus? status,
    MemberRole? role,
    String? search,
    int? birthdayMonth,
  });

  Future<MemberModel> getMemberById(String id);

  Future<MemberModel> updateMember({
    required String id,
    required String name,
    required String phone,
    String? email,
    required MemberRole role,
    required DateTime birthDate,
  });

  Future<MemberModel> deactivateMember(String id);

  Future<MemberModel> reactivateMember(String id);

  Future<List<MemberModel>> getUpcomingBirthdays({int days = 30});
}

class MemberRemoteDataSourceImpl implements MemberRemoteDataSource {
  final ApiClient apiClient;

  MemberRemoteDataSourceImpl({required this.apiClient});

  static String _formatDate(DateTime dt) {
    return "${dt.year.toString().padLeft(4, '0')}-${dt.month.toString().padLeft(2, '0')}-${dt.day.toString().padLeft(2, '0')}";
  }

  @override
  Future<MemberModel> createMember({
    required String name,
    required String phone,
    String? email,
    required MemberRole role,
    required DateTime birthDate,
  }) async {
    final response = await apiClient.post('/members', {
      'name': name,
      'phone': phone,
      'email': email,
      'role': role.value,
      'birth_date': _formatDate(birthDate),
    });
    return MemberModel.fromJson(response as Map<String, dynamic>);
  }

  @override
  Future<List<MemberModel>> getMembers({
    MemberStatus? status,
    MemberRole? role,
    String? search,
    int? birthdayMonth,
  }) async {
    final queryParams = <String, String>{};
    if (status != null) queryParams['status'] = status.value;
    if (role != null) queryParams['role'] = role.value;
    if (search != null && search.trim().isNotEmpty) queryParams['search'] = search.trim();
    if (birthdayMonth != null) queryParams['birthday_month'] = birthdayMonth.toString();

    final response = await apiClient.get('/members', queryParams: queryParams.isEmpty ? null : queryParams);
    final list = response as List;
    return list.map((item) => MemberModel.fromJson(item as Map<String, dynamic>)).toList();
  }

  @override
  Future<MemberModel> getMemberById(String id) async {
    final response = await apiClient.get('/members/$id');
    return MemberModel.fromJson(response as Map<String, dynamic>);
  }

  @override
  Future<MemberModel> updateMember({
    required String id,
    required String name,
    required String phone,
    String? email,
    required MemberRole role,
    required DateTime birthDate,
  }) async {
    final response = await apiClient.put('/members/$id', {
      'name': name,
      'phone': phone,
      'email': email,
      'role': role.value,
      'birth_date': _formatDate(birthDate),
    });
    return MemberModel.fromJson(response as Map<String, dynamic>);
  }

  @override
  Future<MemberModel> deactivateMember(String id) async {
    final response = await apiClient.delete('/members/$id');
    return MemberModel.fromJson(response as Map<String, dynamic>);
  }

  @override
  Future<MemberModel> reactivateMember(String id) async {
    final response = await apiClient.patch('/members/$id/reactivate');
    return MemberModel.fromJson(response as Map<String, dynamic>);
  }

  @override
  Future<List<MemberModel>> getUpcomingBirthdays({int days = 30}) async {
    final response = await apiClient.get('/members/birthdays/upcoming', queryParams: {'days': days.toString()});
    final list = response as List;
    return list.map((item) => MemberModel.fromJson(item as Map<String, dynamic>)).toList();
  }
}
