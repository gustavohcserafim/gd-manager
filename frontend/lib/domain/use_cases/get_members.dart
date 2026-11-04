import '../entities/member.dart';
import '../enums/member_enums.dart';
import '../repositories/member_repository.dart';

class GetMembers {
  final MemberRepository repository;

  GetMembers(this.repository);

  Future<List<Member>> call({
    MemberStatus? status,
    MemberRole? role,
    String? search,
    int? birthdayMonth,
  }) {
    return repository.getMembers(
      status: status,
      role: role,
      search: search,
      birthdayMonth: birthdayMonth,
    );
  }
}
