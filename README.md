# dictat

> Windows向け音声文字起こしアプリ。グローバルホットキーで録音を開始・停止し、文字起こし結果をアクティブウィンドウに直接入力します。

[![Test](https://github.com/YOUR_USERNAME/dictat/actions/workflows/test.yml/badge.svg)](https://github.com/YOUR_USERNAME/dictat/actions/workflows/test.yml)
![Python](https://img.shields.io/badge/python-3.13%2B-blue)
![Platform](https://img.shields.io/badge/platform-Windows-blue)
![License](https://img.shields.io/badge/license-MIT-green)

---

## 概要

**dictat** は macOS の [superwhisper](https://superwhisper.com) にインスパイアされた Windows 向け音声文字起こしツールです。

- ホットキーを押すだけで **どのアプリでも** 音声入力できます
- **3 種類の文字起こしエンジン**（ローカル Whisper・Whisper API・ElevenLabs Scribe）に対応
- **GPT / Gemini** によるテンプレート整形機能付き
- API キーは **Windows Credential Manager** に安全に保存
- システムトレイに常駐し、低フットプリントで動作

---

## 動作イメージ

```
[Ctrl+Shift+R 押す]  → 🔴 録音開始（トレイアイコンが赤くなる）
[Ctrl+Shift+R 押す]  → ⏳ 文字起こし & 整形
                      → ✅ アクティブウィンドウにテキストを直接入力
```

---

## 必要要件

- Windows 10 / 11
- Python 3.13 以上
- [uv](https://docs.astral.sh/uv/) パッケージマネージャー

---

## インストール

```bash
git clone https://github.com/YOUR_USERNAME/dictat.git
cd dictat
uv sync
```

### ローカル Whisper を使う場合

初回起動時にモデルが自動ダウンロードされます（`base` モデル: 約 150 MB）。

---

## 起動

```bash
uv run python -m dictat
```

起動するとシステムトレイに緑のアイコンが表示されます。右クリックで設定ダイアログを開けます。

---

## 設定

トレイアイコンを右クリック → **設定** から変更できます。

### APIキー / エンジン

| 項目 | 説明 |
|------|------|
| エンジン | `Whisper（ローカル）` / `Whisper API` / `ElevenLabs Scribe` |
| Whisperモデル | `tiny` / `base` / `small` / `medium` / `large` / `turbo` |
| 言語 | `日本語` / `English` / 自動検出 |
| OpenAI APIキー | Whisper API・GPT整形で使用 |
| ElevenLabs APIキー | Scribe で使用 |
| Gemini APIキー | Gemini 整形で使用 |

### ホットキー

修飾キー（Ctrl / Shift / Alt）と任意の1文字を組み合わせて最大3キーまで設定できます。

デフォルト: `Ctrl + Shift + R`

### テンプレート整形

整形エンジンを選択し、`{text}` を含むプロンプトを自由に記述できます。

```
整形なし（verbatim）: 文字起こし結果をそのまま入力
OpenAI GPT:          プロンプトで整形してから入力
Google Gemini:       同上
```

テンプレート例:

```
以下の音声文字起こしを箇条書きに整形してください:

{text}
```

---

## データ保存先

| 種別 | 場所 |
|------|------|
| 設定ファイル | `%APPDATA%\dictat\config.json` |
| APIキー | Windows Credential Manager（`dictat` サービス名） |

---

## プロジェクト構成

```
dictat/
├── .github/
│   └── workflows/
│       └── test.yml          # GitHub Actions CI
├── src/
│   └── dictat/
│       ├── app.py            # メインアプリ（Qt + スレッド統合）
│       ├── audio/
│       │   └── recorder.py   # sounddevice 録音・WAV変換
│       ├── transcription/
│       │   ├── base.py       # AbstractTranscriber
│       │   ├── whisper_local.py
│       │   ├── whisper_api.py
│       │   └── elevenlabs.py
│       ├── formatting/
│       │   ├── base.py       # AbstractFormatter
│       │   ├── verbatim.py
│       │   ├── openai_fmt.py
│       │   └── gemini_fmt.py
│       ├── hotkey/
│       │   └── manager.py    # pynput グローバルホットキー
│       ├── output/
│       │   └── injector.py   # アクティブウィンドウへのテキスト注入
│       ├── storage/
│       │   ├── config.py     # JSON 設定ファイル
│       │   └── keys.py       # keyring APIキー管理
│       └── ui/
│           ├── tray.py       # システムトレイアイコン
│           └── settings/     # 設定ダイアログ（3タブ）
├── tests/                    # pytest ユニットテスト
├── dictat.spec               # PyInstaller 設定
└── pyproject.toml
```

---

## 技術スタック

| カテゴリ | ライブラリ |
|----------|-----------|
| UI / システムトレイ | [PySide6](https://doc.qt.io/qtforpython-6/) |
| グローバルホットキー | [pynput](https://pynput.readthedocs.io/) |
| 音声キャプチャ | [sounddevice](https://python-sounddevice.readthedocs.io/) + [NumPy](https://numpy.org/) |
| ローカル文字起こし | [openai-whisper](https://github.com/openai/whisper) |
| Whisper API | [openai](https://github.com/openai/openai-python) |
| ElevenLabs Scribe | [elevenlabs](https://github.com/elevenlabs/elevenlabs-python) |
| GPT 整形 | [openai](https://github.com/openai/openai-python) |
| Gemini 整形 | [google-genai](https://github.com/googleapis/python-genai) |
| APIキー保存 | [keyring](https://github.com/jaraco/keyring) |
| パッケージング | [PyInstaller](https://pyinstaller.org/) |
| プロジェクト管理 | [uv](https://docs.astral.sh/uv/) |

---

## 開発

```bash
# 依存インストール（dev含む）
uv sync --all-groups

# テスト実行
uv run pytest

# .exe ビルド
uv run pyinstaller dictat.spec
```

テストは push / PR のたびに GitHub Actions（`windows-latest`）で自動実行されます。

---

## ライセンス

MIT
