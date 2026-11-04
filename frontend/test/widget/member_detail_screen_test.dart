import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:gd_manager/data/datasources/api_client.dart';
import 'package:gd_manager/domain/entities/member.dart';
import 'package:gd_manager/domain/enums/member_enums.dart';
import 'package:gd_manager/presentation/controllers/session_context_controller.dart';
import 'package:gd_manager/presentation/screens/member_detail_screen.dart';

void main() {
  final member = Member(
    id: 'detail-id',
    name: 'Karina Ramos',
    phone: '11966667777',
    email: 'karina@teste.com',
    role: MemberRole.core,
    status: MemberStatus.active,
    initials: 'KR',
    createdAt: DateTime.now(),
    updatedAt: DateTime.now(),
  );

  testWidgets('MemberDetailScreen shows edit button for leader', (WidgetTester tester) async {
    final sessionController = SessionContextController(apiClient: ApiClient(), initialRole: MemberRole.leader);

    await tester.pumpWidget(
      MaterialApp(
        home: MemberDetailScreen(
          member: member,
          sessionController: sessionController,
        ),
      ),
    );

    expect(find.text('Karina Ramos'), findsOneWidget);
    expect(find.text('11966667777'), findsOneWidget);
    expect(find.text('Editar'), findsOneWidget);
  });

  testWidgets('MemberDetailScreen hides edit button for normal member', (WidgetTester tester) async {
    final sessionController = SessionContextController(apiClient: ApiClient(), initialRole: MemberRole.normal);

    await tester.pumpWidget(
      MaterialApp(
        home: MemberDetailScreen(
          member: member,
          sessionController: sessionController,
        ),
      ),
    );

    expect(find.text('Karina Ramos'), findsOneWidget);
    expect(find.text('Editar'), findsNothing);
  });
}
