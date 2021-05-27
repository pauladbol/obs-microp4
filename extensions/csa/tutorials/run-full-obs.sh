sudo mn -c

${UP4ROOT}/build/p4c-msa -I ${UP4ROOT}/build/p4include -o full_obs_ipv4.json full_obs_ipv4.up4
${UP4ROOT}/build/p4c-msa -I ${UP4ROOT}/build/p4include -o full_obs_ipv6.json full_obs_ipv6.up4

${UP4ROOT}/build/p4c-msa --target-arch v1model -I ${UP4ROOT}/build/p4include  -l full_obs_ipv4.json,full_obs_ipv6.json full_obs.up4

../p4c-compile.sh full_obs_v1model.p4

#!/bin/bash
bold=$(tput bold)
normal=$(tput sgr0)
#/home/microp4/ microp4/extensions/csa/msa-examples/bmv2/mininet/tutorials/obs_example_v1model_sw.py
PROGRAMS="full_obs_v1model"
# extensions/csa/tutorials/exercise-3/obs_example_v1model_sw.py
BMV2_MININET_PATH=${UP4ROOT}/extensions/csa/tutorials/one-big-switch
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