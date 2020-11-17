# ChangeLog

## Ver_0.0.15, 2020.11.18 08:00

- Rcfg2vasp.py にて、引数(変換したいファイル名) を cfg あり無しどちらでも対応

## Ver_0.0.15

- ReadFdmSd.py
    - コンストラクタで bav インスタンスを引けるように

- ReadFdmTxt.py
    - E_fermi に互換として、結果 0 を返すようにする
    
- ReadFdmSd2020.py
    - d 軌道の情報取り出しに関してのバグ修正
    
## Ver_0.0.14, 2020.08.12 09:50

- 旧来の互換propertyが一部未実装なのを修正
    - ReadFdmSd.py
    - ReadFdmSd2016.py
    - ReadFdmSd2020.py

- カプセル化推進(&新版調整)
    - ReadFdmText.py

- 微調整
    - bin/FDplot_LDOS.py
    - bin/fdLDOSmulti.py
    
## Ver_0.0.13, 2020.08.11 10:21

- bugfix:
    - ReadAthenaNor.py

- 吸収端のエネルギー取得の 2020版
    - ReadFdmBav.py
    - ReadFdmBav2020.py

- カプセル化推進(I/F互換のため)
    - ReadFdmBav2016.py
    
## Ver_0.0.12, 2020.08.11 09:11

- ReadAthenaNor.py
    - カプセル化推進
    - バージョン切り替えに関してのバグフィックス
- ReadFdmBav2020.py
    - カプセル化推進
    - lmax 取得に関しての 2020版のための修正
- ReadFdmBav.py
    - カプセル化推進

## Ver_0.0.11, 2020.07.17-23 14:54

FDMNES のバージョンによる切り替えの準備

- ReadFdmBav.py
- ReadFdmBav2016.py
- ReadFdmBav2020.py
- ReadFdmSd.py
- ReadFdmSd2016.py
- ReadFdmSd2020.py

## Ver_0.0.10, 2020.06.24 07:51

- setup.py がアホ(環境によってはパッケージのサブフォルダが入らない):
  (実はこれは PyCharm 側で ```__ini___.py``` がaddされてなかったため
   git add ではダメ。)
- matplotlib の画面が表示できない問題:
  (これも環境の問題で, yum で tkinter を導入に pyenv で python を導入する必要)
- 細かい調整

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
