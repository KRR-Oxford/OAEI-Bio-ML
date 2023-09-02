from deeponto.onto import Ontology
from deeponto.align.mapping import *
import click
from deeponto.utils import read_table

@click.command()
@click.option("-t", "--task_name", type=str)
def generate_statistics(task_name: str):
    src_onto_name, tgt_onto_name = task_name.split("-")
    if "." in tgt_onto_name:
        src_onto_name = src_onto_name + "." + tgt_onto_name.split(".")[-1]
    src_onto = Ontology(f"{task_name}/{src_onto_name}.owl")
    tgt_onto = Ontology(f"{task_name}/{tgt_onto_name}.owl")
    refs_equiv = len(ReferenceMapping.read_table_mappings(f"{task_name}/refs_equiv/full.tsv"))
    refs_subs = len(ReferenceMapping.read_table_mappings(f"{task_name}/refs_subs/train.tsv"))
    refs_subs += len(read_table(f"{task_name}/refs_subs/test.cands.tsv"))
    stats = {
        "task": task_name,
        "#SrcCls": len(src_onto.owl_classes),
        "#TgtCls": len(tgt_onto.owl_classes),
        "#RefsEquiv": refs_equiv,
        "#RefsSubs": refs_subs
    }
    print(stats)

if __name__ == "__main__":
    generate_statistics()