#!/usr/bin/env python
##########################################################################
# K.NAKADA, kengo.nakada@gmail.com
# for WIEN2k 13.1
#
# convert/output INTDOS data
#
# read
#   case.int
#   case.outputt
#
##########################################################################
#
# 2014.06.11
#    based on wcon_dos2gnuplotdata.py (2014.06.11)
#
##########################################################################
from __future__ import print_function
################################################################################

import sys
import os
import glob
import optparse
import copy
from numpy import *

cname=os.path.basename(os.getcwd())


####################################### optparse  ####
#usage = "usage: %prog [options] case "

parser = optparse.OptionParser()
parser.add_option(  '-f','--ef',
                    action='store_true',
                    dest='FLAG_EF',
)
parser.add_option(  '-e', '--unit',
                    action='store_true',
                    dest='FLAG_UNIT',
)
parser.add_option(  '-v','--debug',
                    action='store_true',
)
parser.add_option(  '-t','--test',
                    action='store_true',
)
parser.add_option(  '-d','--deep',
                    action='store_true',
)
options,  args = parser.parse_args()

#print args,options
if len(args) > 0:
    #print "script name:",argvs[0]
    cname=args[0]

if options.debug:
    print ""
    print "BASE NAME     =",cname

### default unit (eV)
unit=''
if options.FLAG_UNIT:
    unit='ev'
    unit_tmp='eV'
else:
    unit_tmp='Ry'

######################################################


if not os.path.exists(cname+".int"):
    print cname+".int file not found"
    print "EXIT"
    sys.exit()

if options.debug:
    print "UNIT          =",unit_tmp
    print "EF0 MODE      =",options.FLAG_EF


TOTALDOS_FLAG = False
##########################################################################
# version 2014.06.05
##########################################################################
##
## read case.int
##
##########################################################################
##########################################################################

tmp = open(cname+'.int')
intfile = tmp.read()
tmp.close

# read number of orbital
intlines = intfile.split('\n')
n=intlines[2].split()
n_total_orbit=int(n[0])


###############################################################
#
# max_orbit_number : 軌道番号の最大値の取得
#
max_orbit_number=1
for line in range(1,1+n_total_orbit):
    orbital=intlines[line+2].split()
    tmp=int(orbital[1])
    if tmp > max_orbit_number:
        max_orbit_number=tmp

if options.debug:
    print ""
    print "MAXORBIT NUM  =", max_orbit_number



###############################################################
#
# natom : 最大の原子数の取得(暫定版)
#
#    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#     注意)  原子の番号の並びが小さい方から大きい方へ並んでいるのを仮定
#            つまり TOTAL-DOS は先頭行になくてはいけない
#            (もしくは TOTAL-DOS 行が存在しなくても良い)
#    !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#
atom=0
l=0
for num in range(1,1+n_total_orbit):
    orbital=intlines[num+2].split()

    atom_tmp =int(orbital[0])
    if atom_tmp == 0:
        TOTALDOS_FLAG=True

    if atom_tmp < atom:
        print "STOP: READ",cname+".int Files, atom_tmp < atom " ,atom_tmp,atom
        sys.exit()

    if atom_tmp > atom:
        atom=int(orbital[0])

natom=atom

if options.debug:
    print "NATOM         =",natom
    print "TOTAL ORBITAL =",n_total_orbit
    if TOTALDOS_FLAG:
        print "TOTLDOS       =",TOTALDOS_FLAG

###############################################################
#
# indexatom[num]  : 軌道の通し番号に対しての原子種index
# indexorbit[num] : 軌道の通し番号に対して原子種ごとの軌道番号index
# indexname[num] : 軌道の通し番号に対して軌道の記号を返す
#
indexatom =zeros((n_total_orbit+1))
indexorbit=zeros((n_total_orbit+1))
indexname=["list0"]
l=0
atom=0
for num in range(1,1+n_total_orbit):
    l += 1
    orbital=intlines[num+2].split()

    atom_tmp =int(orbital[0])
    orbit_tmp=int(orbital[1])

    indexatom[num] =atom_tmp
    indexorbit[num]=orbit_tmp
    indexname.append(orbital[2])

#   if atom_tmp == 0:
#       TOTALDOS_FLAG= True
#       indexatom[0] = 0


if options.test:
    print ""
    print "num, indexatom[num], indexorbit[num], indexname[num]"
    for num in range(1,n_total_orbit+1):
        print num, int(indexatom[num]), int(indexorbit[num]),indexname[num]
    print ""


