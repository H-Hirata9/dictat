import pytest
from unittest.mock import MagicMock, patch
from dictat.hotkey.manager import _build_combo, HotkeyManager


def test_build_combo_single_modifier_and_key():
    assert _build_combo(["ctrl", "r"]) == "<ctrl>+r"


def test_build_combo_two_modifiers():
    assert _build_combo(["ctrl", "shift", "r"]) == "<ctrl>+<shift>+r"


def test_build_combo_three_modifiers():
    assert _build_combo(["ctrl", "shift", "alt"]) == "<ctrl>+<shift>+<alt>"


def test_build_combo_key_only():
    assert _build_combo(["r"]) == "r"


def test_build_combo_alt_modifier():
    assert _build_combo(["alt", "x"]) == "<alt>+x"


def test_hotkey_manager_starts_listener():
    callback = MagicMock()
    with patch("dictat.hotkey.manager.keyboard.GlobalHotKeys") as MockHotKeys:
        mock_listener = MagicMock()
        MockHotKeys.return_value = mock_listener
        manager = HotkeyManager(keys=["ctrl", "shift", "r"], on_activate=callback)
        manager.start()
        MockHotKeys.assert_called_once_with({"<ctrl>+<shift>+r": callback})
        mock_listener.start.assert_called_once()


def test_hotkey_manager_stop_clears_listener():
    with patch("dictat.hotkey.manager.keyboard.GlobalHotKeys") as MockHotKeys:
        mock_listener = MagicMock()
        MockHotKeys.return_value = mock_listener
        manager = HotkeyManager(keys=["ctrl", "r"], on_activate=MagicMock())
        manager.start()
        manager.stop()
        mock_listener.stop.assert_called_once()
        assert manager._listener is None


def test_hotkey_manager_update_restarts_with_new_keys():
    callback = MagicMock()
    with patch("dictat.hotkey.manager.keyboard.GlobalHotKeys") as MockHotKeys:
        mock_listener = MagicMock()
        MockHotKeys.return_value = mock_listener
        manager = HotkeyManager(keys=["ctrl", "r"], on_activate=callback)
        manager.start()
        manager.update(["ctrl", "shift", "t"])
        assert MockHotKeys.call_count == 2
        last_call = MockHotKeys.call_args_list[-1]
        assert "<ctrl>+<shift>+t" in last_call[0][0]
