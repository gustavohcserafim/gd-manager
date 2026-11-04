import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:gd_manager/data/datasources/api_client.dart';
import 'package:gd_manager/domain/entities/member.dart';
import 'package:gd_manager/domain/enums/member_enums.dart';
import 'package:gd_manager/presentation/controllers/session_context_controller.dart';
import 'package:gd_manager/presentation/screens/member_detail_screen.dart';
import 'package:gd_manager/presentation/widgets/member_card.dart';

void main() {
  group('Member Card & Detail Birthday Widget Tests', () {
    testWidgets('MemberCard shows birthday date and indicator', (WidgetTester tester) async {
      final member = Member(
        id: '1',
        name: 'Carlos Santos',
        phone: '11988881111',
        role: MemberRole.normal,
        status: MemberStatus.active,
        initials: 'CS',
        birthDate: DateTime(1995, 5, 15),
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
      );

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: MemberCard(member: member),
          ),
        ),
      );

      expect(find.text('Carlos Santos'), findsOneWidget);
      expect(find.textContaining('15 de Maio'), findsOneWidget);
    });

    testWidgets('MemberCard shows Hoje badge when isBirthdayToday is true', (WidgetTester tester) async {
      final now = DateTime.now();
      final member = Member(
        id: '2',
        name: 'Aniversariante Hoje',
        phone: '11988882222',
        role: MemberRole.core,
        status: MemberStatus.active,
        initials: 'AH',
        birthDate: DateTime(1992, now.month, now.day),
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
      );

      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: MemberCard(member: member),
          ),
        ),
      );

      expect(find.textContaining('Hoje!'), findsOneWidget);
    });

    testWidgets('MemberDetailScreen displays complete birth date and calculated age', (WidgetTester tester) async {
      final sessionController = SessionContextController(apiClient: ApiClient(), initialRole: MemberRole.leader);
      final member = Member(
        id: 'detail-bday',
        name: 'Roberta Dias',
        phone: '11977773333',
        role: MemberRole.leader,
        status: MemberStatus.active,
        initials: 'RD',
        birthDate: DateTime(1990, 8, 20),
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
      );

      await tester.pumpWidget(
        MaterialApp(
          home: MemberDetailScreen(
            member: member,
            sessionController: sessionController,
          ),
        ),
      );

      expect(find.text('Roberta Dias'), findsOneWidget);
      expect(find.textContaining('20/08/1990'), findsOneWidget);
      expect(find.textContaining('anos'), findsOneWidget);
    });

    testWidgets('MemberDetailScreen displays Data não informada for legacy member', (WidgetTester tester) async {
      final sessionController = SessionContextController(apiClient: ApiClient(), initialRole: MemberRole.leader);
      final legacyMember = Member(
        id: 'legacy-bday',
        name: 'Membro Legado',
        phone: '11977774444',
        role: MemberRole.normal,
        status: MemberStatus.active,
        initials: 'ML',
        birthDate: null,
        createdAt: DateTime.now(),
        updatedAt: DateTime.now(),
      );

      await tester.pumpWidget(
        MaterialApp(
          home: MemberDetailScreen(
            member: legacyMember,
            sessionController: sessionController,
          ),
        ),
      );

      expect(find.textContaining('Data não informada'), findsOneWidget);
    });
  });
}
