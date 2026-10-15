# SAE — Structure Analysis Environment

Python 3.7 の構文で使用できる、計算コード別のクラスライブラリ。
移植元は `SAE/SAE` の 0.0.58 系ソースです。元のソースには変更を加えていません。

```python
from sae.openmx import Input

calculation = Input.read('openmx.dat')
calculation.set_parameter('scf.maxIter', 200)
geometry = calculation.structure
geometry.translate([0.0, 0.0, 0.2])
calculation.set_structure(geometry)
calculation.write('relaxed.dat')
```

## 構成

計算コードを第一階層とし、その中を用途で分けています。
実装は各コードの名前空間にあり、他コードとの一括読み込みは行いません。

- `sae.openmx`: `Input`, `Output`, `SCFHistory`, `Trajectory`; `dos` と `pseudopotential`
- `sae.hilapw`: `Input`（sets.in の格子、対称性サイト、スピン、k 点）
- `sae.fdmnes`: `Input`, `InputWriter`, `BatchInput`, `BatchWriter`; `output`, `dos`, `spectra`。2016/2020 形式を区別
- `sae.vasp`: `Poscar`, `Incar`, `Kpoints`, `Potcar`; `output`, `bands`, `dos`, `charge_density`, `trajectory`, `symmetry`, `charges`
- `sae.quantum_espresso`: `Input`, `Output`, `dos`, `spectra`
- `sae.wien2k`: `output`, `dos`, `spectra`
- `sae.rmcpot`: `Configuration`
- `sae.lobster`: `COHP`, `DensityOfStates`, `Output`
- `sae.bader`: `Charges`, `volumes`
- `sae.athena`: `NormalizedSpectrum`
- `sae.pf`: `Document`

[63 クラスの移植先一覧](docs/API.md) / [移植範囲と検証](docs/MIGRATION.md)

## インストール

```sh
python -m pip install .
# 既存の解析系パーサー・ASE 連携・描画も利用する場合
python -m pip install '.[analysis]'
python -m pip install '.[test]'
python -m pytest
```

必須依存は NumPy。追加依存は使用する解析機能に応じて導入します。
Python 3.7 を含む対応版の選択は pip の Requires-Python 解決に委ねます。
新規 API は `list[str]` や `X | None` 等の 3.7 非対応アノテーションを使用しません。

## 新しいドキュメントクラス

`openmx.Input`, `hilapw.Input`, `vasp.Poscar`, `openmx.dos.TotalDOS` は
`Class.read(path)` で読み込みます。他の移植クラスは既存のコンストラクターとメソッドを
保持しています（例: `sae.fdmnes.output.Output2020(prefix)`）。

OpenMX Input は未知の設定・ブロックも保持します。構造更新時にはサイト数・順序・種別の一致を
要求し、追加の電子数列や固定指定との対応を守ります。原子種ラベルは基底の異なる種を区別するため
元素記号へ勝手に置換しません。

HiLAPW の長さは元の入力単位を保存し、対称性サイトを全原子へ自動展開しません。
`input.to_structure(length_unit='bohr')` のように、変換時には単位を明示してください。

POSCAR は負の体積スケール、3 成分スケール、非直交格子、Selective dynamics に対応。
VASP 4 形式は `Poscar.read(path, species=['Si', 'O'])` のように原子種を明示します。
`movable=True` は VASP の T（移動可）です。OpenMX の `fixed=True`（固定）とは逆です。

`sae.structure.Structure` は共有する幾何操作だけを担当し、格子ベクトルは行、長さは Å。
座標の取得はコピーを返します。変更には `translate`, `wrap`, `set_cell` を使います。
`repeat` と `select` は新しい Structure を返し、計算コード固有の設定は複製しません。

書き込みは既存ファイルを上書きしません。必要な場合は `overwrite=True` を明示します。

## 旧 API

`StructureAnalysisEnvironment` の旧 import 名は互換用に残しています。
63 クラスは新モジュールへの shim で、別実装の二重管理にはしていません。
旧形式の配列配置や get_* メソッドは互換層で維持しています。
既存スクリプトは `src/StructureAnalysisEnvironment/bin/` に保存していますが、
用途固有のスクリプト群を一律に PATH へインストールすることはやめています。
統一 CLI は `sae --help`、Python API の例は [examples](examples/) を参照してください。

旧 README は [docs/README-original.md](docs/README-original.md) に保存しています。
