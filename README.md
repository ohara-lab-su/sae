# StructureAnalysisEnvironment (SAE)

VASP, WIEN2k, Quantum ESPRESSO, OpenMX, CP2K, HiLAPW, FDMNES, RMC_POT などの
第一原理計算、電子状態解析、X線吸収スペクトル計算および逆モンテカルロ法の各種計算コードに対応した、
入出力・構造操作・解析の一元化を目的とする Python フレームワークです。

SAE は、計算コードごとに異なる入力・出力形式を Python のクラスとして扱い、
構造作成、入力ファイルの編集、計算結果の読み込み、解析などを、
可能な限り共通した考え方でプログラムから操作することを目的として開発してきました。

このプロジェクトは 2015 年から開発されてきた
`StructureAnalysisEnvironment` のコードを引き継ぐものです。
Python 2 時代の初期実装から、Python 2/3 両対応、Python 3 への移行、
各計算コードへの対応追加、名前空間やパッケージ構成の修正を継続し、
0.0.58 系まで開発されてきました。

**v0.1.0 では、その既存コードと開発履歴を引き継いだ上で、
現在の Python 環境で継続して利用・開発できるようにパッケージ全体を整理しました。**
旧 API の互換性を可能な範囲で維持しながら、計算コードごとの名前空間、
共通構造クラス、読み書きの API、パッケージングおよびドキュメントを整理しています。

v0.1.0 は別のプロジェクトとして作り直したものではなく、
従来の SAE の開発を継続したバージョンです。

## v0.1.0

v0.1.0 では、0.0.58 系までの SAE を基礎として、
従来コードを現在の Python パッケージとして扱いやすい形へ統合しました。

主な変更点は以下です。

- Python 3.7 以降で利用できる構文へ統一
- `src` レイアウトを用いたパッケージ構成へ整理
- 計算コードごとの名前空間を `sae.<code>` として整理
- 旧 `StructureAnalysisEnvironment` import を互換層として維持
- 既存クラスを新しい名前空間へ移し、同一機能の二重実装を避ける構成へ変更
- 構造操作の共通部分を `sae.structure.Structure` へ整理
- 主要な入力クラスに `Class.read(path)` を用いる読み込み API を導入
- `pyproject.toml` を中心とした現在の Python パッケージングへ移行
- 必須依存と解析用の追加依存を分離
- 従来の用途別スクリプトを保存しつつ、すべてを PATH へ展開する方式を廃止
- Python API、移植範囲、互換性に関するドキュメントを整理

旧コードで蓄積されてきた各計算コードのパーサーや解析処理を捨てて
新しい API だけを作り直したものではありません。
従来実装を継承しながら、今後の保守と機能追加を行いやすくすることが
v0.1.0 の主な目的です。

## フレームワークの基本的な考え方

SAE では、一般的な Python のオブジェクト指向による形で、
各計算コードの入力・出力や解析結果をオブジェクトとして扱います。

従来の SAE では、たとえば VASP の POSCAR を読み込み、
FDMNES 形式へ変換するといった処理を、計算コードの違いを吸収した
共通インターフェースから扱うことを目指していました。

v0.1.0 でもこの考え方は変わっていません。
一方で、すべての計算コードを一つの巨大な名前空間から暗黙に扱うのではなく、
現在は各計算コードの実装を明示的な名前空間へ分けています。

たとえば OpenMX の入力ファイルは次のように扱えます。

```python
from sae.openmx import Input

calculation = Input.read("openmx.dat")
calculation.set_parameter("scf.maxIter", 200)

geometry = calculation.structure
geometry.translate([0.0, 0.0, 0.2])

calculation.set_structure(geometry)
calculation.write("relaxed.dat")
```

入力ファイルをクラスとして読み込み、構造や計算条件を変更し、
再び計算コード固有の形式で書き出す、という基本的な考え方は
従来の SAE から継続しています。

## 対応する計算コード・データ

実装は計算コードを第一階層とし、その中を用途ごとに分けています。

- `sae.openmx`
  - `Input`
  - `Output`
  - `SCFHistory`
  - `Trajectory`
  - `dos`
  - `pseudopotential`
- `sae.hilapw`
  - `Input`
  - `sets.in` の格子、対称性サイト、スピン、k 点
- `sae.fdmnes`
  - `Input`
  - `InputWriter`
  - `BatchInput`
  - `BatchWriter`
  - `output`
  - `dos`
  - `spectra`
  - FDMNES 2016 / 2020 形式
