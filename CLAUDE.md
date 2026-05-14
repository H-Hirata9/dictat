# dictat

Windows向け音声文字起こしアプリ。superwhisperクローン。

## アーキテクチャ

グローバルホットキー（pynput）でトグル録音 → 文字起こし → LLM整形 → アクティブウィンドウに注入。

```
src/dictat/
├── app.py                     # DictatApp: Qt + スレッド統合の中心
├── audio/recorder.py          # sounddevice録音（16kHz, mono, float32）
│                              # to_wav_bytes() で WAV バイト列変換
├── transcription/
│   ├── base.py                # AbstractTranscriber: transcribe(np.ndarray) -> str
│   ├── whisper_local.py       # openai-whisper（オフライン）
│   ├── whisper_api.py         # OpenAI Whisper API
│   └── elevenlabs.py          # ElevenLabs Scribe v1
├── formatting/
│   ├── base.py                # AbstractFormatter: format(str) -> str
│   ├── verbatim.py            # パススルー
│   ├── openai_fmt.py          # GPT で整形
│   └── gemini_fmt.py          # Gemini で整形
├── hotkey/manager.py          # HotkeyManager: pynput GlobalHotKeys ラッパー
├── output/injector.py         # TextInjector: pynput.keyboard.Controller.type()
├── storage/
│   ├── config.py              # Config: %APPDATA%/dictat/config.json（ドット記法アクセス）
│   └── keys.py                # KeyStore: keyring 経由で Windows Credential Manager に保存
└── ui/
    ├── tray.py                # SystemTray: 緑/赤アイコン切り替え
    └── settings/
        ├── dialog.py          # SettingsDialog: タブ形式ダイアログ
        ├── tab_api.py         # エンジン選択 + APIキー入力
        ├── tab_hotkey.py      # ホットキー設定
        └── tab_template.py    # 整形エンジン + テンプレート
```

## スレッドモデル

- Qt メインスレッド: UI（トレイ、ダイアログ）
- pynput スレッド: ホットキー検出 → `_toggle()` を呼ぶ
- daemon スレッド: 文字起こし + 整形（ブロッキング処理）
- スレッド間通信: `_Signals(QObject)` の Qt シグナル（自動 Queued Connection）

## コマンド

```bash
# 起動
uv run python -m dictat

# テスト実行（TDD: 機能追加前にテストを書く）
uv run pytest

# 依存追加（本番）
uv add <package>
# 依存追加（dev）
uv add --dev <package>

# .exe ビルド
uv run pyinstaller dictat.spec
```

## テスト方針（TDD）
- 新機能はテストを先に書いてから実装する
- `tests/` に機能ごとのテストファイルを配置（`test_<module>.py`）
- 外部API（openai, elevenlabs, google-genai, keyring）は `unittest.mock.patch` でモック
- Qt/sounddevice/pynput に依存するコードはユニットテスト対象外（統合テストで確認）
- CI: GitHub Actions（`windows-latest`）で push/PR 時に自動実行

## データ保存

| 種別 | 場所 |
|------|------|
| 設定 | `%APPDATA%/dictat/config.json` |
| APIキー | Windows Credential Manager（keyring: service=`dictat`） |

## 文字起こしエンジン（config: `transcription.engine`）

| 値 | 説明 |
|----|------|
| `whisper_local` | openai-whisper ローカル実行。`transcription.whisper_model` でモデル指定 |
| `whisper_api` | OpenAI Whisper API。`openai` APIキー必要 |
| `elevenlabs` | ElevenLabs Scribe v1。`elevenlabs` APIキー必要 |

## 整形エンジン（config: `output.formatting`）

| 値 | 説明 |
|----|------|
| `verbatim` | 変換なし |
| `openai` | `formatting.model` と `formatting.template` を使って GPT 整形 |
| `gemini` | 同上、Gemini 使用 |

## 注意事項

- テキスト注入前に 50ms のディレイあり（ホットキーリリース後のフォーカス戻り待ち）
- ローカル Whisper はモデル初回ロード時に数秒かかる（lazy load）
- ホットキー変更は設定保存時に即時反映（再起動不要）
