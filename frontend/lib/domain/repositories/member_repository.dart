import '../entities/member.dart';
import '../enums/member_enums.dart';

abstract class MemberRepository {
  Future<Member> createMember({
    required String name,
    required String phone,
    String? email,
    required MemberRole role,
  });

  Future<List<Member>> getMembers({
    MemberStatus? status,
    MemberRole? role,
    String? search,
  });

  Future<Member> getMemberById(String id);

  Future<Member> updateMember({
    required String id,
    required String name,
    required String phone,
    String? email,
    required MemberRole role,
  });

  Future<Member> deactivateMember(String id);

  Future<Member> reactivateMember(String id);
}
