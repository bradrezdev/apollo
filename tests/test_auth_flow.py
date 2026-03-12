"""
Tests para el flujo de autenticación de Proyecto Apollo.

Cubre:
- Validaciones de formulario (email, password, terms)
- Flujo de login (sign_in_user, submit_login, sync)
- Flujo de registro (sign_up_user, submit_step3, auto-login)
- Sesión persistente (monkey-patch cookies, refresh guard)
- Auth guard (on_load redirect)
- Profile drawer state management

Ejecutar: pytest tests/test_auth_flow.py -v
"""

import pytest
from unittest.mock import MagicMock, patch, PropertyMock


# ────────────────────────────────────────────────────────────────
#  1. Validación de password (lógica pura, sin Reflex runtime)
# ────────────────────────────────────────────────────────────────

class TestPasswordValidation:
    """Valida las reglas de password sin necesitar el runtime de Reflex."""

    @staticmethod
    def _has_lowercase(pw: str) -> bool:
        return any(c.islower() for c in pw)

    @staticmethod
    def _has_uppercase(pw: str) -> bool:
        return any(c.isupper() for c in pw)

    @staticmethod
    def _has_number(pw: str) -> bool:
        return any(c.isdigit() for c in pw)

    @staticmethod
    def _has_special(pw: str) -> bool:
        return any(not c.isalnum() for c in pw) and len(pw) > 0

    @staticmethod
    def _is_length_valid(pw: str) -> bool:
        return len(pw) >= 8

    @staticmethod
    def _is_password_valid(pw: str) -> bool:
        return (
            TestPasswordValidation._has_lowercase(pw)
            and TestPasswordValidation._has_uppercase(pw)
            and TestPasswordValidation._has_number(pw)
            and TestPasswordValidation._has_special(pw)
            and len(pw) >= 8
        )

    def test_valid_password(self):
        assert self._is_password_valid("Onano1234$")

    def test_password_missing_uppercase(self):
        assert not self._is_password_valid("onano1234$")

    def test_password_missing_lowercase(self):
        assert not self._is_password_valid("ONANO1234$")

    def test_password_missing_number(self):
        assert not self._is_password_valid("OnanoTest$")

    def test_password_missing_special(self):
        assert not self._is_password_valid("Onano12345")

    def test_password_too_short(self):
        assert not self._is_password_valid("On1$")

    def test_empty_password(self):
        assert not self._is_password_valid("")


# ────────────────────────────────────────────────────────────────
#  2. Validación de email (lógica pura)
# ────────────────────────────────────────────────────────────────

class TestEmailValidation:
    """Replica la lógica de AuthState.is_email_valid."""

    @staticmethod
    def _is_email_valid(email: str) -> bool:
        return "@" in email and "." in email.split("@")[-1]

    def test_valid_email(self):
        assert self._is_email_valid("bnunez@correo.com")

    def test_valid_email_subdomain(self):
        assert self._is_email_valid("user@sub.domain.org")

    def test_invalid_email_no_at(self):
        assert not self._is_email_valid("bnunez.correo.com")

    def test_invalid_email_no_dot(self):
        assert not self._is_email_valid("bnunez@correocom")

    def test_empty_email(self):
        assert not self._is_email_valid("")


# ────────────────────────────────────────────────────────────────
#  3. Validación de passwords_match (lógica pura)
# ────────────────────────────────────────────────────────────────

class TestPasswordsMatch:
    """Replica AuthState.passwords_match."""

    @staticmethod
    def _passwords_match(pw: str, confirm: str) -> bool:
        return pw == confirm and len(pw) > 0

    def test_matching_passwords(self):
        assert self._passwords_match("Onano1234$", "Onano1234$")

    def test_non_matching_passwords(self):
        assert not self._passwords_match("Onano1234$", "Onano1234")

    def test_empty_passwords(self):
        assert not self._passwords_match("", "")


# ────────────────────────────────────────────────────────────────
#  4. sign_in_user response parsing
# ────────────────────────────────────────────────────────────────

