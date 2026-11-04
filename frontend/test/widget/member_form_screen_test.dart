import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:gd_manager/domain/entities/member.dart';
import 'package:gd_manager/domain/enums/member_enums.dart';
import 'package:gd_manager/domain/repositories/member_repository.dart';
import 'package:gd_manager/domain/use_cases/create_member.dart';
import 'package:gd_manager/presentation/controllers/member_form_controller.dart';
import 'package:gd_manager/presentation/screens/member_form_screen.dart';

class StubMemberRepository implements MemberRepository {
  @override
  Future<Member> createMember({
    required String name,
    required String phone,
    String? email,
    required MemberRole role,
    required DateTime birthDate,
  }) async {
    return Member(
      id: 'stub-id',
      name: name,
      phone: phone,
      email: email,
      role: role,
      status: MemberStatus.active,
      initials: 'MS',
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
  testWidgets('MemberFormScreen renders form fields and save button', (WidgetTester tester) async {
    final repo = StubMemberRepository();
    final createUseCase = CreateMember(repo);
    final controller = MemberFormController(createMemberUseCase: createUseCase);

    await tester.pumpWidget(
      MaterialApp(
        home: MemberFormScreen(controller: controller),
      ),
    );

    expect(find.text('Cadastro de Membro'), findsOneWidget);
    expect(find.byType(TextFormField), findsNWidgets(3)); // Nome, Telefone, Email
    expect(find.textContaining('Data de Nascimento'), findsWidgets);
    expect(find.text('Salvar Membro'), findsOneWidget);
  });
}
