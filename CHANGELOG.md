# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.1] - 2025-08-01

### Added
- **CI/CD Pipeline**: 完全なCI/CDパイプラインの構築
  - GitHub Actionsによる自動テスト・リント・ビルド
  - 複数Pythonバージョン（3.8-3.12）でのテスト実行
  - 自動PyPI公開機能
  - GitHub Release自動生成
- **Code Quality Tools**: コード品質向上ツールの統合
  - Black（コードフォーマット）
  - isort（import整理）
  - flake8（リント）
  - mypy（型チェック）
- **Release Automation**: リリース自動化スクリプト
  - `scripts/release.py`による自動リリースプロセス
  - バージョン管理の自動化
  - CHANGELOG.mdの自動更新

### Changed
- **Project Configuration**: プロジェクト設定の統一
  - `pyproject.toml`での一元管理
  - 79文字行長での統一フォーマット
  - 開発依存関係の整理
- **CI Workflow**: CIワークフローの改善
  - テストとlintingの分離
  - 効率的な並列実行
  - 適切な権限設定

### Fixed
- **CI Issues**: CI/CDパイプラインの問題を解決
  - mypyの設定とPySide6型スタブの問題を解決
  - GitHub Actionsの権限設定を修正
  - リリースワークフローの安定化
- **Code Formatting**: コードフォーマットの統一
  - 行の長さを79文字に統一
  - import文の整理
  - 一貫したコーディングスタイル
## [0.2.0] - 2025-07-29

### Added
- **Phase 2 Features**: フォルダ選択ポップアップ機能
  - 最下層ボタンクリックでサブフォルダ一覧表示
  - `FolderSelectionPopup`クラスの実装
  - フォルダ選択時のシグナル発火
- **Theme Integration**: `qt-theme-manager`との統合
  - 動的テーマ切り替え対応
  - ボタンスタイルの自動更新
  - セパレーター色のテーマ追従
- **Enhanced UI**: 改善されたユーザーインターフェース
  - ボタンサイズの動的変更
  - フォントサイズの動的変更
  - セパレーター文字の動的変更
- **Debug Support**: デバッグ機能の強化
  - 詳細なログ出力
  - テーマ変更時のデバッグ情報
  - ポップアップ表示時のデバッグ情報

### Changed
- **Theme System**: 内部テーマ管理から`qt-theme-manager`統合に変更
- **Signal Enhancement**: `BreadcrumbItem`のシグナルを拡張（`clicked_with_info`）
- **API Updates**: テーマ関連のAPIを`qt-theme-manager`に合わせて更新

### Fixed
- **Popup Display**: `QMenu.popup`メソッドの引数エラーを修正
- **Theme Updates**: テーマ変更時のボタン色更新問題を解決
- **Import Issues**: `QAction`のインポートエラーを修正

## [0.1.0] - 2025-07-29

### Added
- **Phase 1 Features**: 基本的なパンくずリスト機能
  - 階層ナビゲーション表示
  - クリックナビゲーション
  - 省略表示機能
  - 基本スタイリング
- **Core Components**: 主要コンポーネントの実装
  - `BreadcrumbAddressBar`: メインウィジェット
  - `BreadcrumbItem`: 個別ボタンコンポーネント
  - `ThemeManager`: テーマ管理システム
- **Project Structure**: プロジェクト基盤の構築
  - 標準的なPythonライブラリ構造
  - テスト環境の構築
  - ドキュメントの整備 