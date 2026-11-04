import 'package:flutter/material.dart';
import '../../domain/enums/member_enums.dart';
import '../controllers/member_form_controller.dart';

class MemberFormScreen extends StatelessWidget {
  final MemberFormController controller;

  const MemberFormScreen({
    super.key,
    required this.controller,
  });

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: controller,
      builder: (context, _) {
        return Scaffold(
          appBar: AppBar(
            title: Text(controller.isEditing ? 'Editar Membro' : 'Cadastro de Membro'),
            backgroundColor: Colors.blueGrey.shade900,
            foregroundColor: Colors.white,
          ),
          body: SingleChildScrollView(
            padding: const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                if (controller.errorMessage != null)
                  Container(
                    margin: const EdgeInsets.only(bottom: 16),
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: Colors.red.shade50,
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(color: Colors.red.shade300),
                    ),
                    child: Row(
                      children: [
                        const Icon(Icons.error_outline, color: Colors.red),
                        const SizedBox(width: 8),
                        Expanded(
                          child: Text(
                            controller.errorMessage!,
                            style: TextStyle(color: Colors.red.shade900, fontSize: 13),
                          ),
                        ),
                      ],
                    ),
                  ),

                TextFormField(
                  controller: controller.nameController,
                  decoration: const InputDecoration(
                    labelText: 'Nome Completo *',
                    hintText: 'Ex: Carlos Eduardo da Silva',
                    prefixIcon: Icon(Icons.person_outline),
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 16),

                TextFormField(
                  controller: controller.phoneController,
                  keyboardType: TextInputType.phone,
                  decoration: const InputDecoration(
                    labelText: 'Telefone / WhatsApp *',
                    hintText: 'Ex: 11987654321',
                    prefixIcon: Icon(Icons.phone_outlined),
                    border: OutlineInputBorder(),
                    helperText: 'Obrigatório e único entre membros ativos.',
                  ),
                ),
                const SizedBox(height: 16),

                InkWell(
                  onTap: () async {
                    final now = DateTime.now();
                    final initial = controller.selectedBirthDate ?? DateTime(2000, 1, 1);
                    final picked = await showDatePicker(
                      context: context,
                      initialDate: initial.isAfter(now) ? now : initial,
                      firstDate: DateTime(1900, 1, 1),
                      lastDate: now,
                      helpText: 'Selecione a data de nascimento',
                      confirmText: 'CONFIRMAR',
                      cancelText: 'CANCELAR',
                    );
                    if (picked != null) {
                      controller.setBirthDate(picked);
                    }
                  },
                  child: InputDecorator(
                    decoration: const InputDecoration(
                      labelText: 'Data de Nascimento *',
                      hintText: 'Selecione a data de nascimento',
                      prefixIcon: Icon(Icons.cake_outlined),
                      suffixIcon: Icon(Icons.calendar_month_outlined),
                      border: OutlineInputBorder(),
                      helperText: 'Obrigatória para cadastro e comemorações.',
                    ),
                    child: Text(
                      controller.formattedBirthDate ?? 'Toque para selecionar',
                      style: TextStyle(
                        fontSize: 16,
                        color: controller.selectedBirthDate != null
                            ? Colors.black87
                            : Colors.grey.shade600,
                      ),
                    ),
                  ),
                ),
                const SizedBox(height: 16),

                TextFormField(
                  controller: controller.emailController,
                  keyboardType: TextInputType.emailAddress,
                  decoration: const InputDecoration(
                    labelText: 'E-mail (opcional)',
                    hintText: 'Ex: carlos@exemplo.com',
                    prefixIcon: Icon(Icons.email_outlined),
                    border: OutlineInputBorder(),
                  ),
                ),
                const SizedBox(height: 20),

                const Text(
                  'Tipo de Membro *',
                  style: TextStyle(fontWeight: FontWeight.bold, fontSize: 14),
                ),
                const SizedBox(height: 8),
                Wrap(
                  spacing: 10,
                  children: MemberRole.values.map((role) {
                    final isSelected = controller.selectedRole == role;
                    return ChoiceChip(
                      label: Text(role.label),
                      selected: isSelected,
                      selectedColor: Colors.blueGrey.shade800,
                      labelStyle: TextStyle(
                        color: isSelected ? Colors.white : Colors.black87,
                        fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                      ),
                      onSelected: (_) => controller.setRole(role),
                    );
                  }).toList(),
                ),
                const SizedBox(height: 32),

                ElevatedButton.icon(
                  onPressed: controller.isLoading
                      ? null
                      : () async {
                          final success = await controller.submit();
                          if (success && context.mounted) {
                            ScaffoldMessenger.of(context).showSnackBar(
                              SnackBar(
                                content: Text(
                                  controller.isEditing
                                      ? 'Membro atualizado com sucesso!'
                                      : 'Membro cadastrado com sucesso!',
                                ),
                                backgroundColor: Colors.green.shade700,
                              ),
                            );
                            Navigator.of(context).pop(controller.savedMember);
                          }
                        },
                  icon: controller.isLoading
                      ? const SizedBox(
                          width: 20,
                          height: 20,
                          child: CircularProgressIndicator(strokeWidth: 2, color: Colors.white),
                        )
                      : const Icon(Icons.check_circle_outline),
                  label: Text(
                    controller.isEditing ? 'Salvar Alterações' : 'Salvar Membro',
                    style: const TextStyle(fontSize: 16),
                  ),
                  style: ElevatedButton.styleFrom(
                    backgroundColor: Colors.blueGrey.shade900,
                    foregroundColor: Colors.white,
                    padding: const EdgeInsets.symmetric(vertical: 16),
                  ),
                ),
              ],
            ),
          ),
        );
      },
    );
  }
}
