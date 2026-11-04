import 'package:flutter/material.dart';

class DeactivateConfirmationDialog extends StatelessWidget {
  final String memberName;

  const DeactivateConfirmationDialog({
    super.key,
    required this.memberName,
  });

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Row(
        children: [
          Icon(Icons.warning_amber_rounded, color: Colors.red),
          SizedBox(width: 8),
          Text('Inativar Membro'),
        ],
      ),
      content: Text(
        'Tem certeza que deseja inativar o membro "$memberName"?\n\n'
        'O membro deixará de ser exibido na listagem ativa, mas seu histórico será preservado e poderá ser reativado pela liderança.',
        style: const TextStyle(fontSize: 14),
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.of(context).pop(false),
          child: const Text('Cancelar'),
        ),
        ElevatedButton(
          style: ElevatedButton.styleFrom(
            backgroundColor: Colors.red.shade700,
            foregroundColor: Colors.white,
          ),
          onPressed: () => Navigator.of(context).pop(true),
          child: const Text('Sim, Inativar'),
        ),
      ],
    );
  }
}
