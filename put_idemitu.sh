#!/bin/bash -
#===============================================================================
#
#          FILE: put_t2k.sh
#
#         USAGE: ./put_t2k.sh
#
#   DESCRIPTION:
#
#       OPTIONS: ---
#  REQUIREMENTS: ---
#          BUGS: ---
#         NOTES: ---
#        AUTHOR: Kengo NAKADA (), kengo.nakada@gmail.com
#  ORGANIZATION:
#       CREATED: 2021/05/28 20:29
#      REVISION:  ---
#===============================================================================

set -o nounset                              # Treat unset variables as an error
rsync -avz -e ssh ./ idemitu:~/install/sae/

