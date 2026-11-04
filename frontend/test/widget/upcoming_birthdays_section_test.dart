import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:gd_manager/domain/entities/member.dart';
import 'package:gd_manager/domain/enums/member_enums.dart';
import 'package:gd_manager/presentation/widgets/upcoming_birthdays_section.dart';

void main() {
  group('UpcomingBirthdaysSection Widget Tests', () {
    final now = DateTime.now();
    final m1 = Member(
      id: '1',
      name: 'Carla Dias',
      phone: '11988883333',
      role: MemberRole.core,
      status: MemberStatus.active,
      initials: 'CD',
      birthDate: DateTime(1992, now.month, now.day),
      createdAt: now,
      updatedAt: now,
    );
    final m2 = Member(
      id: '2',
      name: 'Felipe Ramos',
      phone: '11988884444',
      role: MemberRole.normal,
      status: MemberStatus.active,
      initials: 'FR',
      birthDate: DateTime(1995, now.month, now.day + 5 > 28 ? 28 : now.day + 5),
      createdAt: now,
      updatedAt: now,
    );

    testWidgets('renders upcoming birthdays cards and titles', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: UpcomingBirthdaysSection(
              members: [m1, m2],
              onSelectMember: (_) {},
            ),
          ),
        ),
      );

      expect(find.textContaining('Próximos Aniversariantes'), findsOneWidget);
      expect(find.text('Carla Dias'), findsOneWidget);
      expect(find.text('Felipe Ramos'), findsOneWidget);
    });

    testWidgets('renders empty state when there are no upcoming birthdays', (WidgetTester tester) async {
      await tester.pumpWidget(
        MaterialApp(
          home: Scaffold(
            body: UpcomingBirthdaysSection(
              members: const [],
              onSelectMember: (_) {},
            ),
          ),
        ),
      );

      expect(find.textContaining('Nenhum aniversário nos próximos 30 dias'), findsOneWidget);
    });
  });
}
