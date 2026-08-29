"""Ujian Fasa 2: config.get_api_key / config.valid_key_format."""
import config


def test_valid_key_format_sah():
    assert config.valid_key_format("HADIS_12345678-1234-1234-1234-123456789012") is True


def test_valid_key_format_tidak_sah():
    assert config.valid_key_format("") is False
    assert config.valid_key_format("HADIS_xxxx") is False
    assert config.valid_key_format("FOO_12345678-1234-1234-1234-123456789012") is False
    # 11 aksara pada segmen terakhir (perlu 12)
    assert config.valid_key_format("HADIS_12345678-1234-1234-1234-12345678901") is False


def test_get_api_key_prioriti_env(monkeypatch):
    # Asingkan daripada settings/env-fail sebenar supaya ujian deterministik.
    monkeypatch.setattr(config, "_from_env_file", lambda: "")
    monkeypatch.setattr(config, "_from_settings", lambda: "")
    monkeypatch.setenv("HADIS_API_KEY", "HADIS_12345678-1234-1234-1234-123456789012")
    assert config.get_api_key() == "HADIS_12345678-1234-1234-1234-123456789012"
