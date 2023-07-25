# Copyright 2023 Yuan He. All rights reserved.

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
from deeponto.align.bertmap import BERTMapPipeline, DEFAULT_CONFIG_FILE
from deeponto.utils import FileUtils
import enlighten
from typing import List
import pandas as pd

def bertmap_predict(bertmap: BERTMapPipeline, src_class_labels: List[str], tgt_class_labels: List[str]):
    bertmap_score = bertmap.mapping_predictor.bert_mapping_score(src_class_labels, tgt_class_labels)
    bertmaplt_score = bertmap.mapping_predictor.edit_similarity_mapping_score(src_class_labels, tgt_class_labels)
    return bertmap_score, bertmaplt_score

def bertmap_ranking(
    bertmap: BERTMapPipeline,
    test_cands_file: str,
    src_annotation_index: dict,
    tgt_annotation_index: dict
):
    test_cands = FileUtils.read_table(test_cands_file)
    enlighten_manager = enlighten.get_manager()
    progress_bar = enlighten_manager.counter(total=len(test_cands), desc="Mapping Prediction", unit="per src class")
    bertmap_results = []
    bertmaplt_results = []

    for _, dp in test_cands.iterrows():
        src_class_iri = dp["SrcEntity"]
        tgt_class_iri = dp["TgtEntity"]
        tgt_cands = eval(dp["TgtCandidates"])
        temp_progress_bar = enlighten_manager.counter(
            total=len(tgt_cands), desc="Mapping Prediction", unit="per tgt candidate", leave=False
        )
        cur_bertmap_results = (src_class_iri, tgt_class_iri, [])
        cur_bertmaplt_results = (src_class_iri, tgt_class_iri, [])
        for tgt_cand_iri in tgt_cands:
            bertmap_score, bertmaplt_score = bertmap_predict(
                bertmap, src_annotation_index[src_class_iri], tgt_annotation_index[tgt_cand_iri]
            )
            cur_bertmap_results[2].append((tgt_cand_iri, bertmap_score))
            cur_bertmaplt_results[2].append((tgt_cand_iri, bertmaplt_score))
            temp_progress_bar.update()
        bertmap_results.append(cur_bertmap_results)
        bertmaplt_results.append(cur_bertmaplt_results)
        progress_bar.update()
        pd.DataFrame(bertmap_results, columns=["SrcEntity", "TgtEntity", "TgtCandidates"]).to_csv("bertmap.rank.tsv", index=False, sep="\t")
        pd.DataFrame(bertmaplt_results, columns=["SrcEntity", "TgtEntity", "TgtCandidates"]).to_csv("bertmaplt.rank.tsv", index=False, sep="\t")
        temp_progress_bar.close()

config = BERTMapPipeline.load_bertmap_config(DEFAULT_CONFIG_FILE)

data_dir = ...  # path to the OAEI data directory
src_onto_name = ...
tgt_onto_name = ...
src_onto = Ontology(f"{data_dir}/{src_onto_name}.owl")
tgt_onto = Ontology(f"{data_dir}/{tgt_onto_name}.owl")

config.model = "bertmap" 
# config.bert.resume_training = None  # or True, uncomment if training is interrupted
config.global_matching.enabled = False  # IMPORTANT! turn off global_matching 
config.global_matching.for_oaei = True

bertmap = BERTMapPipeline(src_onto, tgt_onto, config)

test_cands_file = f"{data_dir}/refs_equiv/test.cands.tsv"
bertmap_ranking(
    bertmap, test_cands_file, bertmap.src_annotation_index, bertmap.tgt_annotation_index
)
