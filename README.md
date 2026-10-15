# SAE クラスライブラリ

計算コードごとのクラスと、ファイル・構造・変換・出力を担当するクラスで構成しています。
実装はすべて `src/sae` 内にあり、旧プロジェクトや旧パッケージは不要です。

```python
from sae import VASP
vasp = VASP("POSCAR")
vasp.conv_direct2car()
vasp.write(outname="converted", code="FDMNES")
```

`sae/vasp/poscar.py` には構造データと操作メソッドの本体があり、
`sae/vasp/poscar_writer.py` には PoscarWriter の書き出し実装があります。
`sae/fdmnes/inp_writer.py` には FDMNES 入力生成クラスの本体があります。
同様に OpenMX, HiLAPW, PWscf, WIEN2k, RMC_POT, LOBSTER, Bader, Athena, PF を整理しています。

元の単独関数も CoordinateTransforms, SupercellOperations, ElementTable,
TextFiles, 各コードの Writer 等のメソッドへ移植しています。
計算式・単位・既定値は保持し、必要な I/F 修正は検証記録に記します。

[設計](docs/design.md) / [実装の対応表](docs/implementation-map.json)

## インストール

```sh
python -m pip install .
```

パッケージ設定は `pyproject.toml` に記述しています。setup.py はありません。
Python 3.7 の構文に対応します。数値ライブラリは実行するPythonに対応する版が必要です。

[検証記録](docs/validation.md)を参照してください。

## 構成例

- `sae/vasp/vasp.py`: VASP の構造・入力・出力・解析オブジェクトを保持するクラス。
- `sae/vasp/poscar.py`: POSCAR のデータ保持・読み込み・座標操作の実装。
- `sae/vasp/poscar_writer.py`: POSCAR の書き出しクラス。
- `sae/fdmnes/inp_writer.py`: FDMNES の入力パラメータと生成メソッド。
- `sae/geometry/coordinates.py`: 既存の座標変換式を持つクラス。
- `sae/geometry/supercell.py`: 既存のスーパーセル生成処理を持つクラス。

クラスを再エクスポートするだけの旧パッケージは収録していません。
各処理はここにあるクラスのメソッド本体で実行します。
