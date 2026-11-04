import '../../domain/entities/member.dart';
import '../../domain/enums/member_enums.dart';
import '../../domain/repositories/member_repository.dart';
import '../datasources/member_remote_data_source.dart';

class MemberRepositoryImpl implements MemberRepository {
  final MemberRemoteDataSource remoteDataSource;

  MemberRepositoryImpl({required this.remoteDataSource});

  @override
  Future<Member> createMember({
    required String name,
    required String phone,
    String? email,
    required MemberRole role,
    required DateTime birthDate,
  }) {
    return remoteDataSource.createMember(
      name: name,
      phone: phone,
      email: email,
      role: role,
      birthDate: birthDate,
    );
  }

  @override
  Future<List<Member>> getMembers({
    MemberStatus? status,
    MemberRole? role,
    String? search,
    int? birthdayMonth,
  }) {
    return remoteDataSource.getMembers(
      status: status,
      role: role,
      search: search,
      birthdayMonth: birthdayMonth,
    );
  }

  @override
  Future<Member> getMemberById(String id) {
    return remoteDataSource.getMemberById(id);
  }

  @override
  Future<Member> updateMember({
    required String id,
    required String name,
    required String phone,
    String? email,
    required MemberRole role,
    required DateTime birthDate,
  }) {
    return remoteDataSource.updateMember(
      id: id,
      name: name,
      phone: phone,
      email: email,
      role: role,
      birthDate: birthDate,
    );
  }

  @override
  Future<Member> deactivateMember(String id) {
    return remoteDataSource.deactivateMember(id);
  }

  @override
  Future<Member> reactivateMember(String id) {
    return remoteDataSource.reactivateMember(id);
  }

  Future<List<Member>> getUpcomingBirthdays({int days = 30}) {
    return remoteDataSource.getUpcomingBirthdays(days: days);
  }
}
