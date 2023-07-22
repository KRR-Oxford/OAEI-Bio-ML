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

from typing import List

from deeponto.align.bertmap import BERTMapPipeline
from deeponto.utils import FileUtils
import enlighten


def bertmap_predict(bertmap: BERTMapPipeline, src_class_labels: List[str], tgt_class_labels: List[str]):
    bertmap_score = bertmap.mapping_predictor.bert_mapping_score(src_class_labels, tgt_class_labels)
    # the bertmaplt score
    bertmaplt_score = bertmap.mapping_predictor.edit_similarity_mapping_score(src_class_labels, tgt_class_labels)
    return bertmap_score, bertmaplt_score


def bertmap_ranking(
    bertmap: BERTMapPipeline,
    test_cands_file: str,
    src_annotation_index: dict,
    tgt_annotation_index: dict,
    result_file: str,
):
    test_cands = FileUtils.read_table(test_cands_file)
    enlighten_manager = enlighten.get_manager()
    progress_bar = enlighten_manager.counter(total=len(test_cands), desc="Mapping Prediction", unit="per src class")
    result_dict = dict()

    for _, dp in test_cands.iterrows():
        src_class_iri = dp["SrcEntity"]
        tgt_class_iri = dp["TgtEntity"]
        tgt_cands = eval(dp["TgtCandidates"])
        temp_progress_bar = enlighten_manager.counter(
            total=len(tgt_cands), desc="Mapping Prediction", unit="per tgt candidate"
        )
        for tgt_cand_iri in tgt_cands:
            bertmap_score, bertmaplt_score = bertmap_predict(
                bertmap, src_annotation_index[src_class_iri], tgt_annotation_index[tgt_cand_iri]
            )
            result_dict[src_class_iri, tgt_class_iri][tgt_cand_iri] = (bertmap_score, bertmaplt_score)
            temp_progress_bar.update()

        progress_bar.update()

    FileUtils.save_file(result_dict, result_file)
