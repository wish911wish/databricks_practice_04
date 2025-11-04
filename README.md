# databricks_practice_04
政府統計データを使用したデータ分析の練習

## 環境要件

- Databricks Runtime 15 (DBR15) に対応
- Python 3.11.9
- pyenv-win (Pythonバージョン管理)

## セットアップ手順

### 1. pyenv-winのインストール

PowerShellで以下を実行:

```powershell
Invoke-WebRequest -UseBasicParsing -Uri "https://raw.githubusercontent.com/pyenv-win/pyenv-win/master/pyenv-win/install-pyenv-win.ps1" -OutFile "./install-pyenv-win.ps1"
& "./install-pyenv-win.ps1"
```

### 2. Python 3.11.9のインストール

```powershell
& 'C:\Users\<ユーザー名>\.pyenv\pyenv-win\bin\pyenv.bat' install 3.11.9
```

### 3. プロジェクトでPython 3.11.9を指定

プロジェクトディレクトリで以下を実行:

```powershell
cd C:\Users\<ユーザー名>\development\databricks_practice_04
& 'C:\Users\<ユーザー名>\.pyenv\pyenv-win\bin\pyenv.bat' local 3.11.9
```

### 4. 仮想環境の作成

```powershell
& 'C:\Users\<ユーザー名>\.pyenv\pyenv-win\versions\3.11.9\python.exe' -m venv .venv
```

### 5. 仮想環境の有効化

```powershell
.\.venv\Scripts\Activate.ps1
```

もしPowerShellの実行ポリシーでエラーが出る場合:

```powershell
powershell -ExecutionPolicy Bypass -Command ".\.venv\Scripts\Activate.ps1"
```

### 6. Databricks Connectのインストール

仮想環境を有効化した状態で:

```powershell
python -m pip install --upgrade pip
pip install databricks-connect
```

## VSCode設定

### Pythonインタープリタの選択

1. `Ctrl+Shift+P` を押す
2. "Python: Select Interpreter" を選択
3. `.venv\Scripts\python.exe` を選択

## pyenv環境変数の永続化 (オプション)

今後の新しいターミナルでpyenvを使えるようにするには、PowerShellで以下を実行:

```powershell
[System.Environment]::SetEnvironmentVariable('PYENV', $HOME + '\.pyenv\pyenv-win\', 'User')
[System.Environment]::SetEnvironmentVariable('PYENV_ROOT', $HOME + '\.pyenv\pyenv-win\', 'User')
[System.Environment]::SetEnvironmentVariable('PYENV_HOME', $HOME + '\.pyenv\pyenv-win\', 'User')
[System.Environment]::SetEnvironmentVariable('Path', $HOME + '\.pyenv\pyenv-win\bin;' + $HOME + '\.pyenv\pyenv-win\shims;' + [System.Environment]::GetEnvironmentVariable('Path', 'User'), 'User')
```

## 使用方法

### Databricks Connectの確認

```powershell
pip show databricks-connect
```

### Pythonバージョンの確認

```powershell
python --version
# Python 3.11.9 と表示されることを確認
```

## トラブルシューティング

### 間違ったPythonバージョンが使用される場合

プロジェクトディレクトリに `.python-version` ファイルが存在し、`3.11.9` と記載されていることを確認してください。

### PowerShell実行ポリシーエラー

PowerShellスクリプトの実行が制限されている場合は、`-ExecutionPolicy Bypass` オプションを使用してください。

## プロジェクト情報

- Bundle名: databricks_practice_04
- Databricks Workspace: https://dbc-c774cc06-d9a6.cloud.databricks.com
- Target: dev (development mode)
