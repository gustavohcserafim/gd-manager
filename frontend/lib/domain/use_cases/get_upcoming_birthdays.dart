import '../entities/member.dart';
import '../repositories/member_repository.dart';

class GetUpcomingBirthdays {
  final MemberRepository repository;

  GetUpcomingBirthdays(this.repository);

  Future<List<Member>> call({int days = 30}) {
    return repository.getUpcomingBirthdays(days: days);
  }
}
