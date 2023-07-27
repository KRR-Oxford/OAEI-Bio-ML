#!/bin/bash
set -e

data_dir="..." # data dir to oaei-2023
task_name=$1  # ncit-doid, omim-ordo, snomed-fma.body, snomed-ncit.neoplas, snomed-ncit.pharm
IFS='-' read -ra onto_names <<< "$task_name"
src_onto=${onto_names[0]}
tgt_onto=${onto_names[1]}
# fix ontology names if they are from UMLS
IFS="." read -ra topic <<< "${onto_names[1]}"
if [ "${#topic[@]}" -eq 2 ]; then
    src_onto="${src_onto}.${topic[1]}"
fi
src_onto="${data_dir}/${task_name}/${src_onto}.owl"
tgt_onto="${data_dir}/${task_name}/${tgt_onto}.owl"
echo $src_onto $tgt_onto

client=matching-eval-client-latest.jar  # this needs to be downloaded from the MELT platform
tool_path="./${tool_name}/${tool_name}.tar.gz"
result_path="..."  # path to the OM tool in .tar.gz
sudo mkdir -p $result_path
sudo java -Xms500M -Xmx15G -DentityExpansionLimit=100000000 -jar $client -s $tool_path --local-testcase $src_onto $tgt_onto test_map_to_skip_melt_eval.rdf -r $result_path 2> $result_path/err.log > $result_path/out.log
# copy the alignment.rdf out
sudo mv ${result_path}/LocalTrack_1.0/Local+TC/.%*/systemAlignment.rdf ${result_path}/systemAlignment.rdf
