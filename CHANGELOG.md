# ChangeLog

## Ver_0.0.10

- setup.py がアホ(環境によってはパッケージのサブフォルダが入らない)

## Ver_0.0.9, 2020.06.23 10:33

XAFS周りに注力して修正(ネームスペース修正,Python3に伴う修正)

 - StructureAnalysisEnvironment/get_atomic_radius.py:
    - 原子番号、元素名変換データーベースへのパス関係の修正
    - get_atomic_radius0(num)
    - get_atomic_radius1(atom)
    - get_atomic_number1(atom)
    - get_atomic_symbol0(num)

XAFS周りに注力して修正(バグ修正)

- io/fdm/ReadFdmInp.py:
    Crystal の文字のあとにスペースが一つ以上入っていないと atoms_index_j の生成が出来ない問題
- setup.py:
    実はpackage化せずに直接 install すると MANIFEST.in 記述が無視されて
    *.list ファイルが登録されない問題があった。
    setup.py 中に直接 packages にファイルを apped することで解決

## ver_0.0.8, 2020.06.05

修正(主に、ネームスペース変更の影響)

- パッケージの構造修正
- cfg to vasp script修正(atoms_index をきちんと引けるようにした)
- import エラー修正
- copyright の修正


## ver_0.0.8, 2020.06.04 alpha

- cfg to vasp 関係を修正
    - atoms_index を引数に引く

## ver_0.0.7, 2019.03.15, 10:16

- ReadFdmInp.txt バグ修正

## ver_0.0.6 2018.1015

- Python2/3 両対応・暫定対策(追加対応)

## ver_0.0.3, 2018.08.17:

- Python2/3 両対応・暫定対策(ほぼ全コード対応)

## ver_0.0.2, 2018.08.15:

- Python2/3 両対応・暫定対策