- `sae.vasp`
  - `Poscar`
  - `Incar`
  - `Kpoints`
  - `Potcar`
  - `output`
  - `bands`
  - `dos`
  - `charge_density`
  - `trajectory`
  - `symmetry`
  - `charges`
- `sae.quantum_espresso`
  - `Input`
  - `Output`
  - `dos`
  - `spectra`
- `sae.wien2k`
  - `output`
  - `dos`
  - `spectra`
- `sae.rmcpot`
  - `Configuration`
- `sae.lobster`
  - `COHP`
  - `DensityOfStates`
  - `Output`
- `sae.bader`
  - `Charges`
  - `volumes`
- `sae.athena`
  - `NormalizedSpectrum`
- `sae.pf`
  - `Document`

詳細は以下を参照してください。

- [63 クラスの移植先一覧](docs/API.md)
- [移植範囲と検証](docs/MIGRATION.md)

## インストール

```sh
python -m pip install .
```

必須依存は NumPy です。

従来から存在する解析系パーサー、ASE 連携、描画機能なども利用する場合は
追加依存を導入します。

```sh
python -m pip install '.[analysis]'
```

テスト環境は次のように導入できます。

```sh
python -m pip install '.[test]'
python -m pytest
```

Python 3.7 を含む対応版の選択は pip の `Requires-Python` 解決に委ねます。

新しく追加する API では、Python 3.7 との互換性を保つため、
`list[str]` や `X | None` など Python 3.7 で使用できない型アノテーションは使用しません。

## 入出力クラス

v0.1.0 で整理した主要なドキュメントクラスでは、
入力ファイルを `Class.read(path)` で読み込みます。

対象には、たとえば以下があります。

- `openmx.Input`
- `hilapw.Input`
- `vasp.Poscar`
- `openmx.dos.TotalDOS`

一方、0.0.x 系から引き継いだクラスについては、
既存コードとの互換性を保つため、従来のコンストラクターやメソッドを維持しています。

たとえば FDMNES の既存出力クラスは次のように使用できます。

```python
sae.fdmnes.output.Output2020(prefix)
```

### OpenMX

OpenMX `Input` は、SAE が直接解釈しない未知の設定やブロックも保持します。

構造を更新するときにはサイト数、サイト順序、原子種の一致を要求し、
追加の電子数列や固定指定など、各原子に対応する情報との関係を維持します。

また、原子種ラベルは基底関数の異なる種を区別するために使われる可能性があるため、
自動的に元素記号へ置換しません。

### HiLAPW

HiLAPW の長さは元の入力単位を保存します。

また、入力に記述された対称性サイトを、自動的に全原子へ展開することはしません。

Structure へ変換するときには、必要に応じて単位を明示します。

```python
structure = input.to_structure(length_unit="bohr")
```

### VASP POSCAR

`Poscar` は以下に対応します。

- 負の体積スケール
- 3 成分スケール
- 非直交格子
- Selective dynamics

VASP 4 形式ではファイル自体に元素名が含まれないため、
必要に応じて原子種を明示します。

```python
poscar = Poscar.read("POSCAR", species=["Si", "O"])
```

Selective dynamics の意味に合わせ、

```python
movable=True
```

は VASP の `T`、すなわち移動可能を表します。

これは OpenMX 側の

```python
fixed=True
```

が固定を意味することとは逆なので注意してください。

## 共通構造クラス

`sae.structure.Structure` は、
計算コードに依存しない共通の幾何操作を担当します。

格子ベクトルは行ベクトルとして保持し、長さの内部単位は Å です。

座標の取得はコピーを返します。
構造を変更する場合は、明示的な操作を使用します。

```python
structure.translate(...)
structure.wrap(...)
structure.set_cell(...)
```

`repeat` と `select` は新しい `Structure` を返します。

計算コード固有の入力設定まで暗黙に複製することはしません。
構造そのものと、各計算コード固有の計算条件を分離して扱うためです。

## ファイルの書き込み

書き込み API は、既存ファイルを暗黙に上書きしません。

上書きが必要な場合は明示します。

```python
document.write("output.dat", overwrite=True)
```

計算入力を扱うライブラリでは、既存の計算条件や結果を誤って失わないことを優先しています。

## 旧 API との互換性

v0.1.0 は従来の SAE から連続したバージョンであるため、
旧 `StructureAnalysisEnvironment` の import 名も互換用として残しています。

