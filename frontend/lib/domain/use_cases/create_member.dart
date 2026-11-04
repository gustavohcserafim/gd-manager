import '../entities/member.dart';
import '../enums/member_enums.dart';
import '../repositories/member_repository.dart';

class CreateMember {
  final MemberRepository repository;

  CreateMember(this.repository);

  Future<Member> call({
    required String name,
    required String phone,
    String? email,
    required MemberRole role,
  }) {
    return repository.createMember(
      name: name,
      phone: phone,
      email: email,
      role: role,
    );
  }
}
