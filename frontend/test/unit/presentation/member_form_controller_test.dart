import 'package:flutter_test/flutter_test.dart';
import 'package:gd_manager/domain/entities/member.dart';
import 'package:gd_manager/domain/enums/member_enums.dart';
import 'package:gd_manager/domain/repositories/member_repository.dart';
import 'package:gd_manager/domain/use_cases/create_member.dart';
import 'package:gd_manager/presentation/controllers/member_form_controller.dart';

class FakeMemberRepository implements MemberRepository {
  @override
  Future<Member> createMember({
    required String name,
    required String phone,
    String? email,
    required MemberRole role,
  }) async {
    if (phone == '11999990001') {
      throw Exception('duplicate');
    }
    return Member(
      id: 'uuid-1',
      name: name,
      phone: phone,
      email: email,
      role: role,
      status: MemberStatus.active,
      initials: 'AS',
      createdAt: DateTime.now(),
      updatedAt: DateTime.now(),
    );
  }

  @override
  Future<List<Member>> getMembers({MemberStatus? status, MemberRole? role, String? search}) async => [];
  @override
  Future<Member> getMemberById(String id) async => throw UnimplementedError();
  @override
  Future<Member> updateMember({required String id, required String name, required String phone, String? email, required MemberRole role}) async => throw UnimplementedError();
  @override
  Future<Member> deactivateMember(String id) async => throw UnimplementedError();
  @override
  Future<Member> reactivateMember(String id) async => throw UnimplementedError();
}

void main() {
  test('MemberFormController submits and updates state', () async {
    final repo = FakeMemberRepository();
    final createUseCase = CreateMember(repo);
    final controller = MemberFormController(createMemberUseCase: createUseCase);

    controller.nameController.text = 'Ana Silva';
    controller.phoneController.text = '11988887777';
    controller.selectedRole = MemberRole.leader;

    final success = await controller.submit();
    expect(success, isTrue);
    expect(controller.errorMessage, isNull);
  });
}
