import json
from pathlib import Path
import re
import struct
import unittest

ROOT = Path(__file__).resolve().parents[1]
PACKAGE = json.loads((ROOT / 'package.json').read_text(encoding='utf8'))
THEME = json.loads((ROOT / PACKAGE['contributes']['themes'][0]['path']).read_text(encoding='utf8'))
PALETTE = json.loads((ROOT / 'palette.json').read_text(encoding='utf8'))


class ThemeTests(unittest.TestCase):
    def test_identity_and_no_extension_runtime(self):
        self.assertEqual(PACKAGE['displayName'], 'Italian Pizza')
        self.assertEqual(PACKAGE['contributes']['themes'][0]['uiTheme'], 'vs-dark')
        self.assertNotIn('main', PACKAGE)
        self.assertNotIn('activationEvents', PACKAGE)
        self.assertNotIn('configurationDefaults', PACKAGE['contributes'])

    def test_every_color_is_valid(self):
        colors = list(THEME['colors'].values()) + list(THEME['semanticTokenColors'].values())
        colors += [rule['settings']['foreground'] for rule in THEME['tokenColors']]
        for color in colors:
            self.assertRegex(color, r'^#[0-9A-Fa-f]{6}([0-9A-Fa-f]{2})?$')

    def test_reference_backgrounds(self):
        self.assertEqual(THEME['colors']['editor.background'], '#1A1C1F')
        self.assertEqual(THEME['colors']['sideBar.background'], '#202227')
        self.assertEqual(THEME['colors']['editor.lineHighlightBackground'], '#272930')

    def test_all_bracket_pairs_keep_reference_purple(self):
        for level in range(1, 7):
            self.assertEqual(THEME['colors'][f'editorBracketHighlight.foreground{level}'], PALETTE['bracket'])

    def test_native_and_user_methods_are_distinct(self):
        self.assertEqual(THEME['semanticTokenColors']['method'], PALETTE['control'])
        self.assertEqual(THEME['semanticTokenColors']['method.defaultLibrary'], PALETTE['builtin'])
        self.assertEqual(THEME['semanticTokenColors']['property'], PALETTE['control'])

    def test_luau_header_scope_preserves_body_control_flow(self):
        rules = {scope: rule['settings'] for rule in THEME['tokenColors'] for scope in rule['scope']}
        self.assertEqual(rules['meta.function.luau keyword.control.luau']['foreground'], PALETTE['declaration'])
        self.assertEqual(rules['keyword.control']['foreground'], PALETTE['control'])
        self.assertEqual(rules['comment']['fontStyle'], '')

    def test_pizza_icon_and_preview(self):
        for path in [PACKAGE['icon'], 'images/preview.png']:
            data = (ROOT / path).read_bytes()
            self.assertEqual(data[:8], b'\x89PNG\r\n\x1a\n')
            width, height = struct.unpack('>II', data[16:24])
            self.assertGreaterEqual(width, 256)
            self.assertGreaterEqual(height, 256)


if __name__ == '__main__':
    unittest.main(verbosity=2)