移行した 63 クラスについては、新旧で別々の実装を維持するのではなく、
新しいモジュールへの shim として旧 API を提供します。

旧形式の配列配置や `get_*` メソッドなど、
既存コードで利用されてきたインターフェースも互換層で維持しています。

したがって、v0.1.0 への移行は、
従来の SAE の機能を捨てて新 API へ全面的に置き換えることを意味しません。
既存コードを動かすための互換性を残しながら、
新しいコードでは整理された `sae` 名前空間を利用できる構成としています。

## 従来のツール群

旧 SAE では、フレームワーク本体だけでなく、
それを利用する多数の実用スクリプトを同時に開発してきました。

これらは計算コードごとに名前を対応させる方式を採っていました。

- `CP*`: CP2K
- `FD*`: FDMNES
- `LA*`: HiLAPW
- `MX*`: OpenMX
- `PW*`: Quantum ESPRESSO / PWscf
- `R*`: RMC_POT
- `V*`: VASP
- `W*`: WIEN2k

たとえば、同じ処理を異なる計算コードへ適用するツールについて、
先頭のコード識別文字以外をできるだけ同じ名前とし、
似た操作で利用できるようにする設計でした。

この考え方は SAE が当初から目指してきた
「計算コードの違いによる周辺処理の差をできるだけ小さくする」
という目的の一部です。

v0.1.0 では、これらの既存スクリプトを
`src/StructureAnalysisEnvironment/bin/` に保存しています。

ただし、旧版のように用途固有の多数のスクリプトを
インストール時に一律に PATH へ登録する方式は採用していません。

今後の共通 CLI は以下から利用します。

```sh
sae --help
```

Python API の利用例については [examples](examples/) を参照してください。

## 開発の経緯

SAE は当初、第一原理計算コードごとに個別に作っていた
構造変換、入力生成、電子状態解析、プロットなどの周辺処理を、
Python 上で共通化することを目的として開発されました。

初期には Python 2 を前提としていましたが、その後 Python 2/3 両対応を経て
Python 3 へ移行しています。

その過程で、単なるファイル変換だけでなく、

- FDMNES の入出力および XANES 関連処理
- VASP の入力・出力解析
- CHGCAR / ELFCAR
- Bader charge / Bader volume
- RMC_POT の構造
- DOS / LDOS
- 構造操作
- 各種計算コード間のデータ変換

など、実際の計算・解析で必要になった機能を継続的に追加してきました。

2020～2021 年には Python 3 対応、名前空間整理、
FDMNES のバージョン対応、VASP/Bader 関係などを重点的に更新し、
その後も実際の研究計算で必要になった修正を継続しています。

2025 年には Python 3.6 系から新しい Python 環境までを考慮して
`setup.py` と `pyproject.toml` が共存する移行期のパッケージ構成を整備し、
0.0.58 まで更新されました。

v0.1.0 ではその続きを行い、
移行期の構成を整理して、現在の Python パッケージとして
今後も開発を継続できる形へまとめています。

詳細な変更履歴は [CHANGELOG.md](CHANGELOG.md) を参照してください。

## 開発方針

SAE の目的は、単に既存計算コードのファイルを読み書きすることだけではありません。

各計算コード固有の入出力を扱いながら、
可能な部分ではコード依存性を減らし、
構造操作や解析処理を再利用できるようにすることを目指しています。

ASE のような汎用ライブラリが存在する現在では、
SAE が独自にすべてを再実装すること自体には意味がありません。

一方で、

- マイナーな計算コードへの対応
- 研究上必要になった独自解析
- 複数の計算コードをまたぐ実務的な変換処理
- 過去から蓄積された解析コードの継続利用

については、SAE を維持する意味があります。

v0.1.0 では、この従来の方向性を維持しつつ、
今後の機能追加を旧来のパッケージ構造に縛られず行える基盤へ整理しています。

## ドキュメント

- [API / 移植クラス一覧](docs/API.md)
- [移植範囲と検証](docs/MIGRATION.md)
- [Examples](examples/)
- [旧 README](docs/README-original.md)
- [ChangeLog](CHANGELOG.md)

旧 README は、過去の SAE の機能、ツール群、当時の利用方法および
開発方針を記録する資料として `docs/README-original.md` に保存しています。

## ライセンス

ライセンスについては、リポジトリに含まれる `LICENSE` を参照してください。
