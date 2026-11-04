import 'package:flutter_test/flutter_test.dart';
import 'package:gd_manager/domain/entities/member.dart';
import 'package:gd_manager/domain/enums/member_enums.dart';
import 'package:gd_manager/domain/repositories/member_repository.dart';
import 'package:gd_manager/domain/use_cases/get_members.dart';
import 'package:gd_manager/presentation/controllers/member_list_controller.dart';

class StubListMemberRepository implements MemberRepository {
  final List<Member> list = [
    Member(
      id: '1',
      name: 'Eduardo Lima',
      phone: '11933334444',
      role: MemberRole.leader,
      status: MemberStatus.active,
      initials: 'EL',
      createdAt: DateTime.now(),
      updatedAt: DateTime.now(),
    ),
  ];

  @override
  Future<List<Member>> getMembers({MemberStatus? status, MemberRole? role, String? search}) async {
    return list;
  }

  @override
  Future<Member> createMember({required String name, required String phone, String? email, required MemberRole role}) async => throw UnimplementedError();
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
  test('MemberListController loads members and updates list', () async {
    final repo = StubListMemberRepository();
    final getMembersUseCase = GetMembers(repo);
    final controller = MemberListController(getMembersUseCase: getMembersUseCase);

    await controller.loadMembers();

    expect(controller.isLoading, isFalse);
    expect(controller.members.length, 1);
    expect(controller.members.first.name, 'Eduardo Lima');
  });
}
