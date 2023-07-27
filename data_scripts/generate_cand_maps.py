from deeponto.onto import Ontology
from deeponto.align.mapping import *
from deeponto.align.bertmap import BERTMapPipeline
import click
import pandas as pd
from sklearn.model_selection import train_test_split

@click.command()
@click.option("-t", "--task_name", type=str)
@click.option("-s", "--for_subsumption", type=bool)
def generate_candidate_mappings(task_name: str, for_subsumption: bool):
    src_onto_name, tgt_onto_name = task_name.split("-")
    if "." in tgt_onto_name:
        src_onto_name = src_onto_name + "." + tgt_onto_name.split(".")[-1]
    src_onto = Ontology(f"{task_name}/{src_onto_name}.owl")
    tgt_onto = Ontology(f"{task_name}/{tgt_onto_name}.owl")
    refs_equiv = ReferenceMapping.read_table_mappings(f"{task_name}/refs_equiv/full.tsv")
    refs_subs = ReferenceMapping.read_table_mappings(f"{task_name}/refs_subs/train.tsv")
    refs_subs += ReferenceMapping.read_table_mappings(f"{task_name}/refs_subs/test.tsv")
    refs_full = refs_subs if for_subsumption else refs_equiv
    if for_subsumption:
        refs_test = ReferenceMapping.read_table_mappings(f"{task_name}/refs_subs/test.tsv")
        result_path = f"{task_name}/refs_subs/test.cands.tsv"
    else:
        refs_test = ReferenceMapping.read_table_mappings(f"{task_name}/refs_equiv/test.tsv")
        result_path = f"{task_name}/refs_equiv/test.cands.tsv"
    config = BERTMapPipeline.load_bertmap_config()
    neg_gen = NegativeCandidateMappingGenerator(
        src_onto, tgt_onto, refs_full,
        config.annotation_property_iris,
        Tokenizer.from_pretrained(config.bert.pretrained_path),
        for_subsumption=for_subsumption
    )
    results = []
    for test_map in refs_test:
        valid_tgts, stats = neg_gen.mixed_sample(test_map, idf=50, neighbour=50)
        print(f"STATS for {test_map}:\n{stats}")
        results.append((test_map.head, test_map.tail, valid_tgts))
    results = pd.DataFrame(results, columns=["SrcEntity", "TgtEntity", "TgtCandidates"])
    results.to_csv(result_path, sep="\t", index=False)

if __name__ == "__main__":
    generate_candidate_mappings()
