from deeponto.onto import Ontology
from deeponto.align.bertmap import BERTMapPipeline, DEFAULT_CONFIG_FILE

config = BERTMapPipeline.load_bertmap_config(DEFAULT_CONFIG_FILE)

data_dir = ...  # path to the OAEI data directory
src_onto_name = ...
tgt_onto_name = ...
src_onto = Ontology(f"{data_dir}/{src_onto_name}.owl")
tgt_onto = Ontology(f"{data_dir}/{tgt_onto_name}.owl")

config.model = "bertmap" 
# config.bert.resume_training = None  # or True, uncomment if training is interrupted
config.global_matching.enabled = True
config.global_matching.for_oaei = True

bertmap = BERTMapPipeline(src_onto, tgt_onto, config)
# bertmap.bert.train(bertmap.bert_resume_training)  # uncomment if training is interrupted
