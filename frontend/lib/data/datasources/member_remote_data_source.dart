import '../../domain/enums/member_enums.dart';
import '../models/member_model.dart';
import 'api_client.dart';

abstract class MemberRemoteDataSource {
  Future<MemberModel> createMember({
    required String name,
    required String phone,
    String? email,
    required MemberRole role,
  });

  Future<List<MemberModel>> getMembers({
    MemberStatus? status,
    MemberRole? role,
    String? search,
  });

  Future<MemberModel> getMemberById(String id);

  Future<MemberModel> updateMember({
    required String id,
    required String name,
    required String phone,
    String? email,
    required MemberRole role,
  });

  Future<MemberModel> deactivateMember(String id);

  Future<MemberModel> reactivateMember(String id);
}

class MemberRemoteDataSourceImpl implements MemberRemoteDataSource {
  final ApiClient apiClient;

  MemberRemoteDataSourceImpl({required this.apiClient});

  @override
  Future<MemberModel> createMember({
    required String name,
    required String phone,
    String? email,
    required MemberRole role,
  }) async {
    final response = await apiClient.post('/members', {
      'name': name,
      'phone': phone,
      'email': email,
      'role': role.value,
    });
    return MemberModel.fromJson(response as Map<String, dynamic>);
  }

  @override
  Future<List<MemberModel>> getMembers({
    MemberStatus? status,
    MemberRole? role,
    String? search,
  }) async {
    final queryParams = <String, String>{};
    if (status != null) queryParams['status'] = status.value;
    if (role != null) queryParams['role'] = role.value;
    if (search != null && search.trim().isNotEmpty) queryParams['search'] = search.trim();

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
  }) async {
    final response = await apiClient.put('/members/$id', {
      'name': name,
      'phone': phone,
      'email': email,
      'role': role.value,
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
}