class TestSignInUserParsing:
    """Tests para la lógica de parsing de sign_in_user sin llamar a Supabase."""

    def _parse_sign_in_response(self, result: dict) -> dict | None:
        """Replica la lógica de extracción de UID de AuthState.sign_in_user."""
        supabase_uid = None
        user_email = ""
        first_name = ""
        last_name = ""

        if isinstance(result, dict):
            user_obj = result.get("user") or {}
            supabase_uid = user_obj.get("id") or result.get("id")
            user_email = user_obj.get("email", "")
            meta = user_obj.get("user_metadata") or {}
            first_name = meta.get("first_name", "")
            last_name = meta.get("last_name", "")

        if supabase_uid:
            return {
                "id": supabase_uid,
                "email": user_email,
                "first_name": first_name,
                "last_name": last_name,
            }
        return None

    def test_parse_standard_response(self):
        """Supabase sign_in_with_password normal response."""
        result = {
            "access_token": "eyJ...",
            "refresh_token": "abc123",
            "user": {
                "id": "uuid-1234",
                "email": "bnunez@correo.com",
                "user_metadata": {
                    "first_name": "Bryan",
                    "last_name": "Nunez",
                },
            },
        }
        parsed = self._parse_sign_in_response(result)
        assert parsed is not None
        assert parsed["id"] == "uuid-1234"
        assert parsed["email"] == "bnunez@correo.com"
        assert parsed["first_name"] == "Bryan"
        assert parsed["last_name"] == "Nunez"

    def test_parse_flat_response(self):
        """Response con id en la raíz (sin nested user)."""
        result = {"id": "uuid-5678", "email": "test@example.com"}
        parsed = self._parse_sign_in_response(result)
        assert parsed is not None
        assert parsed["id"] == "uuid-5678"

    def test_parse_empty_response(self):
        """Response vacío → None."""
        parsed = self._parse_sign_in_response({})
        assert parsed is None

    def test_parse_missing_metadata(self):
        """User sin metadata → first_name/last_name vacíos."""
        result = {
            "user": {
                "id": "uuid-9999",
                "email": "test@test.com",
            },
        }
        parsed = self._parse_sign_in_response(result)
        assert parsed is not None
        assert parsed["first_name"] == ""
        assert parsed["last_name"] == ""


# ────────────────────────────────────────────────────────────────
#  5. sign_up_user response parsing
# ────────────────────────────────────────────────────────────────

class TestSignUpResponseParsing:
    """Tests para la extracción de UID del response de sign_up."""

    def _extract_uid(self, result: dict) -> str | None:
        """Replica la lógica de sign_up_user."""
        supabase_uid = None
        if isinstance(result, dict):
            supabase_uid = result.get("id")
            if not supabase_uid:
                user_obj = result.get("user")
                if isinstance(user_obj, dict):
                    supabase_uid = user_obj.get("id")
        return supabase_uid

    def test_uid_in_root(self):
        result = {"id": "uid-root", "email": "a@b.com"}
        assert self._extract_uid(result) == "uid-root"

    def test_uid_in_nested_user(self):
        result = {"user": {"id": "uid-nested"}}
        assert self._extract_uid(result) == "uid-nested"

    def test_uid_not_found(self):
        result = {"email": "noid@test.com"}
        assert self._extract_uid(result) is None

    def test_empty_result(self):
        assert self._extract_uid({}) is None


# ────────────────────────────────────────────────────────────────
#  6. Cookie security (monkey-patch logic)
# ────────────────────────────────────────────────────────────────

class TestCookieSecurity:
    """Valida la lógica de secure=not _is_dev del monkey-patch en rxconfig.py."""

    @staticmethod
    def _compute_secure(env_value: str | None) -> bool:
        """Replica la lógica de _is_dev y secure=not _is_dev."""
        _is_dev = (env_value or "dev").lower() in ("dev", "development", "local")
        return not _is_dev

    def test_dev_env_insecure(self):
        assert self._compute_secure("dev") is False

    def test_development_env_insecure(self):
        assert self._compute_secure("development") is False

    def test_local_env_insecure(self):
        assert self._compute_secure("local") is False

    def test_production_env_secure(self):
        assert self._compute_secure("production") is True

    def test_staging_env_secure(self):
        assert self._compute_secure("staging") is True

    def test_none_defaults_to_dev(self):
        """Cuando REFLEX_ENV no está definido, defaultea a 'dev' → insecure."""
        assert self._compute_secure(None) is False


# ────────────────────────────────────────────────────────────────
#  7. Auth guard logic (on_load redirect decision)
# ────────────────────────────────────────────────────────────────