###############################################################
#
# norbit[atom] : 原子種ごとの最大の軌道数
#
if TOTALDOS_FLAG:
    # 0番目の原子がTOTALDOSになる
    norbit = zeros((natom+1+1))
    local_index_orbit = zeros((natom+1+1,max_orbit_number+1))
else:
    norbit = zeros((natom+1))
    local_index_orbit = zeros((natom+1,max_orbit_number+1))

i=1
atom0=0

for num in range(3,3+n_total_orbit):
    orbital=intlines[num].split()
    atom=int(orbital[0])
    norbit[atom]=i
    if atom > atom0:
        i=1
        norbit[atom]=i
        atom0=atom
    i += 1

    if options.test:
        print "num,atom, norbit[atom], orbital", num-2,atom,int(norbit[atom]),int(orbital[1])

if TOTALDOS_FLAG:
    norbit[0]=1
    start=0
else:
    start=1

if options.debug:
    print ""
    for atom in range(start,natom+1):
        if atom == 0:
            print "ATOM=",atom,"NUM ORBIT",int(norbit[atom]),"(TOTAL-DOS)"
        else:    
            print "ATOM=",atom,"NUM ORBIT",int(norbit[atom])
    print ""


###############################################################
#
# index_local_orbit[atom,num_local_orbit]
#    原子毎の軌道の通し番号(num_local_orbit)を与えると軌道番号を返す
#
# index_local_num[atom,num_local_orbit]
#    原子毎の軌道の通し番号(num_local_orbit)を与えると軌道の通し番号を返す
#
num=1
for atom in range(0,natom+1):
    for num_local_orbit in range(1,int(norbit[atom])+1):
        index_local_orbit = zeros((natom+1,norbit[atom]+1))

for atom in range(0,natom+1):
    for num_local_orbit in range(1,int(norbit[atom])+1):
        index_local_orbit[atom,num_local_orbit] = int(indexorbit[num])
        num +=1

if options.test:
    print ""
    print "num, atom, norbit[atom], num_local_orbit,",
    print "indexorbit[num], index_local_orbit[atom,num_local_orbit, indexname[num]"
    num=1
    for atom in range(0,natom+1):
        for num_local_orbit in range(1,int(norbit[atom])+1):
            print num, atom, int(norbit[atom]), num_local_orbit, int(indexorbit[num]), \
                             int(index_local_orbit[atom,num_local_orbit]),indexname[num]
            num +=1


###############################################################
#
# indexnum[atom,orbit] : 原子種と軌道'番号'を与えると通し番号が得られる
#
#print "n_total_orbit",n_total_orbit
if max_orbit_number > n_total_orbit:
    indexnum =zeros((natom+1,max_orbit_number+1))
else:
    indexnum =zeros((natom+1,n_total_orbit+1))
for num in range(1,1+n_total_orbit):
    indexnum[int(indexatom[num]),int(indexorbit[num])]=num


if options.test:
    print ""
    print "num, indexnum[indexatom[num],indexorbit[num]], indexatom[num], indexorbit[num] = "
    for num in range(1,1+n_total_orbit):
        print num,int(indexnum[int(indexatom[num]),int(indexorbit[num])]),
        print            int(indexatom[num]),int(indexorbit[num])


#print ""
#for atom in range(0,natom+1):
#    for num_local_orbit in range(1,int(norbit[atom]+1)):
#        print atom,num_local_orbit, int(index_local_orbit[atom,num_local_orbit])
#print ""





##########################################################################
##########################################################################
##
## read case.dos*
##
##########################################################################
##########################################################################

ls=glob.glob(cname+'.dos*[0-9]'+unit)
nfiles=len(ls)

######### check spin #########
# ls_up[nfiles_up]
# ls_dn[nfiles_dn]
#
SPIN_FLAG=False
if nfiles == 0:
    ls_up=glob.glob(cname+'.dos*[0-9]'+unit+'up')
    nfiles_up=len(ls_up)
    for n in range(0,nfiles_up):
        src = ls_up[n]
        dst = src.replace('up','dn')
        if not os.path.exists(dst):
            print src+"file exist"
            print dst+"file not found"
            print "ERROR: not found spin files"
            print "EXIT"
            sys.exit()
    ls_dn=glob.glob(cname+'.dos*[0-9]'+unit+'dn')
    nfiles_dn=len(ls_dn)
    if not nfiles_dn == nfiles_up:
        print "ERROR: unconformity spin files"
        print "EXIT"
        sys.exit()
    nfiles=nfiles_up
    SPIN_FLAG=True
