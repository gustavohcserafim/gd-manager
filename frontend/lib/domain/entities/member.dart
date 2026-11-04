import '../enums/member_enums.dart';

class Member {
  final String id;
  final String name;
  final String phone;
  final String? email;
  final MemberRole role;
  final MemberStatus status;
  final String initials;
  final DateTime? birthDate;
  final DateTime createdAt;
  final DateTime updatedAt;

  const Member({
    required this.id,
    required this.name,
    required this.phone,
    this.email,
    required this.role,
    required this.status,
    required this.initials,
    this.birthDate,
    required this.createdAt,
    required this.updatedAt,
  });

  bool get isActive => status == MemberStatus.active;

  int? get age {
    if (birthDate == null) return null;
    final now = DateTime.now();
    int calculatedAge = now.year - birthDate!.year;
    if (now.month < birthDate!.month ||
        (now.month == birthDate!.month && now.day < birthDate!.day)) {
      calculatedAge--;
    }
    return calculatedAge >= 0 ? calculatedAge : 0;
  }

  String? get birthdayDisplay {
    if (birthDate == null) return null;
    const months = [
      'Janeiro', 'Fevereiro', 'Março', 'Abril', 'Maio', 'Junho',
      'Julho', 'Agosto', 'Setembro', 'Outubro', 'Novembro', 'Dezembro'
    ];
    final monthName = months[birthDate!.month - 1];
    return '${birthDate!.day} de $monthName';
  }

  String? get birthDateFormatted {
    if (birthDate == null) return null;
    final day = birthDate!.day.toString().padLeft(2, '0');
    final month = birthDate!.month.toString().padLeft(2, '0');
    final year = birthDate!.year.toString().padLeft(4, '0');
    return '$day/$month/$year';
  }

  bool get isBirthdayToday {
    if (birthDate == null) return false;
    final now = DateTime.now();
    if (birthDate!.month == 2 && birthDate!.day == 29) {
      final isLeapYear = (now.year % 4 == 0 && now.year % 100 != 0) || (now.year % 400 == 0);
      if (!isLeapYear) {
        return now.month == 2 && now.day == 28;
      }
    }
    return now.month == birthDate!.month && now.day == birthDate!.day;
  }

  int? get daysUntilBirthday {
    if (birthDate == null) return null;
    final now = DateTime.now();
    final today = DateTime(now.year, now.month, now.day);

    int targetYear = now.year;
    int targetMonth = birthDate!.month;
    int targetDay = birthDate!.day;

    bool isLeap(int y) => (y % 4 == 0 && y % 100 != 0) || (y % 400 == 0);
    if (targetMonth == 2 && targetDay == 29 && !isLeap(targetYear)) {
      targetDay = 28;
    }

    DateTime nextBday = DateTime(targetYear, targetMonth, targetDay);
    if (nextBday.isBefore(today)) {
      targetYear++;
      targetDay = birthDate!.day;
      if (targetMonth == 2 && targetDay == 29 && !isLeap(targetYear)) {
        targetDay = 28;
      }
      nextBday = DateTime(targetYear, targetMonth, targetDay);
    }

    return nextBday.difference(today).inDays;
  }
}
