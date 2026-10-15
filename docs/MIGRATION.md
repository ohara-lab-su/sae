# 移植記録

## 移植元と移植先

移植元: `/Users/nakada/daruma_dev/analysis-python/SAE/SAE`。
同じ親ディレクトリの 0.0.49 配布物ではなく、pyproject.toml が 0.0.58 を示す src 配置のソースを使用。
移植元への書き込みは行っていません。作業先の書き込み確認後にコピーして移植しました。

移植先: このディレクトリ。元の LICENSE、データテーブル、サンプル、旧 CLI スクリプトを保存。
元の各 Python ファイルの SHA-256 は `source-manifest.json` に記録しています。

## 設計

計算コードを所有者とする `sae.<code>` 階層を設け、DOS・入力・出力・擬ポテンシャルなどに分離。
既存の IO クラス 63 個は実装そのものを移動し、旧パスは新実装への互換 import に変更しました。
名前を変えたラッパークラスを大量に積み重ねる構成ではありません。
既存クラスのデータ構造と解析メソッドは引き継いでいます。

`sae.structure.Structure` は幾何の状態と操作だけを担当します。
全コードの入出力を抽象化する万能クラスや、コード固有の値を巨大な属性集合に集めるクラスはありません。
データクラスは使用していません。

新たに整理したクラス:

- OpenMX `Input`: 設定・ブロック・種定義・原子座標・固定指定を所有。未知の入力行を保持。
- HiLAPW `Input`: 空間群・対称性サイト・ネイティブ単位の格子・スピン・k 点を所有。
- VASP `Poscar`: 構造・タイトル・Selective dynamics・末尾セクションを所有。
- OpenMX `dos.TotalDOS`: エネルギー・スピン別 DOS・積分 DOS を所有。参照エネルギー変更と区間積分。

これらは `read` / `write` または `from_string` / `to_string` を持ちます。
既存の他のクラスはファイルを受ける従来のコンストラクターと get_* メソッドを維持しています。
新しい OpenMX/HiLAPW 入力、POSCAR、OpenMX TotalDOS と対応する旧 API は
データ表現・コンストラクターが異なるため、旧実装を LegacyInput/LegacyPoscar/LegacyTotalDOS として残しています。

## 共通の修正

- パッケージの一括 eager import を廃止。名前空間からクラスを要求したときにロード。
- 移植した IO モジュール内の循環した `io import *` を明示的な依存に変更。
- 移植した IO モジュールから import 時の sys.path 書き換えを除去。
- 外部 x_logger への必須依存を除き、標準 logging を使用。
- 移植した reader のコンストラクターの診断 print は debug ログへ変更。
- 移植した IO とトップレベル互換関数の sys.exit を例外に変更。
- 共通テキスト読み込みは pathlib・UTF-8・gzip・末尾改行なしを処理。
- Python 2 の負の import level と、移植 IO 内の削除済み NumPy scalar alias を修正。
- QE TotalDOS の積分 DOS 参照名を修正。積分列はスピン合計なので spin=0 のみ受理。
- 旧 Read のコード選択を明示化。HiLAPW が VASP reader へ流れる不具合とデフォルトファイル名を修正。
- Bader の pandas 空白区切り指定を sep に変更。

## 互換性・範囲

Python 3.7 の構文とアノテーションを採用。ビルド用 setuptools も Python 3.7 対応範囲に設定。
必須依存は NumPy、既存解析 reader の ASE/pandas 等は `analysis` extra。
新コード固有の IO クラスがすべて同一のメソッド名になるような機械的な統一はしていません。

旧スクリプトと一般関数は互換用に保存しています。一部の旧描画・出力関数は標準出力やファイルへの
書き込み等の旧挙動を引き継ぎます。すべての CLI を新 argparse CLI に書き直したという意味ではありません。
新 CLI は OpenMX/HiLAPW/VASP の inspect と OpenMX のパラメーター編集を提供します。

HiLAPW のサイトは対称性展開しません。単位は自動推測しません。
OpenMX の入力からセルを得る際には Atoms.UnitVectors を必要とします。
新しい OpenMX TotalDOS は 3 列・5 列の表形式に対応し、PDOS は別クラスです。
Structure は非退化の完全周期セルを扱います。分子・部分周期は既存の対応 reader の範囲です。

## 検証

- Python 3.12: pytest による 97 件のテスト。
- 63 クラスの新旧 import が同一のクラス実装を指すことを確認。
- OpenMX/HiLAPW/POSCAR のラウンドトリップ、単位、非直交セル、スケール、原子順、拘束、未知設定保持。
- OpenMX のスピン別 DOS と補間端点を含む積分。
- 代表 fixture による旧 OpenMX/HiLAPW/VASP、FDMNES 入力、QE DOS、Athena の値検証。
- CLI、上書き拒否、欠損ファイル、gzip、末尾改行なし、軽量 import。
- Python 3.7.9 実機: 全 Python ソース・テストのコンパイル、軽量名前空間 import、Unicode/gzip IO。

Python 3.7 環境に NumPy がなく、外部パッケージ取得も制限されたため、3.7 上の数値テストは未実施。
元プロジェクトにテスト用の実計算データセットはありません。FDMNES の版別出力、OpenMX の SCF/PDOS、
WIEN2k、RMC_POT、LOBSTER、Bader、大容量 CHGCAR などは配置・import の検証が中心で、
科学的な値の網羅的な回帰検証は実施していません。元の各パーサーの対応形式上の制約も残ります。

配布 wheel を別ディレクトリに依存追加なしでインストールし、作業ツリーを import パスから
外した状態でも同じ 97 件が成功しました。旧名前空間の明示的な公開名 170 個も解決を確認。
wheel には元の 4 つの `.list` データテーブルが含まれることを検査しました。
