import 'dart:convert';
import 'package:http/http.dart' as http;
import '../../core/errors/failures.dart';
import '../../domain/enums/member_enums.dart';

class ApiClient {
  final http.Client client;
  final String baseUrl;
  MemberRole currentRole;

  ApiClient({
    http.Client? client,
    this.baseUrl = 'http://localhost:8000/api/v1',
    this.currentRole = MemberRole.leader,
  }) : client = client ?? http.Client();

  void updateRole(MemberRole newRole) {
    currentRole = newRole;
  }

  Map<String, String> get _headers => {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'X-User-Role': currentRole.value,
      };

  Future<dynamic> get(String path, {Map<String, String>? queryParams}) async {
    try {
      final uri = Uri.parse('$baseUrl$path').replace(queryParameters: queryParams);
      final response = await client.get(uri, headers: _headers);
      return _processResponse(response);
    } on Failure {
      rethrow;
    } catch (e) {
      throw const NetworkFailure();
    }
  }

  Future<dynamic> post(String path, Map<String, dynamic> body) async {
    try {
      final uri = Uri.parse('$baseUrl$path');
      final response = await client.post(uri, headers: _headers, body: jsonEncode(body));
      return _processResponse(response);
    } on Failure {
      rethrow;
    } catch (e) {
      throw const NetworkFailure();
    }
  }

  Future<dynamic> put(String path, Map<String, dynamic> body) async {
    try {
      final uri = Uri.parse('$baseUrl$path');
      final response = await client.put(uri, headers: _headers, body: jsonEncode(body));
      return _processResponse(response);
    } on Failure {
      rethrow;
    } catch (e) {
      throw const NetworkFailure();
    }
  }

  Future<dynamic> delete(String path) async {
    try {
      final uri = Uri.parse('$baseUrl$path');
      final response = await client.delete(uri, headers: _headers);
      return _processResponse(response);
    } on Failure {
      rethrow;
    } catch (e) {
      throw const NetworkFailure();
    }
  }

  Future<dynamic> patch(String path, [Map<String, dynamic>? body]) async {
    try {
      final uri = Uri.parse('$baseUrl$path');
      final response = await client.patch(
        uri,
        headers: _headers,
        body: body != null ? jsonEncode(body) : null,
      );
      return _processResponse(response);
    } on Failure {
      rethrow;
    } catch (e) {
      throw const NetworkFailure();
    }
  }

  dynamic _processResponse(http.Response response) {
    final statusCode = response.statusCode;
    if (statusCode >= 200 && statusCode < 300) {
      if (response.body.isEmpty) return null;
      return jsonDecode(utf8.decode(response.bodyBytes));
    }

    String detail = 'Erro na requisição ($statusCode)';
    try {
      final errorJson = jsonDecode(utf8.decode(response.bodyBytes));
      if (errorJson is Map && errorJson.containsKey('detail')) {
        detail = errorJson['detail'].toString();
      }
    } catch (_) {}

    switch (statusCode) {
      case 400:
        throw ValidationFailure(detail);
      case 403:
        throw UnauthorizedFailure(detail);
      case 404:
        throw NotFoundFailure(detail);
      case 409:
        throw DuplicatePhoneFailure(detail);
      default:
        throw ServerFailure(detail);
    }
  }
}
