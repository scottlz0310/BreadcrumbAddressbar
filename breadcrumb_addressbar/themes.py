"""
Theme System for Breadcrumb Address Bar

Integrates with qt-theme-manager for consistent theming.
"""

from typing import Optional
from PySide6.QtCore import QObject
from PySide6.QtWidgets import QWidget

# qt-theme-managerのインポート（オプショナル）
try:
    from theme_manager import ThemeController, apply_theme_to_widget
    THEME_MANAGER_AVAILABLE = True
except ImportError:
    THEME_MANAGER_AVAILABLE = False
    ThemeController = None
    apply_theme_to_widget = None

from .logger_setup import get_logger


class ThemeManager(QObject):
    """
    Theme manager for the breadcrumb address bar.
    
    Integrates with qt-theme-manager for consistent theming.
    """
    
    def __init__(self):
        """Initialize the theme manager."""
        super().__init__()
        self._logger = get_logger("breadcrumb_addressbar.themes")
        
        if THEME_MANAGER_AVAILABLE:
            self._theme_controller = ThemeController()
        else:
            self._theme_controller = None
            self._logger.warning("qt-theme-manager is not available")
    
    def apply_theme_to_widget(self, widget: QWidget, 
                            theme_name: Optional[str] = None) -> bool:
        """
        Apply theme to a widget using qt-theme-manager.
        
        Args:
            widget: Widget to apply theme to
            theme_name: Name of theme to apply (uses current theme if None)
            
        Returns:
            True if theme was successfully applied
        """
        if not THEME_MANAGER_AVAILABLE:
            self._logger.warning("qt-theme-manager is not available")
            return False
            
        try:
            return apply_theme_to_widget(widget, theme_name)
        except Exception as e:
            self._logger.error(f"Failed to apply theme: {e}")
            return False
    
    def get_current_theme_name(self) -> str:
        """
        Get the current theme name.
        
        Returns:
            Current theme name
        """
        if not THEME_MANAGER_AVAILABLE or self._theme_controller is None:
            raise RuntimeError("qt-theme-manager is not available")
        return self._theme_controller.get_current_theme_name()
    
    def get_available_themes(self) -> dict:
        """
        Get available themes.
        
        Returns:
            Dictionary of available themes
        """
        if not THEME_MANAGER_AVAILABLE or self._theme_controller is None:
            raise RuntimeError("qt-theme-manager is not available")
        return self._theme_controller.get_available_themes()
    
    def set_theme(self, theme_name: str) -> bool:
        """
        Set the current theme.
        
        Args:
            theme_name: Name of theme to set
            
        Returns:
            True if theme was successfully set
        """
        if not THEME_MANAGER_AVAILABLE or self._theme_controller is None:
            raise RuntimeError("qt-theme-manager is not available")
            
        try:
            self._theme_controller.set_theme(theme_name)
            self._logger.info(f"Theme changed to: {theme_name}")
            return True
        except Exception as e:
            self._logger.error(f"Failed to set theme: {e}")
            return False
    
    def refresh_widget_styles(self, widget) -> None:
        """
        Refresh styles for a widget after theme change.
        
        Args:
            widget: Widget to refresh styles for
        """
        try:
            # ウィジェットに新しいスタイルを適用
            self.apply_theme_to_widget(widget)
            self._logger.debug(f"Refreshed styles for widget: {widget}")
        except Exception as e:
            self._logger.error(f"Failed to refresh widget styles: {e}")
    
    def get_button_stylesheet(self, is_current: bool = False) -> str:
        """
        Get button stylesheet that adapts to the current theme.
        
        Args:
            is_current: Whether this is the current folder button
            
        Returns:
            CSS stylesheet string
        """
        if not THEME_MANAGER_AVAILABLE or self._theme_controller is None:
            raise RuntimeError("qt-theme-manager is not available")
            
        # qt-theme-managerのテーマ情報を取得
        current_theme = self._theme_controller.get_current_theme_name()
        themes = self._theme_controller.get_available_themes()
        
        if current_theme in themes:
            theme_data = themes[current_theme]
            button_data = theme_data.get('button', {})
            
            # デバッグログ
            self._logger.debug(f"Generating stylesheet for theme: {current_theme}, is_current: {is_current}")
            self._logger.debug(f"Theme data keys: {list(theme_data.keys())}")
            self._logger.debug(f"Button data: {button_data}")
            
            # テキスト色の取得を改善
            text_color = theme_data.get('textColor', '#333333')
            if not text_color or text_color == '#333333':
                # フォールバック: テーマのprimaryColorを使用
                text_color = theme_data.get('primaryColor', '#333333')
            
            self._logger.debug(f"Using text color: {text_color}")
            
            if is_current:
                return f"""
                    QPushButton {{
                        background-color: {button_data.get('background', '#0078d4')};
                        color: {button_data.get('text', '#ffffff')};
                        border: 1px solid {button_data.get('border', '#0078d4')};
                        border-radius: 4px;
                        padding: 4px 8px;
                        font-weight: bold;
                    }}
                    QPushButton:hover {{
                        background-color: {button_data.get('hover', '#106ebe')};
                        border-color: {button_data.get('hover', '#106ebe')};
                    }}
                    QPushButton:pressed {{
                        background-color: {button_data.get('pressed', '#005a9e')};
                        border-color: {button_data.get('pressed', '#005a9e')};
                    }}
                """
            else:
                # 非選択ボタン用のより詳細なスタイル
                hover_bg = button_data.get('hover', '#f0f0f0')
                hover_border = button_data.get('border', '#d0d0d0')
                pressed_bg = button_data.get('pressed', '#e0e0e0')
                focus_color = button_data.get('focus', '#0078d4')
                
                self._logger.debug(f"Non-current button colors - text: {text_color}, hover_bg: {hover_bg}")
                
                return f"""
                    QPushButton {{
                        background-color: transparent;
                        color: {text_color};
                        border: 1px solid transparent;
                        border-radius: 4px;
                        padding: 4px 8px;
                        font-weight: normal;
                    }}
                    QPushButton:hover {{
                        background-color: {hover_bg};
                        border-color: {hover_border};
                        color: {text_color};
                    }}
                    QPushButton:pressed {{
                        background-color: {pressed_bg};
                        border-color: {pressed_bg};
                        color: {text_color};
                    }}
                    QPushButton:focus {{
                        border-color: {focus_color};
                        outline: none;
                        color: {text_color};
                    }}
                """
        
        # フォールバック: システムパレットを使用
        if is_current:
            return """
                QPushButton {
                    background-color: palette(highlight);
                    color: palette(highlighted-text);
                    border: 1px solid palette(highlight);
                    border-radius: 4px;
                    padding: 4px 8px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: palette(light);
                    border-color: palette(light);
                }
                QPushButton:pressed {
                    background-color: palette(dark);
                    border-color: palette(dark);
                }
            """
        else:
            return """
                QPushButton {
                    background-color: transparent;
                    color: palette(text);
                    border: 1px solid transparent;
                    border-radius: 4px;
                    padding: 4px 8px;
                }
                QPushButton:hover {
                    background-color: palette(light);
                    border-color: palette(mid);
                }
                QPushButton:pressed {
                    background-color: palette(mid);
                    border-color: palette(dark);
                }
                QPushButton:focus {
                    border-color: palette(highlight);
                    outline: none;
                }
            """
    
    def get_separator_color(self) -> str:
        """
        Get separator color that adapts to the current theme.
        
        Returns:
            Color string
        """
        if not THEME_MANAGER_AVAILABLE or self._theme_controller is None:
            raise RuntimeError("qt-theme-manager is not available")
            
        current_theme = self._theme_controller.get_current_theme_name()
        themes = self._theme_controller.get_available_themes()
        
        if current_theme in themes:
            theme_data = themes[current_theme]
            return theme_data.get('textColor', '#cccccc')
        
        return "palette(mid)"


# グローバルテーママネージャーインスタンス
_theme_manager = ThemeManager()


def get_theme_manager() -> ThemeManager:
    """
    Get the global theme manager instance.
    
    Returns:
        Theme manager instance
    """
    return _theme_manager 