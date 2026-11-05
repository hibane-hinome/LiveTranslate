import sqlite3

from history_db import TranslationHistoryDB, to_history_language


def test_short_codes_become_the_tags_the_csharp_history_uses():
    assert to_history_language("zh") == "zh-CN"
    assert to_history_language("ja") == "ja-JP"
    assert to_history_language("ZH") == "zh-CN"


def test_existing_tags_and_unknown_codes_pass_through():
    assert to_history_language("zh-TW") == "zh-TW"
    assert to_history_language("xx") == "xx"
    assert to_history_language("") == ""


def test_log_writes_one_row_with_the_tag_form(tmp_path):
    db = TranslationHistoryDB(str(tmp_path / "history.db"), api_name="LiveTranslate:test")

    db.log("こんにちは", "你好", "zh")
    db.close()

    rows = sqlite3.connect(str(tmp_path / "history.db")).execute(
        "SELECT TargetLanguage, ApiUsed FROM TranslationHistory"
    ).fetchall()
    assert rows == [("zh-CN", "LiveTranslate:test")]


def test_error_placeholder_is_not_history(tmp_path):
    db = TranslationHistoryDB(str(tmp_path / "history.db"), api_name="LiveTranslate:test")

    db.log("こんにちは", "[error: timeout]", "zh")
    db.log("", "你好", "zh")
    db.close()

    count = sqlite3.connect(str(tmp_path / "history.db")).execute(
        "SELECT COUNT(*) FROM TranslationHistory"
    ).fetchone()[0]
    assert count == 0
