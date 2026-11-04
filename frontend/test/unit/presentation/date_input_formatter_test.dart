import 'package:flutter_test/flutter_test.dart';
import 'package:flutter/services.dart';
import 'package:gd_manager/presentation/formatters/date_input_formatter.dart';

void main() {
  group('DateInputFormatter Unit Tests', () {
    late DateInputFormatter formatter;

    setUp(() {
      formatter = DateInputFormatter();
    });

    test('should format single digits without slash', () {
      const oldValue = TextEditingValue.empty;
      const newValue = TextEditingValue(
        text: '1',
        selection: TextSelection.collapsed(offset: 1),
      );

      final result = formatter.formatEditUpdate(oldValue, newValue);
      expect(result.text, equals('1'));
      expect(result.selection.baseOffset, equals(1));
    });

    test('should format two digits without slash', () {
      const oldValue = TextEditingValue(text: '1');
      const newValue = TextEditingValue(
        text: '15',
        selection: TextSelection.collapsed(offset: 2),
      );

      final result = formatter.formatEditUpdate(oldValue, newValue);
      expect(result.text, equals('15'));
      expect(result.selection.baseOffset, equals(2));
    });

    test('should automatically add first slash after day', () {
      const oldValue = TextEditingValue(text: '15');
      const newValue = TextEditingValue(
        text: '150',
        selection: TextSelection.collapsed(offset: 3),
      );

      final result = formatter.formatEditUpdate(oldValue, newValue);
      expect(result.text, equals('15/0'));
      expect(result.selection.baseOffset, equals(4));
    });

    test('should format month and add second slash', () {
      const oldValue = TextEditingValue(text: '15/0');
      const newValue = TextEditingValue(
        text: '15/051',
        selection: TextSelection.collapsed(offset: 6),
      );

      final result = formatter.formatEditUpdate(oldValue, newValue);
      expect(result.text, equals('15/05/1'));
      expect(result.selection.baseOffset, equals(7));
    });

    test('should format full date DD/MM/AAAA and limit to 10 characters', () {
      const oldValue = TextEditingValue.empty;
      const newValue = TextEditingValue(
        text: '150519959999',
        selection: TextSelection.collapsed(offset: 12),
      );

      final result = formatter.formatEditUpdate(oldValue, newValue);
      expect(result.text, equals('15/05/1995'));
      expect(result.selection.baseOffset, equals(10));
    });

    test('should ignore non-numeric characters', () {
      const oldValue = TextEditingValue.empty;
      const newValue = TextEditingValue(
        text: '15-05-1995',
        selection: TextSelection.collapsed(offset: 10),
      );

      final result = formatter.formatEditUpdate(oldValue, newValue);
      expect(result.text, equals('15/05/1995'));
    });
  });
}
