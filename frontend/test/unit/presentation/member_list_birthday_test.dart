import 'package:flutter_test/flutter_test.dart';
import 'package:gd_manager/domain/entities/member.dart';
import 'package:gd_manager/domain/enums/member_enums.dart';
import 'package:gd_manager/domain/repositories/member_repository.dart';
import 'package:gd_manager/domain/use_cases/get_members.dart';
import 'package:gd_manager/domain/use_cases/get_upcoming_birthdays.dart';
import 'package:gd_manager/presentation/controllers/member_list_controller.dart';

class StubMemberRepository implements MemberRepository {
  final List<Member> allMembers;

  StubMemberRepository(this.allMembers);

  @override
  Future<List<Member>> getMembers({
    MemberStatus? status,
    MemberRole? role,
    String? search,
    int? birthdayMonth,
  }) async {
    var list = allMembers;
    if (status != null) list = list.where((m) => m.status == status).toList();
    if (role != null) list = list.where((m) => m.role == role).toList();
    if (search != null) list = list.where((m) => m.name.toLowerCase().contains(search.toLowerCase())).toList();
    if (birthdayMonth != null) list = list.where((m) => m.birthDate?.month == birthdayMonth).toList();
    return list;
  }

  @override
  Future<Member> getMemberById(String id) async => allMembers.firstWhere((m) => m.id == id);

  @override
  Future<Member> createMember({required String name, required String phone, String? email, required MemberRole role, required DateTime birthDate}) async => throw UnimplementedError();

  @override
  Future<Member> updateMember({required String id, required String name, required String phone, String? email, required MemberRole role, required DateTime birthDate}) async => throw UnimplementedError();

  @override
  Future<Member> deactivateMember(String id) async => throw UnimplementedError();

  @override
  Future<Member> reactivateMember(String id) async => throw UnimplementedError();
}

void main() {
  group('MemberListController Birthday Month & Upcoming Tests', () {
    final now = DateTime.now();
    final m1 = Member(
      id: '1',
      name: 'Maria Maio',
      phone: '11988880001',
      role: MemberRole.leader,
      status: MemberStatus.active,
      initials: 'MM',
      birthDate: DateTime(1990, 5, 10),
      createdAt: now,
      updatedAt: now,
    );
    final m2 = Member(
      id: '2',
      name: 'João Junho',
      phone: '11988880002',
      role: MemberRole.core,
      status: MemberStatus.active,
      initials: 'JJ',
      birthDate: DateTime(1992, 6, 15),
      createdAt: now,
      updatedAt: now,
    );

    test('GetMembers with birthdayMonth filter returns only matching members', () async {
      final repo = StubMemberRepository([m1, m2]);
      final useCase = GetMembers(repo);

      final resultMay = await useCase(birthdayMonth: 5);
      expect(resultMay.length, 1);
      expect(resultMay.first.name, 'Maria Maio');

      final resultJune = await useCase(birthdayMonth: 6);
      expect(resultJune.length, 1);
      expect(resultJune.first.name, 'João Junho');
    });

    test('MemberListController sets birthday month and reloads members', () async {
      final repo = StubMemberRepository([m1, m2]);
      final getMembersUseCase = GetMembers(repo);
      final controller = MemberListController(getMembersUseCase: getMembersUseCase);

      await controller.loadMembers();
      expect(controller.members.length, 2);

      await controller.setBirthdayMonth(5);
      expect(controller.selectedBirthdayMonth, 5);
      expect(controller.members.length, 1);
      expect(controller.members.first.name, 'Maria Maio');

      await controller.setBirthdayMonth(null);
      expect(controller.selectedBirthdayMonth, isNull);
      expect(controller.members.length, 2);
    });
  });
}
