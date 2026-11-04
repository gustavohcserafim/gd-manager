import 'package:flutter/material.dart';
import 'data/datasources/api_client.dart';
import 'data/datasources/member_remote_data_source.dart';
import 'data/repositories/member_repository_impl.dart';
import 'domain/enums/member_enums.dart';
import 'domain/use_cases/create_member.dart';
import 'domain/use_cases/get_members.dart';
import 'domain/use_cases/get_upcoming_birthdays.dart';
import 'domain/use_cases/update_member.dart';
import 'domain/use_cases/lifecycle_member.dart';
import 'presentation/controllers/member_form_controller.dart';
import 'presentation/controllers/member_list_controller.dart';
import 'presentation/controllers/session_context_controller.dart';
import 'presentation/screens/member_detail_screen.dart';
import 'presentation/screens/member_form_screen.dart';
import 'presentation/screens/member_list_screen.dart';
import 'presentation/widgets/deactivate_confirmation_dialog.dart';

void main() {
  runApp(const GDManagerApp());
}

class GDManagerApp extends StatefulWidget {
  const GDManagerApp({super.key});

  @override
  State<GDManagerApp> createState() => _GDManagerAppState();
}

class _GDManagerAppState extends State<GDManagerApp> {
  late final ApiClient apiClient;
  late final SessionContextController sessionController;
  late final MemberRemoteDataSource remoteDataSource;
  late final MemberRepositoryImpl repository;
  late final GetMembers getMembersUseCase;
  late final GetUpcomingBirthdays getUpcomingBirthdaysUseCase;
  late final CreateMember createMemberUseCase;
  late final UpdateMember updateMemberUseCase;
  late final GetMemberById getMemberByIdUseCase;
  late final DeactivateMember deactivateMemberUseCase;
  late final ReactivateMember reactivateMemberUseCase;
  late final MemberListController listController;

  @override
  void initState() {
    super.initState();
    apiClient = ApiClient();
    sessionController = SessionContextController(apiClient: apiClient, initialRole: MemberRole.leader);
    remoteDataSource = MemberRemoteDataSourceImpl(apiClient: apiClient);
    repository = MemberRepositoryImpl(remoteDataSource: remoteDataSource);

    getMembersUseCase = GetMembers(repository);
    getUpcomingBirthdaysUseCase = GetUpcomingBirthdays(repository);
    createMemberUseCase = CreateMember(repository);
    updateMemberUseCase = UpdateMember(repository);
    getMemberByIdUseCase = GetMemberById(repository);
    deactivateMemberUseCase = DeactivateMember(repository);
    reactivateMemberUseCase = ReactivateMember(repository);

    listController = MemberListController(
      getMembersUseCase: getMembersUseCase,
      getUpcomingBirthdaysUseCase: getUpcomingBirthdaysUseCase,
    );
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'GD Manager',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blueGrey),
        useMaterial3: true,
      ),
      home: Builder(
        builder: (context) => MemberListScreen(
          listController: listController,
          sessionController: sessionController,
          onAddMember: () async {
            final formController = MemberFormController(createMemberUseCase: createMemberUseCase);
            await Navigator.of(context).push(
              MaterialPageRoute(builder: (_) => MemberFormScreen(controller: formController)),
            );
            listController.loadMembers();
          },
          onSelectMember: (memberId) async {
            try {
              final member = await getMemberByIdUseCase(memberId);
              if (!context.mounted) return;
              await Navigator.of(context).push(
                MaterialPageRoute(
                  builder: (ctx) => MemberDetailScreen(
                    member: member,
                    sessionController: sessionController,
                    onEdit: () async {
                      final formController = MemberFormController(
                        createMemberUseCase: createMemberUseCase,
                        updateMemberUseCase: updateMemberUseCase,
                        editingMember: member,
                      );
                      final updatedMember = await Navigator.of(ctx).push(
                        MaterialPageRoute(builder: (_) => MemberFormScreen(controller: formController)),
                      );
                      if (updatedMember != null) {
                        if (ctx.mounted) Navigator.of(ctx).pop();
                        listController.loadMembers();
                      }
                    },
                    onDeactivate: () async {
                      final confirmed = await showDialog<bool>(
                        context: ctx,
                        builder: (_) => DeactivateConfirmationDialog(memberName: member.name),
                      );
                      if (confirmed == true) {
                        try {
                          await deactivateMemberUseCase(member.id);
                          if (ctx.mounted) Navigator.of(ctx).pop();
                          listController.loadMembers();
                          if (context.mounted) {
                            ScaffoldMessenger.of(context).showSnackBar(
                              SnackBar(
                                content: Text('Membro "${member.name}" inativado com sucesso.'),
                                backgroundColor: Colors.blueGrey.shade800,
                              ),
                            );
                          }
                        } catch (e) {
                          if (ctx.mounted) {
                            ScaffoldMessenger.of(ctx).showSnackBar(
                              SnackBar(
                                content: Text('Erro ao inativar membro: ${e.toString().replaceAll('Exception:', '').trim()}'),
                                backgroundColor: Colors.red.shade700,
                              ),
                            );
                          }
                        }
                      }
                    },
                    onReactivate: () async {
                      try {
                        await reactivateMemberUseCase(member.id);
                        if (ctx.mounted) Navigator.of(ctx).pop();
                        listController.loadMembers();
                        if (context.mounted) {
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(
                              content: Text('Membro "${member.name}" reativado com sucesso.'),
                              backgroundColor: Colors.green.shade700,
                            ),
                          );
                        }
                      } catch (e) {
                        if (ctx.mounted) {
                          ScaffoldMessenger.of(ctx).showSnackBar(
                            SnackBar(
                              content: Text(e.toString().replaceAll('Exception:', '').trim()),
                              backgroundColor: Colors.red.shade700,
                            ),
                          );
                        }
                      }
                    },
                  ),
                ),
              );
            } catch (e) {
              if (context.mounted) {
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('Erro ao abrir detalhes: $e')),
                );
              }
            }
          },
        ),
      ),
    );
  }
}