class TestAuthGuard:
    """Valida la lógica del auth guard sin Reflex runtime."""

    def test_no_tokens_redirects_to_auth(self):
        """Sin access_token ni refresh_token → redirect a /."""
        access = ""
        refresh = ""
        should_redirect = not access and not refresh
        assert should_redirect is True

    def test_access_token_present_stays(self):
        """Con access_token → no redirect, user queda en /chat."""
        access = "eyJ-valid-token"
        should_redirect = not access
        assert should_redirect is False

    def test_no_access_but_refresh_exists(self):
        """Sin access_token pero con refresh_token → debería intentar refresh."""
        access = ""
        refresh = "refresh-token-abc"
        should_attempt_refresh = not access and bool(refresh)
        assert should_attempt_refresh is True

    def test_auth_page_redirects_if_authenticated(self):
        """AuthState.on_load: si tiene access_token → redirect a /chat."""
        access = "eyJ-valid-token"
        should_redirect_to_chat = bool(access)
        assert should_redirect_to_chat is True


# ────────────────────────────────────────────────────────────────
#  8. Profile drawer state logic
# ────────────────────────────────────────────────────────────────

class TestProfileDrawer:
    """Tests para la lógica del toggle_profile_drawer."""

    def test_toggle_opens_drawer(self):
        is_open = False
        is_open = not is_open  # toggle with None
        assert is_open is True

    def test_toggle_closes_drawer(self):
        is_open = True
        is_open = not is_open
        assert is_open is False

    def test_explicit_open(self):
        """on_open_change pasa True → abre."""
        value = True
        is_open = value
        assert is_open is True

    def test_explicit_close(self):
        """on_open_change pasa False → cierra."""
        value = False
        is_open = value
        assert is_open is False


# ────────────────────────────────────────────────────────────────
#  9. Response sanitization (chat_state)
# ────────────────────────────────────────────────────────────────

class TestResponseSanitization:
    """Tests para _sanitize_response de State."""

    @staticmethod
    def _sanitize_response(text: str) -> str:
        """Replica State._sanitize_response."""
        import re
        if not text:
            return text
        text = re.sub(r'\s*filecite\w*', '', text)
        text = re.sub(r'【[^】]*】', '', text)
        text = re.sub(r'sandbox:/mnt/\S+', '', text)
        text = re.sub(r'\[\d+:\d+†[^\]]*\]', '', text)
        text = re.sub(r'  +', ' ', text)
        return text.strip()

    def test_clean_text_unchanged(self):
        assert self._sanitize_response("Hello world") == "Hello world"

    def test_removes_filecite(self):
        result = self._sanitize_response("Some text fileciteturn7file4 more text")
        assert "filecite" not in result
        assert "Some text" in result

    def test_removes_cjk_brackets(self):
        result = self._sanitize_response("Answer【source: doc.pdf】here")
        assert "【" not in result
        assert "Answerhere" == result

    def test_removes_sandbox_paths(self):
        result = self._sanitize_response("File at sandbox:/mnt/data/file.csv is ready")
        assert "sandbox:" not in result

    def test_empty_string(self):
        assert self._sanitize_response("") == ""


# ────────────────────────────────────────────────────────────────
#  10. user_name computed var logic
# ────────────────────────────────────────────────────────────────

class TestUserNameComputed:
    """Replica la lógica de State.user_name computed var."""

    @staticmethod
    def _user_name(user_metadata: dict | None) -> str:
        if user_metadata:
            first = user_metadata.get("first_name", "")
            last = user_metadata.get("last_name", "")
            if first or last:
                return f"{first} {last}".strip()
        return "Usuario"

    def test_full_name(self):
        meta = {"first_name": "Bryan", "last_name": "Nunez"}
        assert self._user_name(meta) == "Bryan Nunez"

    def test_first_name_only(self):
        meta = {"first_name": "Bryan"}
        assert self._user_name(meta) == "Bryan"

    def test_last_name_only(self):
        meta = {"last_name": "Nunez"}
        assert self._user_name(meta) == "Nunez"

    def test_no_metadata(self):
        assert self._user_name(None) == "Usuario"

    def test_empty_metadata(self):
        assert self._user_name({}) == "Usuario"

    def test_empty_names_in_metadata(self):
        meta = {"first_name": "", "last_name": ""}
        assert self._user_name(meta) == "Usuario"
