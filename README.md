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

## VS Codeでのノートブック開発フロー

### 1. ノートブックファイルの作成

VS Codeで新しいPythonファイルを作成し、Databricksノートブック形式で記述します：

```
notebooks/
└── data_ingestion_example.py
```

### 2. ノートブックの基本構造

Databricksノートブックは以下の要素で構成されます：

```python
# Databricks notebook source
# MAGIC %md
# MAGIC # タイトル

# COMMAND ----------

# コードセル
from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()
```

**重要な要素:**
- `# Databricks notebook source`: ファイルの先頭に必須
- `# COMMAND ----------`: セル区切り（VS Codeのセル実行に対応）
- `# MAGIC %md`: Markdownセル
- `# MAGIC`: Markdownセル内の各行に必要

### 3. データ取り込みの実装フロー

サンプル実装: [notebooks/data_ingestion_example.py](notebooks/data_ingestion_example.py)

#### ステップ1: 接続確認

```python
from pyspark.sql import SparkSession
spark = SparkSession.builder.getOrCreate()
print(f"Spark Version: {spark.version}")
```

#### ステップ2: データの作成・取得

```python
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

# スキーマ定義
schema = StructType([
    StructField("prefecture_code", StringType(), False),
    StructField("prefecture_name", StringType(), False),
    StructField("year", IntegerType(), False),
    StructField("population", IntegerType(), False)
])

# DataFrameの作成
df = spark.createDataFrame(data, schema=schema)
```

#### ステップ3: Delta Tableへの保存

```python
# Delta形式で保存
table_name = "population_statistics"
save_path = f"/tmp/delta/{table_name}"

df.write \
    .format("delta") \
    .mode("overwrite") \
    .save(save_path)
```

#### ステップ4: データの読み込みと確認

```python
# Delta Tableから読み込み
df_loaded = spark.read.format("delta").load(save_path)
df_loaded.show()
```

#### ステップ5: データ変換と集計

```python
# 集計処理の例
yearly_stats = df_loaded.groupBy("year") \
    .agg({"population": "sum"}) \
    .orderBy("year")
```

### 4. VS Codeでの実行方法

**方法1: セル単位での実行**
1. Databricks拡張機能がインストールされていることを確認
2. `# COMMAND ----------` で区切られたセルにカーソルを置く
3. セル実行ボタンをクリック、またはショートカットキーで実行

**方法2: ノートブック全体の実行**
1. VS Codeのコマンドパレット（`Ctrl+Shift+P`）を開く
2. "Databricks: Run File" を選択
3. Databricksワークスペースで実行される

**方法3: ローカル実行（Databricks Connect使用）**
```powershell
# 仮想環境を有効化
.\.venv\Scripts\Activate.ps1

# Pythonスクリプトとして実行
python notebooks/data_ingestion_example.py
```

### 5. デバッグとトラブルシューティング

**接続確認:**
```powershell
# 環境変数の確認
Get-Content .\.databricks\.databricks.env

# Databricks CLI認証確認
databricks auth login --host https://dbc-c774cc06-d9a6.cloud.databricks.com
```

**よくあるエラー:**
- **認証エラー**: `.databricks/.databricks.env` の設定を確認
- **モジュールが見つからない**: 仮想環境が有効化されているか確認
- **Spark接続エラー**: サーバーレスコンピュートが有効か確認

### 6. データ取り込みのベストプラクティス

1. **Delta Lake形式を使用**: トランザクション、バージョニング、タイムトラベルのサポート
2. **スキーマの明示的定義**: データ型を明確に定義することでエラーを防止
3. **パーティショニング**: 大規模データの場合は適切にパーティション分割
4. **データバリデーション**: 取り込み前にデータの整合性チェックを実施
5. **エラーハンドリング**: try-exceptブロックでエラーを適切に処理

### 7. 次のステップ

- **実データ取得**: e-Stat API等の政府統計APIからのデータ取得
- **データクレンジング**: 欠損値処理、型変換、異常値検出
- **スケジュール実行**: Databricks Jobsでの定期実行設定
- **可視化**: Databricks SQLやDashboardでのビジュアライゼーション

## トラブルシューティング

### 間違ったPythonバージョンが使用される場合

プロジェクトディレクトリに `.python-version` ファイルが存在し、`3.11.9` と記載されていることを確認してください。

### PowerShell実行ポリシーエラー

PowerShellスクリプトの実行が制限されている場合は、`-ExecutionPolicy Bypass` オプションを使用してください。

## プロジェクト構成

### ディレクトリ構造

```
databricks_practice_04/
├── .claude/              # Claude Code設定
├── .databricks/          # Databricks設定とバンドル(56 MB)
│   ├── .databricks.env   # 環境変数(認証、Spark設定)
│   └── bundle/dev/       # 開発環境用バンドル
│       ├── terraform/    # Terraformインフラ設定
│       └── sync-snapshots/ # ワークスペース同期
├── .git/                 # Gitバージョン管理
├── .venv/                # Python仮想環境(329 MB)
├── .vscode/              # VS Code設定
│   └── settings.json     # Jupyterセル区切り設定
├── notebooks/            # Databricksノートブック
│   └── data_ingestion_example.py  # データ取り込みサンプル
├── .gitignore
├── .python-version       # Python 3.11.9を指定
├── databricks.yml        # Databricksバンドル定義
├── install-pyenv-win.ps1 # pyenvインストールスクリプト
└── README.md             # このファイル
```

### 主要ファイルの説明

| ファイル | 目的 |
|---------|------|
| `databricks.yml` | Databricks Asset Bundle設定(開発環境の定義) |
| `.python-version` | Python 3.11.9を指定(pyenvが使用) |
| `install-pyenv-win.ps1` | Windows用pyenvインストールスクリプト |
| `.databricks/.databricks.env` | Databricks接続とSpark設定の環境変数 |
| `.databricks/bundle/dev/terraform/` | Databricks provider v1.87.0を使用したTerraform設定 |
| `.vscode/settings.json` | Databricksノートブック互換のJupyterセル区切り設定 |

### アーキテクチャの特徴

1. **Databricks Asset Bundles (DAB)**: 開発環境(dev)用の構成管理を使用
2. **サーバーレスコンピュート**: Databricksの最新サーバーレスアーキテクチャに対応
3. **Infrastructure as Code**: TerraformでDatabricksリソースを管理
4. **pyenvによるバージョン管理**: Python 3.11.9で環境の再現性を確保
5. **VS Code統合**: Jupyterノートブック形式でのDatabricks開発に対応
6. **metadata-service認証**: Databricks Connectを使用したローカル開発に適した認証方式

## プロジェクト情報

- **Bundle名**: databricks_practice_04
- **Databricks Workspace**: https://dbc-c774cc06-d9a6.cloud.databricks.com
- **Target**: dev (development mode)
- **Pythonバージョン**: 3.11.9
- **Databricks Runtime**: DBR15
- **認証方式**: metadata-service
- **Terraformプロバイダー**: databricks v1.87.0
