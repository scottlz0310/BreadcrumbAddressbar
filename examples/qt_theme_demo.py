#!/usr/bin/env python3
"""
Qt Theme Manager Demo for Breadcrumb Address Bar

Demonstrates integration with qt-theme-manager:
- Theme switching
- Automatic theme detection
- Consistent styling
"""

import sys
import os
import logging
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
    QWidget, QLabel, QPushButton, QComboBox
)

from breadcrumb_addressbar import BreadcrumbAddressBar, get_theme_manager
from breadcrumb_addressbar.logger_setup import setup_logger


class QtThemeDemoWindow(QMainWindow):
    """Demo window for qt-theme-manager integration."""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Breadcrumb Address Bar - Qt Theme Manager Demo")
        self.setGeometry(100, 100, 1000, 500)
        
        # ロガーをセットアップ（デバッグログを有効化）
        self.logger = setup_logger(level=logging.DEBUG)
        
        # メインウィジェット
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # タイトル
        title_label = QLabel("Qt Theme Manager 統合デモ")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title_label)
        
        # パンくずリスト型アドレスバー
        self.addressbar = BreadcrumbAddressBar()
        self.addressbar.pathChanged.connect(self.on_path_changed)
        self.addressbar.folderSelected.connect(self.on_folder_selected)
        layout.addWidget(self.addressbar)
        
        # コントロールパネル
        controls_layout = QHBoxLayout()
        
        # テーマ選択
        theme_label = QLabel("テーマ:")
        controls_layout.addWidget(theme_label)
        
        self.theme_combo = QComboBox()
        self.theme_combo.currentTextChanged.connect(self.on_theme_changed)
        controls_layout.addWidget(self.theme_combo)
        
        # セパレーター設定
        separator_label = QLabel("セパレーター:")
        controls_layout.addWidget(separator_label)
        
        self.separator_combo = QComboBox()
        self.separator_combo.addItems(["なし", " > ", " / ", " \\ "])
        self.separator_combo.currentTextChanged.connect(self.on_separator_changed)
        controls_layout.addWidget(self.separator_combo)
        
        # ボタンサイズ
        size_label = QLabel("ボタンサイズ:")
        controls_layout.addWidget(size_label)
        
        self.size_combo = QComboBox()
        self.size_combo.addItems(["28px", "32px", "36px", "40px"])
        self.size_combo.setCurrentText("32px")
        self.size_combo.currentTextChanged.connect(self.on_size_changed)
        controls_layout.addWidget(self.size_combo)
        
        controls_layout.addStretch()
        layout.addLayout(controls_layout)
        
        # テーマ情報表示
        info_layout = QHBoxLayout()
        
        # 利用可能なテーマ
        self.themes_label = QLabel("利用可能なテーマ: 読み込み中...")
        self.themes_label.setStyleSheet("background: #f0f0f0; padding: 10px; border-radius: 5px;")
        info_layout.addWidget(self.themes_label)
        
        # 現在のテーマ
        self.current_theme_label = QLabel("現在のテーマ: 読み込み中...")
        self.current_theme_label.setStyleSheet("background: #e0f0ff; padding: 10px; border-radius: 5px;")
        info_layout.addWidget(self.current_theme_label)
        
        layout.addLayout(info_layout)
        
        # ログ表示エリア
        self.log_label = QLabel("ログ: 操作を開始してください")
        self.log_label.setStyleSheet("background: #f8f8f8; padding: 10px; border: 1px solid #ccc;")
        self.log_label.setWordWrap(True)
        layout.addWidget(self.log_label)
        
        # 初期パスを設定
        initial_path = os.path.expanduser("~/Documents")
        if not os.path.exists(initial_path):
            initial_path = os.path.expanduser("~")
        self.addressbar.setPath(initial_path)
        
        # テーママネージャーを初期化
        self.setup_theme_manager()
        
        # 初期テーマをメインウィンドウに適用
        if hasattr(self, 'theme_combo') and self.theme_combo.currentText():
            self.apply_theme_to_window(self.theme_combo.currentText())
        
        self.logger.info("Qt Theme Manager Demo を開始しました")
    
    def setup_theme_manager(self):
        """テーママネージャーをセットアップ"""
        try:
            theme_manager = get_theme_manager()
            available_themes = theme_manager.get_available_themes()
            current_theme = theme_manager.get_current_theme_name()
            
            # テーマ選択コンボボックスを更新
            self.theme_combo.clear()
            self.theme_combo.addItems(list(available_themes.keys()))
            self.theme_combo.setCurrentText(current_theme)
            
            # ラベルを更新
            self.themes_label.setText(f"利用可能なテーマ: {', '.join(available_themes.keys())}")
            self.current_theme_label.setText(f"現在のテーマ: {current_theme}")
            
            self.logger.info(f"利用可能なテーマ: {list(available_themes.keys())}")
            self.logger.info(f"現在のテーマ: {current_theme}")
            
        except Exception as e:
            self.logger.error(f"テーママネージャーの初期化に失敗: {e}")
            self.themes_label.setText("利用可能なテーマ: エラー")
            self.current_theme_label.setText("現在のテーマ: エラー")
    
    def on_path_changed(self, path: str) -> None:
        """パス変更時の処理"""
        self.logger.info(f"パス変更: {path}")
        self.log_label.setText(f"ログ: パスが変更されました → {path}")
    
    def on_folder_selected(self, path: str) -> None:
        """フォルダ選択時の処理"""
        self.logger.info(f"フォルダ選択: {path}")
        self.log_label.setText(f"ログ: フォルダが選択されました → {path}")
    
    def on_theme_changed(self, theme: str) -> None:
        """テーマ変更時の処理"""
        try:
            theme_manager = get_theme_manager()
            success = theme_manager.set_theme(theme)
            
            if success:
                self.logger.info(f"テーマ変更: {theme}")
                self.current_theme_label.setText(f"現在のテーマ: {theme}")
                self.log_label.setText(f"ログ: テーマが変更されました → {theme}")
                
                # パンくずリストのテーマを更新
                self.addressbar.refresh_theme()
                
                # メインウィンドウにもテーマを適用
                self.apply_theme_to_window(theme)
                
                # コンボボックスのドロップダウンを閉じる
                self.theme_combo.hidePopup()
                
            else:
                self.logger.error(f"テーマ変更に失敗: {theme}")
                self.log_label.setText(f"ログ: テーマ変更に失敗しました → {theme}")
                
        except Exception as e:
            self.logger.error(f"テーマ変更エラー: {e}")
            self.log_label.setText(f"ログ: テーマ変更エラー → {e}")
    
    def apply_theme_to_window(self, theme_name: str) -> None:
        """メインウィンドウにテーマを適用"""
        try:
            from theme_manager import apply_theme_to_widget
            
            # メインウィンドウにテーマを適用
            apply_theme_to_widget(self, theme_name)
            self.logger.info(f"メインウィンドウにテーマ '{theme_name}' を適用しました")
            
        except Exception as e:
            self.logger.error(f"メインウィンドウのテーマ適用に失敗: {e}")
    
    def on_separator_changed(self, separator: str) -> None:
        """セパレーター変更時の処理"""
        self.logger.info(f"セパレーター変更: {separator}")
        self.addressbar.setSeparator(separator)
        self.log_label.setText(f"ログ: セパレーターが変更されました → '{separator}'")
        
        # コンボボックスのドロップダウンを閉じる
        self.separator_combo.hidePopup()
    
    def on_size_changed(self, size: str) -> None:
        """ボタンサイズ変更時の処理"""
        height = int(size.replace("px", ""))
        self.logger.info(f"ボタンサイズ変更: {height}px")
        self.addressbar.setButtonHeight(height)
        self.log_label.setText(f"ログ: ボタンサイズが変更されました → {height}px")
        
        # コンボボックスのドロップダウンを閉じる
        self.size_combo.hidePopup()


def main():
    """メイン関数"""
    app = QApplication(sys.argv)
    
    # アプリケーション情報
    app.setApplicationName("Breadcrumb Address Bar - Qt Theme Manager Demo")
    app.setApplicationVersion("0.2.0")
    app.setOrganizationName("Your Organization")
    
    # ウィンドウを作成して表示
    window = QtThemeDemoWindow()
    window.show()
    
    # アプリケーション全体にテーマを適用
    try:
        from theme_manager import apply_theme_to_widget
        apply_theme_to_widget(app, "dark")  # デフォルトでダークテーマを適用
        print("アプリケーション全体にテーマを適用しました")
    except Exception as e:
        print(f"アプリケーションテーマの適用に失敗: {e}")
    
    # イベントループ開始
    sys.exit(app.exec())


if __name__ == "__main__":
    main() 