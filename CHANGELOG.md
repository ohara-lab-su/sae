# ChangeLog

## Ver_0.0.57, 2025.11.12

- pip install . (project.toml) では bin/*.py の導入が難しい
- setup.py を修正(python3.6/python3.10でも動作させることを前提とする)
  - setuptools が 古いと（特定のバージョン？） Vplot_TDOS.py のような
    スクリプトの導入が失敗するので、setuptools をversionを上げる
  - その他色々と setup.py 関係を修正

## Ver_0.0.56, 2025.11.07

- symlink 構造が不要みたいなので(setup.pyの工夫だけで終わり)その方式を止める
 
## Ver_0.0.55, 2025.11.07

- bubfix
  - Rvasp2cfg.py 検証テストで version.py 動作不良を発見
 
## Ver_0.0.54, 2025.11.07

インストール環境の整備
- python 3.6 環境で setup.py install でインストール可能
- python >3.11 環境で pip install . (project.toml) でインストール可能
- setup.py/toml の共存環境
- setup.py/version.py の情報源(バージョン番号)を project.toml に一元化

モジュール周りの生合成の整備
- 何年もの間未調整だった整合性を調整し直している(途中)

全体のパッケージ(Rvasp2cfg)とかの検証はこれから

## Ver_0.0.53, 2022.03.20

Bader 体積が巨大だと（原子数が多いと）BvAt ファイルの原子情報が全部
繋がってしまう

つまりこれは、
Li P S
100 300 300

だとすると
Li P S
100300300

となる。
これは、BvAt からまもとに構造情報を取得しようと atom 情報が分離できずにすると失敗する

BvA ファイルをヘッダ部分と原子ポジション/ＦＦＴ情報の二つに分ける
ことにより、BvAt ファイルと POSCAR 指定で情報を抜けるようにした。
選択性

```
split_chgcar=True
```

```
- samples/chec_Li_CHGCAR.py
- samples/copy_Li_CHGCAR.py
- samples/sim_Li_CHGCAR.py (主にこれの改変)
- StructureAnalysysEnvironment/io/bader/ReadBaderBvat.py
- StructureAnalysysEnvironment/io/bader/UtilBaer.py
- StructureAnalysisEnvironment/io/vasp/read_split_chgcar.py
- StructureAnalysisEnvironment/io/vasp/ReaddVaspChgcar.py
- StructureAnalysisEnvironment/io/vasp/ReaddVaspChgcarFooter.py
- StructureAnalysisEnvironment/io/vasp/ReaddVaspChgcarHeader.py
```

## 0.0.53, 2022.05.14 16:07

- VASP CHGCAR SUM 関係を追加（突貫)

## 0.0.52, 2021.09.00 07:57

- FDM plot 関係 の ylim=0 化 (一部)
 
## 0.0.51, 2021.09.09 07:41

- Vplot_LDOS.py などの V* 関係スクリプトの name spcae 修正
 
## 0.0.50, 2021.09.03 07:41

- FD*.py, fd*.py 関係
  - namespace の修正(io系に対応)

## Ver_0.0.49, 2021.09.02 08:24

- FDplot_*DOS*.py
  - namespace の修正(io系に対応)
 
## Ver_0.0.48, 2021.07.24 14:24

- WiteFdmInp.py
  - convolution 関係のオプションを追加

## Ver_0.0.47, 2021.07.23 11:22

- WiteFdmInp.py
  - added energpho FLAG

## Ver_0.0.46, 2021.07.23, 10:14

- WriteFdmInp.py
  - radius の変更に radius 以外にも R 引数で変更できるようにした

## Ver_0.0.45, 2021.06.18, 07:48

- ReadBaderBcf.py
  - get_distance(atom)
  - get_charge(atom)
  
## Ver_0.0.44, 2021.06.17, 08:53

- ReadRmcpotCfg.py  
  - 例外処理の強化
  - Integer + '.' で終わる文字の Integer 化機能を追加

## Ver_0.0.43, 2021.06.05, 14:48

- Rmt 変更しながら FDMNES を計算するサンプルスクリプト追加

## Ver_0.0.42, 2021.06.03, 09:06

- bugfix (VbaderVolumeSum.py)

## Ver_0.0.41, 2021.06.02, 08:41

46LiI 以外の系で動かないことがある問題。fft-mesh のパラメーター問題。

フレーム側のバグと思って調査したけっか、結局 bin 側のミスだったが、
結果的にバグトレース系の情報が充実した。それに関しての update

- modified: WriteBaderVolume.py
- modified: WriteVaspChgcar.py
- bugfix: VbaderVolumeSum.py: ngx などの FFT-mesh 情報を writer に食わせてなかった問題の修正

## Ver_0.0.40, 2021.06.02, 07:47

- bin
  - VbaderVolumeSum.py: -p all_atom の誤解のままだったのを修正(中身は完全に別物)
  
## Ver_0.0.39, 2021.06.02, 07:27

- bin
  - VbaderVolumeSum.py: logger 追加
- io.vasp
  - ReadVaspChgcar.py: logger 追加
  - WriteVaspChgcar.py: logger 追加
- io.bader
  - WriteBaderVolume.py: logger 追加
  - UtilBader.py: atom_all 化で間違って消してしまった部分を復活
 
## Ver_0.0.38, 2021.06.01, 21:13

- mdified: UtilBader.py

```angular2html
-p all_atoms
-p all_bader

オプションを勘違いしていた点について修正
```

## Ver_0.0.37, 2021.05.31, 21:35

- added samples
  
追加

- io
  - bader
    - ReadBaderAvf.py
  
## Ver_0.0.36, 2021.05.30, 11:11

logger を用意

- util/
  - logger.py
  - logger_support.py
- io/
  - bader
    - ReadBaderBcf.py (logger対応)
- bin/
  - VbaderVolueNum.py: logging level 切り替え(スクリプト中での利用のために info level の表示をシンプル化)

supace Group 関係のエラーを取り敢えず停止(使ってなかったルーチン)

- ReadHiSets.py (# from ase.lattice.spacegroup import crystal)

## Ver_0.0.35, 2021.05.29, 08:56

- VbaderVolumeSum.py (bugfix)
- VbaderVolumeNum.py: 原子番号から体積番号だけを知る

## Ver_0.0.34, 2021.05.28, 21:04

bug fix
- VbarderVolumeSum.py

## Ver_0.0.33, 2021.05.28, 19:21

Bader 対応(Bader Volume sum スクリプトを含む)

- bin
  - VbaderVolumeSum.py (指定原子の Bader Volume を BCF.data から探して、全て足し合わす)
- io
  - bader
    - ReadBaderBcf.py
    - ReadBaderBvat.py
    - UtilBader.py
    - WriteBaderVolume.py
  - vasp
    - ReadVaspChgcar.py
    - WriteVaspChgcar.py
  
## 2021.05.27, 08:34

- bin/Vch --> bin/Vch.py

## Ver_0.0.32, 2021.05.26, 09:11

- io/
  - fdm/
    - WriteFdmInp.py: property 追加
    - WriteFdmfile.py: 新規

## Ver_0.0.31, 2021.05.25, 20:08

CHGCAR 反転
- bin/VchgInverse.py から ReadVaspChagcar() クラスを完全分離

開くことの出来ないCHGCARパターンに対応
- ELFCAR/CHGCAR 両対応（mode指定が必要、デフォルトはCHGCAR)

開くことの出来ないCHGCARパターン（ kx * ky * kz が 5 or 10 で割りきれないときにでてくる) に対応

## Ver_0.0.30, 2021.05.25, 19:42

CHCAR の反転プログラムのバグ修正および単独プログラム化。
**尾原さんへ提供版(2021.05.25, 19:42)**
現バージョンでは ReadVaspChgcar/VchgInverse は同じ内容。

- io/
  - vasp/
    - ReadVaspChgcar.py
- bin/
  - VchgInverse.py

## Ver_0.0.29, 2021.05.25, 16:19

CHGCAR の反転(反転アルゴリズムを変更)
- ReadVaspChgcar.py

## Ver_0.0.28, 2021.05.25, 08:49

- io.WriteFdmInp()
  - Muffin-tin 半径の変更オプションをお試し実装

## Ver_0.0.27, 2021.05.23, 13:56

FDvasp2fdm.py のクラス化

- io/fdm
  - WriteFdmInp.py

## Ver_0.0.26, 2021.05.11, 09:30

- conv_car2direct.py (modified)
- FDM
  - io/ReadFdmBav2020.py (changed property)
  -  bav ファイル読み込みに関しての自動的な suffix 追加の修正
    - io/ReaFdmBav.py
    - io/ReaFdmBav2020.py

## Ver_0.0.25, 2021.05.10, 19:26

- python 3.x と 2.x の互換性問題（gzip module)
    - gzip 読み込み時は decode する必要があるッぽい感じ
    
## Ver_0.0.24, 2021.05.10, 17:01

- VASP 5.4.x にて、OUTCAR からの ISYM 分解で、ISYM に相当する名前が別にある問題が発生した。
そのため、正しく情報を吸い取れないので、分離用の正規表現マッチを変更した。
  - ReadVaspOutcar.py

## 2021.04.27, 19:56

- update sample script
    - fdExp_comp_XAS.py
    
## Ver_0.0.23, 2021.04.27, 08:42

- FDvasp2fdm.py: INP 生成をオプションで制御出来る項目を多数追加
- FDvasp2fdm 中の write method を SAE 中の ASE support メソッドに追加（暫定処理）
そのうち、本家ASE にコミット予定？

### files

- bin
    - FDvasp2fdm.py
- io
    - ase_support
        - fdmnes.py

## Ver_0.0.22, 2021.04.22, 08:33

- FDclean.py が動かなくなっていたのを修正

## Ver_0.0.21, 2021.04.21, 21:07

- python 3.9 環境での FDplot_XAS.py
  - numpy = numpy + value のエラーの修正

## 2021.04.13, 21:14

- bugfix: selective-dynamic T/F 出力が byte になる問題の解決(decodeを取り敢えず入れる)
    - StructureAnalysisEnvironment/print_poscar.py
    
## 2021.04.13, 09:18

- VASP Read 関係にいくつかの基本メソッド(convet)などを追加
- 名前空間の調整、続々

## Ver_0.0.20, 2020.11.19 16:17

- 名前空間の定義リストの変更で Rvasp2cfg.py が使えなくなっていた問題を突貫修正

## Ver_0.0.19, 2020.11.18 20:48

- SAE の __init__.py を少し修正( Method の __init__ 呼び出し)

## Ver_0.0.18, 2020.11.18 20:48

>> hpcs01 へ導入版

環境によってはモジュールのattribute がみつからなくて呼び出せないことがある

1. __init__.py の呼び出し方法を変える
2. 動的なクラス呼び出しの元クラス名を変える

にて対処 (Rcfg2vasp.py でテスト)

注意) 相対は from .module_name import * などと、. (ドット)からが必須
(詳しくは __init__.py にそれぞれ記述)

## Ver_0.0.17, 2020.11.18 17:12

- numba のインストールが難しい環境があるので外す

## Ver_0.0.16, 2020.11.18 08:00

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

Manganese で setup install のみで動作確認

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
