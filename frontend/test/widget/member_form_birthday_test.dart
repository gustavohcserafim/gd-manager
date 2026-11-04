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
  testWidgets('MemberFormScreen renders birth date field and shows error when empty', (WidgetTester tester) async {
    final repo = StubMemberRepository();
    final createUseCase = CreateMember(repo);
    final controller = MemberFormController(createMemberUseCase: createUseCase);

    await tester.pumpWidget(
      MaterialApp(
        home: MemberFormScreen(controller: controller),
      ),
    );

    // Verifica presença do campo de data de nascimento
    expect(find.textContaining('Data de Nascimento'), findsWidgets);

    // Preenche nome e telefone
    await tester.enterText(find.byType(TextFormField).at(0), 'Juliana Lima');
    await tester.enterText(find.byType(TextFormField).at(1), '11988887777');

    // Tenta salvar sem selecionar data de nascimento
    await tester.tap(find.text('Salvar Membro'));
    await tester.pump();

    // Deve exibir mensagem de erro exigindo data de nascimento
    expect(find.textContaining('nascimento'), findsWidgets);
  });

  testWidgets('MemberFormScreen formats typed date with DD/MM/AAAA mask', (WidgetTester tester) async {
    final repo = StubMemberRepository();
    final createUseCase = CreateMember(repo);
    final controller = MemberFormController(createMemberUseCase: createUseCase);

    await tester.pumpWidget(
      MaterialApp(
        home: MemberFormScreen(controller: controller),
      ),
    );

    await tester.enterText(find.byType(TextFormField).at(0), 'Juliana Lima');
    await tester.enterText(find.byType(TextFormField).at(1), '11988887777');
    await tester.enterText(find.byType(TextFormField).at(2), '15051995');
    await tester.pump();

    expect(controller.birthDateController.text, '15/05/1995');
  });
}
