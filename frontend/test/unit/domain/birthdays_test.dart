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
    required DateTime birthDate,
  }) async {
    final member = Member(
      id: 'test-id',
      name: name,
      phone: phone,
      email: email,
      role: role,
      status: MemberStatus.active,
      initials: 'CP',
      birthDate: birthDate,
      createdAt: DateTime.now(),
      updatedAt: DateTime.now(),
    );
    members.add(member);
    return member;
  }

  @override
  Future<List<Member>> getMembers({
    MemberStatus? status,
    MemberRole? role,
    String? search,
    int? birthdayMonth,
  }) async => members;

  @override
  Future<Member> getMemberById(String id) async => members.first;

  @override
  Future<Member> updateMember({
    required String id,
    required String name,
    required String phone,
    String? email,
    required MemberRole role,
    required DateTime birthDate,
  }) async => members.first;

  @override
  Future<Member> deactivateMember(String id) async => members.first;

  @override
  Future<Member> reactivateMember(String id) async => members.first;
}

void main() {
  group('Member Birthday Domain Tests', () {
    test('Member entity stores birthDate and computes birthdayDisplay', () {
      final member = Member(
        id: '1',
        name: 'Ana Costa',
        phone: '11988887777',
        role: MemberRole.core,
        status: MemberStatus.active,
        initials: 'AC',
        birthDate: DateTime(1995, 5, 15),
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
      );

      expect(member.birthDate, DateTime(1995, 5, 15));
      expect(member.birthdayDisplay, '15 de Maio');
      expect(member.birthDateFormatted, '15/05/1995');
      expect(member.age, isNotNull);
      expect(member.age, greaterThanOrEqualTo(25));
    });

    test('Member entity without birthDate returns null for age and display', () {
      final member = Member(
        id: 'legacy-1',
        name: 'Membro Legado',
        phone: '11988887777',
        role: MemberRole.normal,
        status: MemberStatus.active,
        initials: 'ML',
        birthDate: null,
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
      );

      expect(member.birthDate, isNull);
      expect(member.birthdayDisplay, isNull);
      expect(member.birthDateFormatted, isNull);
      expect(member.age, isNull);
      expect(member.isBirthdayToday, isFalse);
      expect(member.daysUntilBirthday, isNull);
    });

    test('isBirthdayToday returns true when month and day match today', () {
      final now = DateTime.now();
      final member = Member(
        id: 'bday-1',
        name: 'Aniversariante',
        phone: '11988887777',
        role: MemberRole.leader,
        status: MemberStatus.active,
        initials: 'AN',
        birthDate: DateTime(1990, now.month, now.day),
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
      );

      expect(member.isBirthdayToday, isTrue);
      expect(member.daysUntilBirthday, 0);
    });

    test('CreateMember use case passes birthDate to repository', () async {
      final repo = MockMemberRepository();
      final useCase = CreateMember(repo);

      final birthDate = DateTime(1992, 10, 20);
      final result = await useCase(
        name: 'Juliana Lima',
        phone: '11977778888',
        role: MemberRole.core,
        birthDate: birthDate,
      );

      expect(result.birthDate, birthDate);
      expect(repo.members.length, 1);
      expect(repo.members.first.birthDate, birthDate);
    });
  });
}
