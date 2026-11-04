import 'package:flutter/material.dart';
import '../../domain/entities/member.dart';
import '../../domain/enums/member_enums.dart';
import '../../domain/use_cases/create_member.dart';
import '../../domain/use_cases/update_member.dart';

class MemberFormController extends ChangeNotifier {
  final CreateMember createMemberUseCase;
  final UpdateMember? updateMemberUseCase;
  final Member? editingMember;

  final TextEditingController nameController = TextEditingController();
  final TextEditingController phoneController = TextEditingController();
  final TextEditingController emailController = TextEditingController();
  MemberRole selectedRole = MemberRole.normal;
  DateTime? selectedBirthDate;

  bool _isLoading = false;
  String? _errorMessage;
  Member? _savedMember;

  MemberFormController({
    required this.createMemberUseCase,
    this.updateMemberUseCase,
    this.editingMember,
  }) {
    if (editingMember != null) {
      nameController.text = editingMember!.name;
      phoneController.text = editingMember!.phone;
      emailController.text = editingMember!.email ?? '';
      selectedRole = editingMember!.role;
      selectedBirthDate = editingMember!.birthDate;
    }
  }

  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;
  Member? get savedMember => _savedMember;
  bool get isEditing => editingMember != null;

  String? get formattedBirthDate {
    if (selectedBirthDate == null) return null;
    final day = selectedBirthDate!.day.toString().padLeft(2, '0');
    final month = selectedBirthDate!.month.toString().padLeft(2, '0');
    final year = selectedBirthDate!.year.toString().padLeft(4, '0');
    return '$day/$month/$year';
  }

  void setRole(MemberRole role) {
    selectedRole = role;
    notifyListeners();
  }

  void setBirthDate(DateTime date) {
    selectedBirthDate = date;
    notifyListeners();
  }

  Future<bool> submit() async {
    final name = nameController.text.trim();
    final phone = phoneController.text.trim();
    final email = emailController.text.trim().isEmpty ? null : emailController.text.trim();

    if (name.length < 3) {
      _errorMessage = 'O nome deve ter no mínimo 3 caracteres.';
      notifyListeners();
      return false;
    }

    if (phone.isEmpty) {
      _errorMessage = 'Telefone de contato é obrigatório.';
      notifyListeners();
      return false;
    }

    if (selectedBirthDate == null) {
      _errorMessage = 'Data de nascimento é obrigatória.';
      notifyListeners();
      return false;
    }

    final today = DateTime.now();
    if (selectedBirthDate!.isAfter(today)) {
      _errorMessage = 'Data de nascimento não pode ser no futuro.';
      notifyListeners();
      return false;
    }

    if (selectedBirthDate!.year < 1900) {
      _errorMessage = 'Ano de nascimento deve ser a partir de 1900.';
      notifyListeners();
      return false;
    }

    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    try {
      if (isEditing) {
        if (updateMemberUseCase == null) throw Exception('UpdateMemberUseCase não configurado.');
        _savedMember = await updateMemberUseCase!(
          id: editingMember!.id,
          name: name,
          phone: phone,
          email: email,
          role: selectedRole,
          birthDate: selectedBirthDate!,
        );
      } else {
        _savedMember = await createMemberUseCase(
          name: name,
          phone: phone,
          email: email,
          role: selectedRole,
          birthDate: selectedBirthDate!,
        );
      }
      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _isLoading = false;
      _errorMessage = e.toString().replaceAll('Exception:', '').trim();
      notifyListeners();
      return false;
    }
  }

  @override
  void dispose() {
    nameController.dispose();
    phoneController.dispose();
    emailController.dispose();
    super.dispose();
  }
}
