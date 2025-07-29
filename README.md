# Breadcrumb Address Bar

PySide6/PyQt6用のパンくずリスト型アドレスバーライブラリです。ファイルマネージャー向けに階層的なナビゲーションを提供します。

## 特徴

- 🚀 **簡単な組み込み**: 既存のQWidgetレイアウトに数行で追加可能
- 🎨 **カスタマイズ可能**: テーマ、サイズ、スタイルを自由に調整
- ⌨️ **キーボード対応**: Tab移動、矢印キー、Enter確定
- 📁 **フォルダ選択**: 最下層ボタンクリックでフォルダ選択ポップアップ
- ⏪ **履歴機能**: 戻る/進むボタン（オプション）
- 🎯 **マルチプラットフォーム**: Windows, macOS, Linux対応

## インストール

```bash
pip install breadcrumb-addressbar
```

**注意**: このライブラリは `qt-theme-manager` に依存しています。テーマ機能を使用する場合は以下もインストールしてください：

```bash
pip install qt-theme-manager
```

## 基本的な使用方法

```python
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from breadcrumb_addressbar import BreadcrumbAddressBar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Breadcrumb Address Bar Demo")
        
        # メインウィジェット
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        
        # パンくずリスト型アドレスバーを追加
        self.addressbar = BreadcrumbAddressBar()
        self.addressbar.pathChanged.connect(self.on_path_changed)
        layout.addWidget(self.addressbar)
        
        # 初期パスを設定
        self.addressbar.setPath("/home/user/documents")
    
    def on_path_changed(self, path):
        print(f"パスが変更されました: {path}")

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
```

## 設定例

```python
# 見た目のカスタマイズ
addressbar.setButtonHeight(40)
addressbar.setFontSize(14)
addressbar.setSeparator(" > ")

# テーマ統合（qt-theme-manager使用）
from breadcrumb_addressbar import get_theme_manager
from theme_manager import ThemeController

theme_manager = get_theme_manager()
theme_controller = ThemeController()

# 利用可能なテーマを確認
available_themes = theme_controller.get_available_themes()
print(f"利用可能なテーマ: {list(available_themes.keys())}")

# テーマを切り替え
theme_controller.set_theme("dark")  # ダークテーマに切り替え

# 機能の有効化
addressbar.enableHistory(True)
addressbar.enableBookmarks(True)
```

## デモ

プロジェクトには複数のデモが含まれています：

### 基本的なデモ
```bash
python examples/basic_example.py
```

### Phase 2機能のデモ（テーマ統合）
```bash
python examples/qt_theme_demo.py
```

### Phase 2機能のデモ（オリジナル）
```bash
python examples/phase2_demo.py
```

## 開発

### セットアップ

```bash
git clone https://github.com/scottlz0310/BreadcrumbAdressbar.git
cd BreadcrumbAdressbar
pip install -e ".[dev]"
```

### テスト実行

```bash
pytest
```

### コードフォーマット

```bash
black .
isort .
```

## 機能一覧

### ✅ Phase 1 (完了)
- 基本的なパンくずリスト表示
- クリックナビゲーション
- 省略表示機能
- 基本スタイリング

### ✅ Phase 2 (完了)
- フォルダ選択ポップアップ
- キーボードナビゲーション
- テーマ対応（qt-theme-manager統合）
- 設定可能なボタンサイズ・フォント

### 🔄 Phase 3 (予定)
- 履歴機能
- 右クリックメニュー
- ドラッグ&ドロップ
- パス直接入力モード

### 🔄 Phase 4 (予定)
- お気に入り機能
- 非同期処理
- パフォーマンス最適化
- 高度なエラーハンドリング

## ライセンス

MIT License - 詳細は [LICENSE](LICENSE) ファイルを参照してください。

## 貢献

プルリクエストやイシューの報告を歓迎します！

### 開発ガイドライン
- コードは `.cursorrules` に従ってください
- 新機能追加時は段階的実装を心がけてください
- テストの追加をお願いします 