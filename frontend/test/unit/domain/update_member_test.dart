import 'package:flutter_test/flutter_test.dart';
import 'package:gd_manager/domain/entities/member.dart';
import 'package:gd_manager/domain/enums/member_enums.dart';
import 'package:gd_manager/domain/repositories/member_repository.dart';
import 'package:gd_manager/domain/use_cases/update_member.dart';

class StubUpdateMemberRepository implements MemberRepository {
  @override
  Future<Member> updateMember({
    required String id,
    required String name,
    required String phone,
    String? email,
    required MemberRole role,
    required DateTime birthDate,
  }) async {
    return Member(
      id: id,
      name: name,
      phone: phone,
      email: email,
      role: role,
      status: MemberStatus.active,
      initials: 'JL',
      birthDate: birthDate,
      createdAt: DateTime.now(),
      updatedAt: DateTime.now(),
    );
  }

  @override
  Future<Member> getMemberById(String id) async {
    return Member(
      id: id,
      name: 'João Lucas',
      phone: '11900001111',
      role: MemberRole.normal,
      status: MemberStatus.active,
      initials: 'JL',
      birthDate: DateTime(1993, 2, 10),
      createdAt: DateTime.now(),
      updatedAt: DateTime.now(),
    );
  }

  @override
  Future<Member> createMember({required String name, required String phone, String? email, required MemberRole role, required DateTime birthDate}) async => throw UnimplementedError();
  @override
  Future<List<Member>> getMembers({MemberStatus? status, MemberRole? role, String? search, int? birthdayMonth}) async => throw UnimplementedError();
  @override
  Future<Member> deactivateMember(String id) async => throw UnimplementedError();
  @override
  Future<Member> reactivateMember(String id) async => throw UnimplementedError();
}

void main() {
  test('UpdateMember use case updates and returns member', () async {
    final repo = StubUpdateMemberRepository();
    final useCase = UpdateMember(repo);

    final updated = await useCase(
      id: 'id-1',
      name: 'João Lucas Lima',
      phone: '11900002222',
      role: MemberRole.core,
      birthDate: DateTime(1993, 2, 10),
    );

    expect(updated.name, 'João Lucas Lima');
    expect(updated.role, MemberRole.core);
    expect(updated.birthDate, DateTime(1993, 2, 10));
  });
}
