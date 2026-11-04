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
    }
  }

  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;
  Member? get savedMember => _savedMember;
  bool get isEditing => editingMember != null;

  void setRole(MemberRole role) {
    selectedRole = role;
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
        );
      } else {
        _savedMember = await createMemberUseCase(
          name: name,
          phone: phone,
          email: email,
          role: selectedRole,
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
