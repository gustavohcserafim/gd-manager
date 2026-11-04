import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:gd_manager/presentation/widgets/deactivate_confirmation_dialog.dart';

void main() {
  testWidgets('DeactivateConfirmationDialog shows warning and handles confirmation', (WidgetTester tester) async {
    bool confirmed = false;

    await tester.pumpWidget(
      MaterialApp(
        home: Scaffold(
          body: Builder(
            builder: (context) => ElevatedButton(
              onPressed: () async {
                final result = await showDialog<bool>(
                  context: context,
                  builder: (ctx) => const DeactivateConfirmationDialog(memberName: 'Pedro Alvares'),
                );
                confirmed = result ?? false;
              },
              child: const Text('Abrir Diálogo'),
            ),
          ),
        ),
      ),
    );

    await tester.tap(find.text('Abrir Diálogo'));
    await tester.pumpAndSettle();

    expect(find.text('Inativar Membro'), findsOneWidget);
    expect(find.textContaining('Pedro Alvares'), findsOneWidget);
    expect(find.text('Cancelar'), findsOneWidget);
    expect(find.text('Sim, Inativar'), findsOneWidget);

    await tester.tap(find.text('Sim, Inativar'));
    await tester.pumpAndSettle();

    expect(confirmed, isTrue);
  });
}
