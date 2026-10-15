#!/bin/csh -f


## set localmachine = terbium
##
## #set server_list=( 192.168.1.40 192.168.1.41 192.168.1.38 iridium b30511@thin.kudpc.kyoto-u.ac.jp ha8000 )
## #set server_list=( 192.168.1.51 192.168.1.40 192.168.1.41 192.168.1.38 iridium b30511@thin.kudpc.kyoto-u.ac.jp kashiwa.issp.u-tokyo.ac.jp )
##
## #set server_list=( 192.168.1.40 192.168.1.41 192.168.1.38 iridium b30511@thin.kudpc.kyoto-u.ac.jp kashiwa.issp.u-tokyo.ac.jp ha8000 )
## #set server_list=( 192.168.1.40 192.168.1.41 192.168.1.38 iridium b30511@thin.kudpc.kyoto-u.ac.jp kashiwa.issp.u-tokyo.ac.jp )
## #set server_list=( iridium 192.168.1.40 192.168.1.41 192.168.1.38 b30511@thin.kudpc.kyoto-u.ac.jp kashiwa.issp.u-tokyo.ac.jp )
##
## #set server_list=( iridium 192.168.1.40 192.168.1.41 192.168.1.43 192.168.1.38 b30511@thin.kudpc.kyoto-u.ac.jp f60138@login.hpc.cmc.osaka-u.ac.jp )
##
## #set server_list=( laurel iridium 192.168.1.40 192.168.1.41 192.168.1.42 192.168.1.43 192.168.1.44 192.168.1.38 )
##
## #set server_list=( antimony iridium 192.168.1.40 192.168.1.41 192.168.1.43 192.168.1.38 b30511@thin.kudpc.kyoto-u.ac.jp f60138@login.hpc.cmc.osaka-u.ac.jp )
##
## #set server_list=( 192.168.1.40 192.168.1.41 192.168.1.38 )
## #set server_list=( 192.168.1.40 192.168.1.41 192.168.1.38 iridium  ha8000 )
## #set server_list=( 192.168.1.40 192.168.1.38 )
##
## #set server_list=( 10.10.78.181 )
## set server_list=( 10.10.78.235 10.10.58.70)
##
## # 10.10.78.235 (neptunium)
## # 10.10.58.70 (fermium)
##
## if ( $#argv > 0 ) then
##     set server_list=( $argv[1] )
##     echo "server === $argv[1]"
## endif
##
## #set src_list=( hilapw1 vasp1 hilapw1 openmx1 aims1 rmcpot1 )
## set src_list=( hilapw1 vasp1 fdmnes1 ase1 wien2k1 openmx1 qe1 rmcpot1 gromacs1 cp2k1 gpaw1)
##
## foreach code1 ( $src_list )
##
##      set src1 = $home/$code1
##      if ( $IAM == $localmachine ) then
##        set src1 = $home/calculation/$code1
##      endif
##      echo "=================================================================="
##      echo "src1: $src1"
##
##      pushd ~/ >& /dev/null
##          foreach server ( $server_list )
##            echo ""
##            echo "====== $server ====="
##            rsync -avz -e ssh $src1/ ${server}:~/$code1/
##
##            if ( $IAM == $localmachine ) then #### PYTHON LIBRARY
##              rsync -avz -e ssh ~/lib/MY_PYTHON/ ${server}:~/lib/MY_PYTHON/
##            endif
##          end
##      popd
##      echo ""
##
## end
##
##
