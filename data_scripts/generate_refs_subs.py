from deeponto.onto import Ontology
from deeponto.align.mapping import *
import click
import pandas as pd
from sklearn.model_selection import train_test_split

@click.command()
@click.option("-t", "--task_name", type=str)
def generate_subsumption_mappings(task_name: str):
    src_onto_name, tgt_onto_name = task_name.split("-")
    if "." in tgt_onto_name:
        src_onto_name = src_onto_name + "." + tgt_onto_name.split(".")[-1]
    src_onto = Ontology(f"{task_name}/{src_onto_name}.owl")
    tgt_onto = Ontology(f"{task_name}/{tgt_onto_name}.owl")
    refs_equiv = ReferenceMapping.read_table_mappings(f"{task_name}/refs_equiv/full.tsv")
    subs_gen = SubsFromEquivMappingGenerator(
        src_onto, tgt_onto, refs_equiv, 
        subs_generation_ratio=1,  # generate 1 subsumption mapping for each equivalence mapping
        delete_used_equiv_tgt_class=False  # disable target class deletion 
    )
    subs_df = pd.DataFrame(subs_gen.subs_from_equivs, columns=["SrcEntity", "TgtEntity", "Score"])
    train, test = train_test_split(subs_df, test_size=0.7)
    train.to_csv(f"{task_name}/refs_subs/train.tsv", sep="\t", index=False)
    test.to_csv(f"{task_name}/refs_subs/test.tsv", sep="\t", index=False)

if __name__ == "__main__":
    generate_subsumption_mappings()
