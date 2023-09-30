import argparse
import gensim
import datetime
import re
import pandas as pd
from ontology import MyOntology

import numpy as np
from nltk import word_tokenize
from sklearn.utils import shuffle
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression

parser = argparse.ArgumentParser()
parser.add_argument('--src_onto_file', type=str, default='../bertsubs_scripts/bio-ml/ncit-doid/ncit.owl')
parser.add_argument('--tgt_onto_file', type=str, default='../bertsubs_scripts/bio-ml/ncit-doid/doid.owl')
parser.add_argument('--eval_subsumption_file', type=str, default='../bertsubs_scripts/bio-ml/ncit-doid/refs_subs/test.cands.tsv')
parser.add_argument('--train_mapping_file', type=str, default='None', help='../bertsubs_scripts/bio-ml/ncit-doid/refs_subs/train.tsv')
parser.add_argument('--src_label_property', type=str, default='http://www.w3.org/2000/01/rdf-schema#label')
parser.add_argument('--tgt_label_property', type=str, default='http://www.w3.org/2000/01/rdf-schema#label')
parser.add_argument('--train_pos_dup', type=int, default=2)
parser.add_argument('--train_neg_dup', type=int, default=2)
parser.add_argument('--word2vec_embedding_file', type=str, default='/home/jiaoyan/w2v_model/enwiki_model/word2vec_gensim',
                    help=', ../bertsubs_scripts/bio-ml/ncit-doid/owl2vec')
parser.add_argument('--classifier', type=str, default='rf', help='rf,mlp,lr')
FLAGS, unparsed = parser.parse_known_args()


def pre_process_label(input_label):
    text = ' '.join([re.sub(r'https?:\/\/.*[\r\n]*', '', w, flags=re.MULTILINE) for w in input_label.lower().split()])
    tokens = word_tokenize(text)
    return [token.lower() for token in tokens if token.isalpha()]


start_time = datetime.datetime.now()
iri_embedding = dict()
w2v = gensim.models.Word2Vec.load(FLAGS.word2vec_embedding_file)


def read_iri_embedding(onto):
    for c in onto.named_classes:
        word_vector = np.zeros(w2v.vector_size)
        n = 0
        if c.iri in onto.iri_label:
            for lab in onto.iri_label[c.iri]:
                words = pre_process_label(input_label=lab)
                for word in words:
                    if word in w2v.wv.index_to_key:
                        word_vector += w2v.wv.get_vector(word)
                        n += 1
        word_vector = word_vector / n if n > 0 else word_vector
        iri_embedding[c.iri] = word_vector


src_onto = MyOntology(onto_file=FLAGS.src_onto_file, label_property=[FLAGS.src_label_property])
read_iri_embedding(onto=src_onto)
src_subsumptions = [[subs[0].iri, subs[1].iri] for subs in src_onto.get_declared_named_class_subsumption()]

tgt_onto = MyOntology(onto_file=FLAGS.tgt_onto_file, label_property=[FLAGS.tgt_label_property])
read_iri_embedding(onto=tgt_onto)
tgt_subsumptions = [[subs[0].iri, subs[1].iri] for subs in tgt_onto.get_declared_named_class_subsumption()]

src_neg_subsumptions = list()
for subs in src_subsumptions:
    c1 = subs[0]
    for _ in range(FLAGS.train_neg_dup):
        neg_c = src_onto.get_negative_sample(subclass_str=c1, subsumption_type='named class')
        src_neg_subsumptions.append([c1, neg_c])
src_pos_subsumptions = FLAGS.train_pos_dup * src_subsumptions
print('src positive subsumptions: %d' % len(src_pos_subsumptions))
print('src negative subsumptions: %d' % len(src_neg_subsumptions))

tgt_neg_subsumptions = list()
for subs in tgt_subsumptions:
    c1 = subs[0]
    for _ in range(FLAGS.train_neg_dup):
        neg_c = tgt_onto.get_negative_sample(subclass_str=c1, subsumption_type='named class')
        tgt_neg_subsumptions.append([c1, neg_c])
tgt_pos_subsumptions = FLAGS.train_pos_dup * tgt_subsumptions
print('tgt positive subsumptions: %d' % len(tgt_pos_subsumptions))
print('tgt negative subsumptions: %d' % len(tgt_neg_subsumptions))

