import 'package:flutter_test/flutter_test.dart';
import 'package:gd_manager/domain/entities/member.dart';
import 'package:gd_manager/domain/enums/member_enums.dart';
import 'package:gd_manager/domain/repositories/member_repository.dart';
import 'package:gd_manager/domain/use_cases/create_member.dart';
import 'package:gd_manager/presentation/controllers/member_form_controller.dart';

class FakeMemberRepository implements MemberRepository {
  DateTime? lastCreatedBirthDate;

  @override
  Future<Member> createMember({
    required String name,
    required String phone,
    String? email,
    required MemberRole role,
    required DateTime birthDate,
  }) async {
    lastCreatedBirthDate = birthDate;
    return Member(
      id: 'uuid-1',
      name: name,
      phone: phone,
      email: email,
      role: role,
      status: MemberStatus.active,
      initials: 'AS',
      birthDate: birthDate,
      createdAt: DateTime.now(),
      updatedAt: DateTime.now(),
    );
  }

  @override
  Future<List<Member>> getMembers({MemberStatus? status, MemberRole? role, String? search, int? birthdayMonth}) async => [];
  @override
  Future<Member> getMemberById(String id) async => throw UnimplementedError();
  @override
  Future<Member> updateMember({required String id, required String name, required String phone, String? email, required MemberRole role, required DateTime birthDate}) async => throw UnimplementedError();
  @override
  Future<Member> deactivateMember(String id) async => throw UnimplementedError();
  @override
  Future<Member> reactivateMember(String id) async => throw UnimplementedError();
}

void main() {
  group('MemberFormController Birthday Tests', () {
    test('MemberFormController fails validation when birthDate is missing', () async {
      final repo = FakeMemberRepository();
      final createUseCase = CreateMember(repo);
      final controller = MemberFormController(createMemberUseCase: createUseCase);

      controller.nameController.text = 'Ana Silva';
      controller.phoneController.text = '11988887777';
      controller.selectedRole = MemberRole.leader;
      controller.selectedBirthDate = null;

      final success = await controller.submit();
      expect(success, isFalse);
      expect(controller.errorMessage, contains('nascimento'));
    });

    test('MemberFormController succeeds when valid birthDate is set', () async {
      final repo = FakeMemberRepository();
      final createUseCase = CreateMember(repo);
      final controller = MemberFormController(createMemberUseCase: createUseCase);

      controller.nameController.text = 'Ana Silva';
      controller.phoneController.text = '11988887777';
      controller.selectedRole = MemberRole.leader;
      final bdate = DateTime(1995, 5, 15);
      controller.setBirthDate(bdate);

      final success = await controller.submit();
      expect(success, isTrue);
      expect(controller.errorMessage, isNull);
      expect(controller.formattedBirthDate, '15/05/1995');
      expect(controller.birthDateController.text, '15/05/1995');
      expect(repo.lastCreatedBirthDate, bdate);
    });

    test('MemberFormController parses typed DD/MM/AAAA format', () async {
      final repo = FakeMemberRepository();
      final createUseCase = CreateMember(repo);
      final controller = MemberFormController(createMemberUseCase: createUseCase);

      controller.nameController.text = 'Ana Silva';
      controller.phoneController.text = '11988887777';
      controller.selectedRole = MemberRole.leader;
      controller.birthDateController.text = '20/10/1988';

      final success = await controller.submit();
      expect(success, isTrue);
      expect(controller.selectedBirthDate, equals(DateTime(1988, 10, 20)));
      expect(repo.lastCreatedBirthDate, equals(DateTime(1988, 10, 20)));
    });

    test('MemberFormController rejects invalid typed date', () async {
      final repo = FakeMemberRepository();
      final createUseCase = CreateMember(repo);
      final controller = MemberFormController(createMemberUseCase: createUseCase);

      controller.nameController.text = 'Ana Silva';
      controller.phoneController.text = '11988887777';
      controller.birthDateController.text = '32/01/1990';

      final success = await controller.submit();
      expect(success, isFalse);
      expect(controller.errorMessage, contains('DD/MM/AAAA'));
    });
  });
}
