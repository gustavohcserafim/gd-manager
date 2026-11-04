import 'package:flutter_test/flutter_test.dart';
import 'package:gd_manager/domain/entities/member.dart';
import 'package:gd_manager/domain/enums/member_enums.dart';
import 'package:gd_manager/domain/repositories/member_repository.dart';
import 'package:gd_manager/domain/use_cases/create_member.dart';

class MockMemberRepository implements MemberRepository {
  final List<Member> members = [];

  @override
  Future<Member> createMember({
    required String name,
    required String phone,
    String? email,
    required MemberRole role,
  }) async {
    final member = Member(
      id: 'test-id',
      name: name,
      phone: phone,
      email: email,
      role: role,
      status: MemberStatus.active,
      initials: 'CP',
      createdAt: DateTime.now(),
      updatedAt: DateTime.now(),
    );
    members.add(member);
    return member;
  }

  @override
  Future<List<Member>> getMembers({MemberStatus? status, MemberRole? role, String? search}) async => members;

  @override
  Future<Member> getMemberById(String id) async => members.first;

  @override
  Future<Member> updateMember({required String id, required String name, required String phone, String? email, required MemberRole role}) async => members.first;

  @override
  Future<Member> deactivateMember(String id) async => members.first;

  @override
  Future<Member> reactivateMember(String id) async => members.first;
}

void main() {
  test('CreateMember use case creates member successfully', () async {
    final repo = MockMemberRepository();
    final useCase = CreateMember(repo);

    final result = await useCase(
      name: 'Carlos Pereira',
      phone: '11999990001',
      role: MemberRole.leader,
    );

    assert(result.name == 'Carlos Pereira');
    assert(result.phone == '11999990001');
    assert(result.role == MemberRole.leader);
    assert(result.status == MemberStatus.active);
  });
}