semi_pos_subsumptions, semi_neg_subsumptions = list(), list()
if not FLAGS.train_mapping_file == 'None':
    with open(FLAGS.train_mapping_file) as f:
        for line in f.readlines()[1:]:
            tmp = line.strip().split('\t')
            subcls, supcls = tmp[0], tmp[1]
            for _ in range(FLAGS.train_pos_dup):
                semi_pos_subsumptions.append([subcls, supcls])
            for _ in range(FLAGS.train_neg_dup):
                neg_c = tgt_onto.get_negative_sample(subclass_str=supcls, subsumption_type='named class')
                semi_neg_subsumptions.append([subcls, neg_c])
print('semi positive subsumptions: %d' % len(semi_pos_subsumptions))
print('semi negative subsumptions: %d' % len(semi_neg_subsumptions))


subsumption_vector = lambda subsumption: np.concatenate((iri_embedding[subsumption[0]], iri_embedding[subsumption[1]]))
pos_X = [subsumption_vector(s) for s in src_pos_subsumptions + tgt_pos_subsumptions + semi_pos_subsumptions]
pos_y = np.ones((len(pos_X)))
pos_X = np.array(pos_X)
neg_X = [subsumption_vector(s) for s in src_neg_subsumptions + tgt_neg_subsumptions + semi_neg_subsumptions]
neg_y = np.zeros((len(neg_X)))
neg_X = np.array(neg_X)
X, y = np.concatenate((pos_X, neg_X)), np.concatenate((pos_y, neg_y))
X, y = shuffle(X, y, random_state=0)

if FLAGS.classifier == 'rf':
    model = RandomForestClassifier(n_estimators=50)
elif FLAGS.classifier == 'mlp':
    model = MLPClassifier(max_iter=1000, hidden_layer_sizes=200)
else:
    model = LogisticRegression(random_state=0)
model.fit(X, y)

end_time = datetime.datetime.now()
print('data pre-processing and training cost %.1f minutes' % ((end_time - start_time).seconds / 60))


start_time = datetime.datetime.now()
na_vals = pd.io.parsers.readers.STR_NA_VALUES.difference({"NULL", "null", "n/a"})
sep = "\t" if FLAGS.eval_subsumption_file.endswith(".tsv") else ","
test_cands = pd.read_csv(FLAGS.eval_subsumption_file, sep=sep, na_values=na_vals, keep_default_na=False)

MRR_sum, hits1_sum, hits5_sum, hits10_sum = 0, 0, 0, 0
MRR, Hits1, Hits5, Hits10 = 0, 0, 0, 0
for k, dp in test_cands.iterrows():
    subclass = dp["SrcEntity"]
    gt = dp["TgtEntity"]
    cands = eval(dp["TgtCandidates"])
    candidates = list(cands)
    if gt not in candidates:
        candidates.append(gt)
    candidate_subsumptions = [[subclass, c] for c in candidates]
    candidate_scores = np.zeros(len(candidate_subsumptions))
    V = np.array([subsumption_vector(candidate_subsumption) for candidate_subsumption in candidate_subsumptions])
    P = model.predict_proba(V)[:, 1]
    sorted_indexes = np.argsort(P)[::-1]
    sorted_classes = list()
    for j in sorted_indexes:
        sorted_classes.append(candidates[j])
    rank = sorted_classes.index(gt) + 1

    MRR_sum += 1.0 / rank
    hits1_sum += 1 if gt in sorted_classes[:1] else 0
    hits5_sum += 1 if gt in sorted_classes[:5] else 0
    hits10_sum += 1 if gt in sorted_classes[:10] else 0
    num = k + 1
    MRR, Hits1, Hits5, Hits10 = MRR_sum / num, hits1_sum / num, hits5_sum / num, hits10_sum / num
    if num % 200 == 0:
        print('\n%d tested, MRR: %.3f, Hits@1: %.3f, Hits@5: %.3f, Hits@10: %.3f\n' % (num, MRR, Hits1, Hits5, Hits10))

print('\nAll tested, MRR: %.3f, Hits@1: %.3f, Hits@5: %.3f, Hits@10: %.3f\n' % (MRR, Hits1, Hits5, Hits10))
end_time = datetime.datetime.now()
print('Evaluation costs %.1f minutes' % ((end_time - start_time).seconds / 60))
