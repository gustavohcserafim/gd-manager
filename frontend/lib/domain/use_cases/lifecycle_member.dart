import '../entities/member.dart';
import '../repositories/member_repository.dart';

class DeactivateMember {
  final MemberRepository repository;

  DeactivateMember(this.repository);

  Future<Member> call(String id) {
    return repository.deactivateMember(id);
  }
}

class ReactivateMember {
  final MemberRepository repository;

  ReactivateMember(this.repository);

  Future<Member> call(String id) {
    return repository.reactivateMember(id);
  }
}
