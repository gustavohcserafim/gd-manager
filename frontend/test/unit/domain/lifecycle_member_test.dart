import 'package:flutter_test/flutter_test.dart';
import 'package:gd_manager/domain/entities/member.dart';
import 'package:gd_manager/domain/enums/member_enums.dart';
import 'package:gd_manager/domain/repositories/member_repository.dart';
import 'package:gd_manager/domain/use_cases/lifecycle_member.dart';

class StubLifecycleRepository implements MemberRepository {
  Member member = Member(
    id: 'life-1',
    name: 'Olivia Rodrigo',
    phone: '11988881234',
    role: MemberRole.normal,
    status: MemberStatus.active,
    initials: 'OR',
    birthDate: DateTime(2003, 2, 20),
    createdAt: DateTime.now(),
    updatedAt: DateTime.now(),
  );

  @override
  Future<Member> deactivateMember(String id) async {
    member = Member(
      id: member.id,
      name: member.name,
      phone: member.phone,
      email: member.email,
      role: member.role,
      status: MemberStatus.inactive,
      initials: member.initials,
      birthDate: member.birthDate,
      createdAt: member.createdAt,
      updatedAt: DateTime.now(),
    );
    return member;
  }

  @override
  Future<Member> reactivateMember(String id) async {
    member = Member(
      id: member.id,
      name: member.name,
      phone: member.phone,
      email: member.email,
      role: member.role,
      status: MemberStatus.active,
      initials: member.initials,
      birthDate: member.birthDate,
      createdAt: member.createdAt,
      updatedAt: DateTime.now(),
    );
    return member;
  }

  @override
  Future<Member> createMember({required String name, required String phone, String? email, required MemberRole role, required DateTime birthDate}) async => throw UnimplementedError();
  @override
  Future<List<Member>> getMembers({MemberStatus? status, MemberRole? role, String? search, int? birthdayMonth}) async => throw UnimplementedError();
  @override
  Future<Member> getMemberById(String id) async => throw UnimplementedError();
  @override
  Future<Member> updateMember({required String id, required String name, required String phone, String? email, required MemberRole role, required DateTime birthDate}) async => throw UnimplementedError();
}

void main() {
  test('DeactivateMember changes member status to inactive', () async {
    final repo = StubLifecycleRepository();
    final useCase = DeactivateMember(repo);

    final result = await useCase('life-1');
    expect(result.status, MemberStatus.inactive);
    expect(result.isActive, isFalse);
  });

  test('ReactivateMember changes member status to active', () async {
    final repo = StubLifecycleRepository();
    repo.member = Member(
      id: 'life-1',
      name: 'Olivia Rodrigo',
      phone: '11988881234',
      role: MemberRole.normal,
      status: MemberStatus.inactive,
      initials: 'OR',
      birthDate: DateTime(2003, 2, 20),
      createdAt: DateTime.now(),
      updatedAt: DateTime.now(),
    );

    final useCase = ReactivateMember(repo);
    final result = await useCase('life-1');
    expect(result.status, MemberStatus.active);
    expect(result.isActive, isTrue);
  });
}
