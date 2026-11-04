import '../entities/member.dart';
import '../enums/member_enums.dart';
import '../repositories/member_repository.dart';

class UpdateMember {
  final MemberRepository repository;

  UpdateMember(this.repository);

  Future<Member> call({
    required String id,
    required String name,
    required String phone,
    String? email,
    required MemberRole role,
  }) {
    return repository.updateMember(
      id: id,
      name: name,
      phone: phone,
      email: email,
      role: role,
    );
  }
}

class GetMemberById {
  final MemberRepository repository;

  GetMemberById(this.repository);

  Future<Member> call(String id) {
    return repository.getMemberById(id);
  }
}