else:
    for n in range(0,nfiles):
        if not os.path.exists(ls[n]):
            print ls[n]," file not found"
            print "EXIT"
            sys.exit()

##############################   

if SPIN_FLAG:
    spin_list = [ 'up', 'dn' ]
    suffix='_'
else:
    spin_list = ['']
    suffix=''

####################
#
# pre Read 
#
for spin in spin_list:

    if spin == 'up':
        ls = ls_up
    if spin == 'dn':
        ls = ls_dn

    f = open(ls[0])
    tmp = f.read()
    f.close

    # get EF and NENRG
    doslines0 = tmp.split('\n')
    n = doslines0[1].split()
    EF=float(n[1])
    if spin == 'up':
        NENRG_up=int(n[5])
    elif spin == 'dn':
        NENRG_dn=int(n[5])
    else:
        NENRG=int(n[5])

    if options.debug:
        if spin == 'up':
            print "NENRG (up)    =",NENRG_up
        elif spin == 'dn':
            print "NENRG (dn)    =",NENRG_dn
        else:
            print "NENRG         =",NENRG

if options.debug:
    print "EF            =",EF
    print ""


######################################## SPIN roop ###########################################
for spin in spin_list:

    if spin == 'up':
        ls = ls_up
        NENRG = NENRG_up
    if spin == 'dn':
        ls = ls_dn
        NENRG = NENRG_dn

    if options.debug:
        if SPIN_FLAG:
            print "===== SPIN "+spin+" ===="
        print "ORIGINAL FILE:"

    ################################################
    #
    # Read case.dos* files
    #
    # data [atom,num,NENRG]

    data = zeros((nfiles+1,n_total_orbit+1,NENRG+1))
    
    n_orbit_page = zeros((nfiles+1))     # *.dos? ファイル一つにいくつの軌道情報があるか？
    
    # index_*_page_colum[page,colum]
    index_atom_page_colum = zeros((nfiles+1, 8+1))  # 原子番号(total-DOSの時は0)のインデックス
    index_orbit_page_colum = zeros((nfiles+1,8+1))  #
    
    num=1
    local_orbit=1
    page=0
    
    if TOTALDOS_FLAG:
        atom=0
    else:
        atom=1

    ################################################
    for dosname in ls:  # ページ(ファイルごとに分解)
       
        if options.debug: 
            print "  ",dosname

        page += 1
    
        f = open(dosname)
        dosfile = f.read()
        f.close
    
        dosdata = dosfile.split('\n')  # 行で分解
        n_orbit_page[page]=len(dosdata[2].split())-2  # 各ページごとの読み込む軌道数
                                                      # ENEを除く,TOTAL-DOS は含む
    
        max_ene=len(dosdata)-1-3
        if NENRG != max_ene:
            print "STOP ERROR:  NENRG=",NENRG," max_ene=",max_ene
            sys.exit()
    
        if options.test:
            print ""
            print "page, n_orbit_page, max_nen =", page, int(n_orbit_page[page]), max_ene
            print ""
   
        if options.debug:
            print "" 
        for colum in range(0,int(n_orbit_page[page])+1):  # カラム分割(インデックス作成用)
     
            if colum == 0: # ページの先頭
                local_orbit -= 1
                index_orbit_page_colum[page,colum] = 0
                num -= 1
            elif local_orbit > int(norbit[atom]):  # ページ途中で原子が切り替わる
                atom += 1
                local_orbit = 1
                index_orbit_page_colum[page,colum] = 1
            else:
                index_orbit_page_colum[page,colum] = local_orbit
     
            ## index[page,colum]
            index_atom_page_colum[page,colum] = atom
     
            if options.test:
                print "num, page, colum, atom_page_colum[page,colum], orbit_page_colum[page,colum]   ",\
                           num,page,colum,\
                           int(index_atom_page_colum[page,colum]), \
                           int(index_orbit_page_colum[page,colum])   # local_num
    
            if options.debug:
                print page,colum,int(index_atom_page_colum[page,colum]), int(index_orbit_page_colum[page,colum]),
                print int(index_orbit_page_colum[page,colum]),indexname[int(index_orbit_page_colum[page,colum])+1]
               #print int(index_orbit_page_colum[page,colum]),indexname[int(index_orbit_page_colum[page,colum])]
     
            num += 1
            local_orbit += 1
    
    
        for i in range(3,len(dosdata)-1): # 行ごとの処理
            doslines=dosdata[i].split()   # 各行を列に分解
            ene=i-2
           #print 'ENERRY=',len(dosdata)-1,ene,doslines[0]
    
            for colum in range(0,int(n_orbit_page[page])+1): # 各ページごとに読み込む軌道数
    
                i_atom=int(index_atom_page_colum[page,colum])
                i_num=int(index_orbit_page_colum[page,colum])   # local_num
    
                if options.debug and colum == 0 and ene == 1:
                    print "page, colum, i_atom, data = ", page,colum, i_atom,float(doslines[colum])
    
                ###############################################
                data[i_atom,i_num, ene] = float(doslines[colum])
                ###############################################
    #           print "%12.8f  " %( data[i_atom, i_num, ene] ),
    
    #       print ""
    
    
    ## ##### TEST PRINT
    if options.deep:
        page=0
        for dosname in ls:
            page += 1
        
            f = open(dosname)
            dosfile = f.read()
            f.close
        
            dosdata = dosfile.split('\n')
            print ""
            print "i_atom, num, data[i_atom,num,ene]"
            for i in range(3,len(dosdata)-1):  # エネルギー分割
                ene=i-2
                for colum in range(0,int(n_orbit_page[page])+1):  # カラム分割( total-DOS も含む)
                    i_atom=int(index_atom_page_colum[page,colum])
                    num=int(index_orbit_page_colum[page,colum])
                   #print "%d %d %12.8f   " %( i_atom, num, data[i_atom, num, ene] ),
                    print "%12.8f   " %(data[i_atom, num, ene] ),
                print ""
    
    
    
    ######################
    #
    # output data
    #
    # data [atom,num,NENRG]
    # data [nfiles+1,n_total_orbit+1,NENRG+1]
    
    if options.test:
        print ""
        print "WRITEDATA"
        print ""
    
    if options.debug:
        print ""
        print "GNUPLOT FORMAT FILE:"
    
    if TOTALDOS_FLAG:
        start=0
    else:
        start=1
    
    for atom in range(start,natom+1):
        gnuplot = open(cname+'.gnuplot_dos'+str(atom)+unit+str(spin),'w')
    
        ###################### print HEADER
        if options.debug:
            print "  ",cname+'.gnuplot_dos'+str(atom)+unit+str(spin)
    
        print >> gnuplot, "#  BAND"
        print >> gnuplot, "#EF= ",EF,"  NATOM= ",natom,"  ATOM= ",atom,"   NORBIT=",int(norbit[atom])
        print >> gnuplot, "# ENERGY  ",
    
        for orbit in range(1,int(norbit[atom])+1):  # atom=0 (total-DOS) の時は norbit[atom]=1
            orbit_num = int(index_local_orbit[atom,orbit])
            index_num = int(indexnum[atom,int(orbit_num)])
    
            if options.test:
                print "norbit[atom], orbit,orbit_num, indexnum[atom,orbit] = ",
                print int(norbit[atom]), atom, orbit, int(orbit_num),
                print int(index_num) ,indexname[int(index_num)]
    
           #print >> gnuplot,"%d:%s  " %(atom,indexnum[atom,orbit_num]),
            print >> gnuplot,"%d:%s  " %(atom,indexname[int(index_num)]),
    
        print >> gnuplot, ""
        print >> gnuplot, ""
    
        #######################################
        if options.test:
            print ""
    
        for nen in range(1,NENRG+1):
            if options.FLAG_EF:
                E = float(data[atom,0,nen]) - float(EF)
            else:
                E = float(data[atom,0,nen])
    
            if TOTALDOS_FLAG:
                data[1,0,nen] = data[0,0,nen]
    
            print >> gnuplot, "%10.6f" %(E),
    
    #       if options.test:
    #           print "atom,"
    
            for orbit in range(1,int(norbit[atom])+1):  # 原子種ごとの軌道番号
    
                if options.deep:
                    print "atom,norbit[atom],orbit = ",atom,int(norbit[atom]),orbit
    
                num=orbit  # 原子種ごとの軌道番号
               #print "atom,orbit,indexnum[atom,orbit] = ",atom,orbit,int(indexnum[atom,orbit])
    
                print >> gnuplot, "%12.8f" %(data[atom,num,nen]),
            print >> gnuplot, ""
        print >> gnuplot, ""
        gnuplot.close()
    
        if options.test:
            print ""
    
    if options.debug:
        print ""
    
###################################### END SPIN roop ##########################################
