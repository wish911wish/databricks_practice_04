# Databricks notebook source
# MAGIC %md
# MAGIC # データ取り込みサンプル
# MAGIC
# MAGIC このノートブックでは、政府統計データの取り込みから基本的な処理までの流れを示します。
# MAGIC
# MAGIC ## 処理の流れ
# MAGIC 1. Databricks Connectの接続確認
# MAGIC 2. サンプルデータの作成
# MAGIC 3. Delta Tableへの保存
# MAGIC 4. データの読み込みと確認

# COMMAND ----------

# MAGIC %md
# MAGIC ## 1. セットアップと接続確認

# COMMAND ----------

from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp, to_date
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DoubleType, DateType

# Spark セッションの取得
spark = SparkSession.builder.getOrCreate()

# バージョン確認
print(f"Spark Version: {spark.version}")
print(f"Databricks Runtime: DBR15")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 2. サンプルデータの作成
# MAGIC
# MAGIC 政府統計データを模したサンプルデータを作成します。
# MAGIC このサンプルでは人口統計データを想定しています。

# COMMAND ----------

# スキーマ定義
schema = StructType([
    StructField("prefecture_code", StringType(), False),
    StructField("prefecture_name", StringType(), False),
    StructField("year", IntegerType(), False),
    StructField("population", IntegerType(), False),
    StructField("population_density", DoubleType(), True),
    StructField("area_km2", DoubleType(), True)
])

# サンプルデータ
sample_data = [
    ("01", "北海道", 2023, 5224614, 66.0, 78421.0),
    ("13", "東京都", 2023, 14047594, 6402.0, 2194.0),
    ("27", "大阪府", 2023, 8837685, 4640.0, 1905.0),
    ("40", "福岡県", 2023, 5135214, 1028.0, 4987.0),
    ("01", "北海道", 2022, 5216615, 66.5, 78421.0),
    ("13", "東京都", 2022, 14064696, 6409.0, 2194.0),
    ("27", "大阪府", 2022, 8837685, 4640.0, 1905.0),
    ("40", "福岡県", 2022, 5138891, 1031.0, 4987.0),
]

# DataFrameの作成
df = spark.createDataFrame(sample_data, schema=schema)

# データ確認
print("サンプルデータの件数:", df.count())
df.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 3. データの基本的な確認

# COMMAND ----------

# スキーマ確認
df.printSchema()

# 基本統計
df.describe().show()

# 都道府県別の人口推移
df.orderBy("prefecture_name", "year").show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 4. Delta Tableへの保存
# MAGIC
# MAGIC Databricksでは、Unity Catalogを使用したデータ管理が推奨されます。
# MAGIC Unity Catalogを使用することで、カタログ、スキーマ、テーブルの3層構造で
# MAGIC データを管理できます。

# COMMAND ----------

# Unity Catalogのカタログとスキーマを設定
# 注: 事前にカタログとスキーマを作成しておく必要があります
# デフォルトのカタログ名を使用（環境に応じて変更してください）
catalog_name = "default"  # または使用しているカタログ名
schema_name = "default"  # または使用しているスキーマ名
table_name = "population_statistics"

# 完全修飾テーブル名
full_table_name = f"{catalog_name}.{schema_name}.{table_name}"

# Unity Catalogの管理テーブルとして保存
df.write \
    .format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable(full_table_name)

print(f"データを {full_table_name} に保存しました")

# COMMAND ----------

# MAGIC %md
# MAGIC ## 5. 保存したデータの読み込みと確認

# COMMAND ----------

# Unity Catalogのテーブルから読み込み
df_loaded = spark.read.table(full_table_name)

print("読み込んだデータの件数:", df_loaded.count())
df_loaded.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 6. データの変換と集計の例

# COMMAND ----------

# 年別の総人口を計算
yearly_population = df_loaded.groupBy("year") \
    .agg({"population": "sum"}) \
    .withColumnRenamed("sum(population)", "total_population") \
    .orderBy("year")

print("年別総人口:")
yearly_population.show()

# 都道府県別の人口密度ランキング（2023年）
population_density_ranking = df_loaded \
    .filter(col("year") == 2023) \
    .orderBy(col("population_density").desc()) \
    .select("prefecture_name", "population", "population_density")

print("人口密度ランキング（2023年）:")
population_density_ranking.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## 7. テーブルとしての登録（オプション）
# MAGIC
# MAGIC Delta Tableをカタログに登録することで、SQL文でもアクセス可能になります。

# COMMAND ----------

# 一時ビューとして登録
df_loaded.createOrReplaceTempView("population_view")

# SQLでのクエリ実行
result = spark.sql("""
    SELECT
        prefecture_name,
        year,
        population,
        ROUND(population / 1000000, 2) as population_millions
    FROM population_view
    WHERE year = 2023
    ORDER BY population DESC
""")

print("SQL クエリ結果:")
result.show()

# COMMAND ----------

# MAGIC %md
# MAGIC ## まとめ
# MAGIC
# MAGIC このノートブックでは以下の処理を実装しました：
# MAGIC
# MAGIC 1. Spark セッションの確認
# MAGIC 2. サンプルデータの作成（政府統計データを模した人口統計）
# MAGIC 3. Delta Lake形式でのデータ保存
# MAGIC 4. 保存したデータの読み込み
# MAGIC 5. データの変換と集計
# MAGIC 6. SQLを使用したデータアクセス
# MAGIC
# MAGIC ### 次のステップ
# MAGIC
# MAGIC - 実際の政府統計APIからのデータ取得（e-Stat API等）
# MAGIC - データクレンジングとバリデーション
# MAGIC - より複雑な集計とビジュアライゼーション
# MAGIC - スケジュール実行の設定
