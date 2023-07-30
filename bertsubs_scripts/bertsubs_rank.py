# Copyright 2023 Jiaoyan Chen. All rights reserved.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from deeponto.onto import Ontology
from deeponto.utils import FileUtils
from yacs.config import CfgNode
from deeponto.subs.bertsubs import BERTSubsInterPipeline, DEFAULT_CONFIG_FILE_INTER

# Inputs
config = CfgNode(FileUtils.load_file(DEFAULT_CONFIG_FILE_INTER))
USE_TRAIN_MAPPINGS = True
data_dir = 'bio-ml/ncit-doid'
config.src_onto_file = f"{data_dir}/ncit.owl"
config.tgt_onto_file = f"{data_dir}/doid.owl"
test_cands_file = f"{data_dir}/refs_subs/test.cands.tsv"
train_file = f"{data_dir}/refs_subs/train.tsv"
config.prompt.prompt_type = 'isolated'  # isolated, traversal, path
config.test_type = 'evaluation'
config.subsumption_type = 'named_class'
config.tgt_label_property = ['http://www.w3.org/2000/01/rdf-schema#label']
config.src_label_property = ['http://www.w3.org/2000/01/rdf-schema#label']

# Parse the testing candidate file and training file
test_lines = list()
test_cands = FileUtils.read_table(test_cands_file)
for _, dp in test_cands.iterrows():
    src_class_iri = dp["SrcEntity"]
    tgt_class_iri = dp["TgtEntity"]
    tgt_cands = eval(dp["TgtCandidates"])
    cands_list = list(tgt_cands)
    cands_list.remove(tgt_class_iri)
    s = '%s,%s,%s' % (src_class_iri, tgt_class_iri, ','.join(cands_list))
    test_lines.append(s)
config.test_subsumption_file = f"{data_dir}/refs_subs/test_subsumptions.csv"
with open(config.test_subsumption_file, 'w') as f:
    for line in test_lines:
        f.write('%s\n' % line)

if USE_TRAIN_MAPPINGS:
    train_lines = list()
    train_data = FileUtils.read_table(train_file)
    for _, dp in train_data.iterrows():
        src_class_iri = dp["SrcEntity"]
        tgt_class_iri = dp["TgtEntity"]
        s = '%s,%s' % (src_class_iri, tgt_class_iri)
        train_lines.append(s)
    config.train_subsumption_file = f"{data_dir}/refs_subs/train_subsumptions.csv"
    with open(config.train_subsumption_file, 'w') as f:
        for line in train_lines:
            f.write('%s\n' % line)

# BERTSubs evaluation
src_onto = Ontology(owl_path=config.src_onto_file)
tgt_onto = Ontology(owl_path=config.tgt_onto_file)
inter_pipeline = BERTSubsInterPipeline(src_onto=src_onto, tgt_onto=tgt_onto, config=config)
