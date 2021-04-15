#!/bin/bash
bold=$(tput bold)
normal=$(tput sgr0)
#/home/microp4/microp4/extensions/csa/msa-examples/bmv2/mininet/tutorials/obs_example_v1model_sw.py
PROGRAMS="obs_example_v1model"
# extensions/csa/tutorials/exercise-3/obs_example_v1model_sw.py
BMV2_MININET_PATH=${UP4ROOT}/extensions/csa/tutorials/exercise-3/
BMV2_SIMPLE_SWITCH_BIN=${UP4ROOT}/extensions/csa/msa-examples/bmv2/targets/simple_switch/simple_switch

P4_MININET_PATH=${UP4ROOT}/extensions/csa/msa-examples/bmv2/mininet

for prog in $PROGRAMS; do
    echo -e "${bold}\n*********************************" 
    echo -e "Running Tutorial program: ${prog}${normal}" 
    sudo bash -c "export P4_MININET_PATH=${P4_MININET_PATH} ;  \
      $BMV2_MININET_PATH/${prog}_sw.py --behavioral-exe $BMV2_SIMPLE_SWITCH_BIN \
      --num-hosts 4 --json ./${prog}.json"
    echo -e "*********************************\n${normal}" 
done
