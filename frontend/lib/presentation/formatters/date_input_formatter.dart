import 'package:flutter/services.dart';

/// Formata a digitação no campo de texto para o padrão brasileiro DD/MM/AAAA,
/// inserindo barras automaticamente e limitando a 10 caracteres.
class DateInputFormatter extends TextInputFormatter {
  @override
  TextEditingValue formatEditUpdate(
    TextEditingValue oldValue,
    TextEditingValue newValue,
  ) {
    // Se estiver apagando, respeita a exclusão
    if (newValue.text.length < oldValue.text.length) {
      return newValue;
    }

    final digitsOnly = newValue.text.replaceAll(RegExp(r'\D'), '');
    final length = digitsOnly.length;

    // Limita a 8 dígitos (DDMMAAAA)
    final trimmedDigits = length > 8 ? digitsOnly.substring(0, 8) : digitsOnly;
    final buffer = StringBuffer();

    for (int i = 0; i < trimmedDigits.length; i++) {
      if (i == 2 || i == 4) {
        buffer.write('/');
      }
      buffer.write(trimmedDigits[i]);
    }

    final formattedText = buffer.toString();
    return TextEditingValue(
      text: formattedText,
      selection: TextSelection.collapsed(offset: formattedText.length),
    );
  }
}
