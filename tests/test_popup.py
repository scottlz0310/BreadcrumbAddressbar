"""
Test cases for FolderSelectionPopup functionality.
"""

import os
import tempfile
from unittest.mock import MagicMock, patch

import pytest

# Headless 環境でのハング防止（CI向け）
os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")


try:
    from PySide6.QtCore import QPoint
    from PySide6.QtWidgets import QApplication

    PYSIDE6_AVAILABLE = True
except ImportError:
    PYSIDE6_AVAILABLE = False

try:
    from breadcrumb_addressbar.popup import FolderSelectionPopup

    POPUP_AVAILABLE = True
except ImportError:
    POPUP_AVAILABLE = False


@pytest.mark.skipif(
    not PYSIDE6_AVAILABLE or not POPUP_AVAILABLE,
    reason="PySide6 or FolderSelectionPopup not available",
)
class TestFolderSelectionPopup:
    """Test cases for FolderSelectionPopup class."""

    @pytest.fixture(autouse=True)
    def setup(self):
        """Setup test environment."""
        # 既存のQApplicationインスタンスがある場合は削除
        app = QApplication.instance()
        if app is None:
            self.app = QApplication([])
        else:
            self.app = app

        self.popup = FolderSelectionPopup()
        yield
        # テスト終了時のクリーンアップは最小限に

    def test_initial_state(self):
        """Test initial state of the popup."""
        assert self.popup._current_path == ""
        assert self.popup.minimumWidth() == 300
        assert self.popup.maximumHeight() == 400

    def test_setup_ui(self):
        """Test UI setup."""
        # UI設定が正しく適用されているかチェック
        assert self.popup.minimumWidth() == 300
        assert self.popup.maximumHeight() == 400

        # フォント設定をチェック
        font = self.popup.font()
        assert font.pointSize() == 10

    def test_get_folders_existing_path(self, tmp_path):
        """Test getting folders from an existing path."""
        # テスト用のディレクトリ構造を作成
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()

        # サブディレクトリを作成
        (test_dir / "folder1").mkdir()
        (test_dir / "folder2").mkdir()
        (test_dir / "file1.txt").touch()  # ファイルは除外される
        (test_dir / ".hidden").mkdir()  # 隠しフォルダは除外される

        folders = self.popup._get_folders(str(test_dir))

        # フォルダ名を抽出
        folder_names = [folder[0] for folder in folders]

        assert len(folders) == 2
        assert "folder1" in folder_names
        assert "folder2" in folder_names
        assert "file1.txt" not in folder_names
        assert ".hidden" not in folder_names

    def test_get_folders_nonexistent_path(self):
        """Test getting folders from a non-existent path."""
        folders = self.popup._get_folders("/nonexistent/path")
        assert folders == []

    def test_get_folders_file_path(self, tmp_path):
        """Test getting folders when path is a file."""
        # テスト用のファイルを作成
        test_file = tmp_path / "test_file.txt"
        test_file.touch()

        folders = self.popup._get_folders(str(test_file))
        assert folders == []

    def test_get_folders_permission_error(self):
        """Test getting folders with permission error."""
        with patch(
            "os.listdir", side_effect=PermissionError("Permission denied")
        ):
            folders = self.popup._get_folders("/some/path")
            assert folders == []

    def test_get_folders_os_error(self):
        """Test getting folders with OS error."""
        with patch("os.listdir", side_effect=OSError("OS error")):
            folders = self.popup._get_folders("/some/path")
            assert folders == []

    def test_get_folders_general_exception(self):
        """Test getting folders with general exception."""
        with patch("os.listdir", side_effect=Exception("General error")):
            folders = self.popup._get_folders("/some/path")
            assert folders == []

    def test_show_for_path_with_folders(self, tmp_path):
        """Test showing popup with folders."""
        # テスト用のディレクトリ構造を作成
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()
        (test_dir / "folder1").mkdir()
        (test_dir / "folder2").mkdir()

        # シグナルが発信されるかチェック
        signal_emitted = False
        received_path = ""

        def on_folder_selected(path):
            nonlocal signal_emitted, received_path
            signal_emitted = True
            received_path = path

        self.popup.folderSelected.connect(on_folder_selected)

        # ポップアップを表示（実際の表示は行わない）
        with patch.object(self.popup, "popup"):
            self.popup.showForPath(str(test_dir))

        assert self.popup._current_path == str(test_dir)
        assert len(self.popup.actions()) == 2  # 2つのフォルダアクション

    def test_show_for_path_no_folders(self, tmp_path):
        """Test showing popup with no folders."""
        # 空のディレクトリを作成
        test_dir = tmp_path / "empty_dir"
        test_dir.mkdir()

        # ポップアップを表示（実際の表示は行わない）
        with patch.object(self.popup, "popup"):
            self.popup.showForPath(str(test_dir))

        assert self.popup._current_path == str(test_dir)
        assert (
            len(self.popup.actions()) == 1
        )  # "フォルダが見つかりません"アクション

        # アクションが無効化されているかチェック
        action = self.popup.actions()[0]
        assert not action.isEnabled()

    def test_show_for_path_with_position(self, tmp_path):
        """Test showing popup with position."""
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()
        (test_dir / "folder1").mkdir()

        position = (100, 200)

        # ポップアップを表示（実際の表示は行わない）
        with patch.object(self.popup, "popup") as mock_popup:
            self.popup.showForPath(str(test_dir), position)

            # popupメソッドが正しい位置で呼ばれるかチェック
            mock_popup.assert_called_once()
            call_args = mock_popup.call_args[0][0]
            assert isinstance(call_args, QPoint)
            assert call_args.x() == position[0]
            assert call_args.y() == position[1]

    def test_show_for_path_without_position(self, tmp_path):
        """Test showing popup without position."""
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()
        (test_dir / "folder1").mkdir()

        # ポップアップを表示（実際の表示は行わない）
        with patch.object(self.popup, "exec_"):
            self.popup.showForPath(str(test_dir))

            # exec_メソッドが呼ばれるかチェック
            self.popup.exec_.assert_called_once()

    def test_on_folder_selected(self):
        """Test folder selection handler."""
        signal_emitted = False
        received_path = ""

        def on_folder_selected(path):
            nonlocal signal_emitted, received_path
            signal_emitted = True
            received_path = path

        self.popup.folderSelected.connect(on_folder_selected)

        test_path = "/test/path"
        self.popup._on_folder_selected(test_path)

        assert signal_emitted
        assert received_path == test_path

    def test_folder_sorting(self, tmp_path):
        """Test that folders are sorted alphabetically."""
        test_dir = tmp_path / "test_dir"
        test_dir.mkdir()

        # 順序を意図的に逆にして作成
        (test_dir / "zebra").mkdir()
        (test_dir / "alpha").mkdir()
        (test_dir / "beta").mkdir()

        folders = self.popup._get_folders(str(test_dir))
        folder_names = [folder[0] for folder in folders]

        # アルファベット順にソートされているかチェック
        expected_order = ["alpha", "beta", "zebra"]
        assert folder_names == expected_order

    def test_clear_actions(self):
        """Test that actions are cleared before adding new ones."""
        # 最初にアクションを追加
        with patch.object(self.popup, "popup"):
            self.popup.showForPath("/some/path")
            initial_count = len(self.popup.actions())

            # 再度アクションを追加
            self.popup.showForPath("/another/path")
            final_count = len(self.popup.actions())

            # アクションがクリアされているかチェック
            assert final_count <= initial_count + 1  # 新しいアクションのみ
