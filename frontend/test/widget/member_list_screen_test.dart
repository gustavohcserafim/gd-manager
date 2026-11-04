import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:gd_manager/data/datasources/api_client.dart';
import 'package:gd_manager/domain/entities/member.dart';
import 'package:gd_manager/domain/enums/member_enums.dart';
import 'package:gd_manager/domain/repositories/member_repository.dart';
import 'package:gd_manager/domain/use_cases/get_members.dart';
import 'package:gd_manager/presentation/controllers/member_list_controller.dart';
import 'package:gd_manager/presentation/controllers/session_context_controller.dart';
import 'package:gd_manager/presentation/screens/member_list_screen.dart';

class MockListRepository implements MemberRepository {
  @override
  Future<List<Member>> getMembers({MemberStatus? status, MemberRole? role, String? search}) async {
    return [
      Member(
        id: '1',
        name: 'Fernanda Lima',
        phone: '11944445555',
        role: MemberRole.core,
        status: MemberStatus.active,
        initials: 'FL',
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
      )
    ];
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
  testWidgets('MemberListScreen renders search bar, filters and member card', (WidgetTester tester) async {
    final repo = MockListRepository();
    final getMembers = GetMembers(repo);
    final listController = MemberListController(getMembersUseCase: getMembers);
    final sessionController = SessionContextController(apiClient: ApiClient(), initialRole: MemberRole.leader);

    await tester.pumpWidget(
      MaterialApp(
        home: MemberListScreen(
          listController: listController,
          sessionController: sessionController,
        ),
      ),
    );
    await tester.pump();

    expect(find.text('Membros do GD'), findsOneWidget);
    expect(find.byType(TextField), findsOneWidget); // Barra de busca
    expect(find.text('Fernanda Lima'), findsOneWidget);
    expect(find.text('Membro do Núcleo'), findsWidgets);
  });
}
