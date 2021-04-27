sudo mn -c

${UP4ROOT}/build/p4c-msa -I ${UP4ROOT}/build/p4include -o ipv4_s1.json ipv4_s1.up4
${UP4ROOT}/build/p4c-msa -I ${UP4ROOT}/build/p4include -o ipv4_s2.json ipv4_s2.up4
${UP4ROOT}/build/p4c-msa -I ${UP4ROOT}/build/p4include -o ipv6_s1.json ipv6_s1.up4
${UP4ROOT}/build/p4c-msa -I ${UP4ROOT}/build/p4include -o ipv6_s3.json ipv6_s3.up4

${UP4ROOT}/build/p4c-msa --target-arch v1model -I ${UP4ROOT}/build/p4include  -l ipv4_s1.json,ipv6_s1.json obs_s1.up4
${UP4ROOT}/build/p4c-msa --target-arch v1model -I ${UP4ROOT}/build/p4include  -l ipv4_s2.json obs_s2.up4
${UP4ROOT}/build/p4c-msa --target-arch v1model -I ${UP4ROOT}/build/p4include  -l ipv6_s3.json obs_s3.up4

../p4c-compile.sh obs_s1_v1model.p4
../p4c-compile.sh obs_s2_v1model.p4
../p4c-compile.sh obs_s3_v1model.p4

#!/bin/bash
bold=$(tput bold)
normal=$(tput sgr0)
#/home/microp4/microp4/extensions/csa/msa-examples/bmv2/mininet/tutorials/obs_example_v1model_sw.py
PROGRAMS="obs_example_v1model"
# extensions/csa/tutorials/exercise-3/obs_example_v1model_sw.py
BMV2_MININET_PATH=${UP4ROOT}/extensions/csa/tutorials/one-big-switch
BMV2_SIMPLE_SWITCH_BIN=${UP4ROOT}/extensions/csa/msa-examples/bmv2/targets/simple_switch/simple_switch

P4_MININET_PATH=${UP4ROOT}/extensions/csa/msa-examples/bmv2/mininet

echo -e "${bold}\n*********************************" 
echo -e "Running Tutorial program: obs_example_v1model${normal}" 
sudo bash -c "export P4_MININET_PATH=${P4_MININET_PATH} ;  \
  $BMV2_MININET_PATH/obs_example2_v1model_sw.py --behavioral-exe $BMV2_SIMPLE_SWITCH_BIN \
  --num-hosts 4 --json1 ./obs_s1_v1model.json --json2 ./obs_s2_v1model.json --json3 ./obs_s3_v1model.json"
echo -e "*********************************\n${normal}" 