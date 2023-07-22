# OAEI :: Bio-ML: A ML-friendly Biomedical track for Equivalence and Subsumption Matching

This repository provides dataset pointer and evaluation protocol for the Bio-ML Track of the OAEI.


## Links

- **Official OAEI Page**: <https://www.cs.ox.ac.uk/isg/projects/ConCur/oaei/index.html>
- **Instructions of Use**: <https://krr-oxford.github.io/DeepOnto/bio-ml/>
- **Resource Paper**: <https://arxiv.org/abs/2205.03447>
- **Dataset Download**:
    - **OAEI 2023**: to be released
    - **OAEI 2022**: <https://zenodo.org/record/6946466>

## Data Statistics

### OAEI 2023
### OAEI 2022

<center>
<small>

| Source | Task        | Category | #SrcCls | #TgtCls | #TgtCls (subs) | #Ref (equiv) | #Ref (subs) |
|--------|:-----------:|:--------:|:-------:|:-------:|:--------------:|:------------:|:-----------:|
| Mondo  | OMIM-ORDO   | Disease  | 9,642   | 8,838   | 8,735          | 3,721        | 103         |
| Mondo  | NCIT-DOID   | Disease  | 6,835   | 8,848   | 5,113          | 4,684        | 3,339       | 
| UMLS   | SNOMED-FMA  | Body     | 24,182  | 64,726  | 59,567         | 7,256        | 5,506       |
| UMLS   | SNOMED-NCIT | Pharm    | 16,045  | 15,250  | 12,462         | 5,803        | 4,225       |
| UMLS   | SNOMED-NCIT | Neoplas  | 11,271  | 13,956  | 13,790         | 3,804        | 213         |

</small>
</center>

| Source | Task        | Category | #Classes      | #RefMaps (subs)  |
|--------|:-----------:|:--------:|:-------------:|:----------------:|
| Mondo  | OMIM-ORDO   | Disease  | 9,642-8,735   | 103              | 
| Mondo  | NCIT-DOID   | Disease  | 6,835-5,113   | 3,339            | 
| UMLS   | SNOMED-FMA  | Body     | 24,182-59,567 | 5,506            | 
| UMLS   | SNOMED-NCIT | Pharm    | 16,045-12,462 | 4,225            | 
| UMLS   | SNOMED-NCIT | Neoplas  | 11,271-13,790 | 213              | 
## Citation

```
@inproceedings{he2022machine,
  title={Machine Learning-Friendly Biomedical Datasets for Equivalence and Subsumption Ontology Matching},
  author={He, Yuan and Chen, Jiaoyan and Dong, Hang and Jim{\'e}nez-Ruiz, Ernesto and Hadian, Ali and Horrocks, Ian},
  booktitle={The Semantic Web--ISWC 2022: 21st International Semantic Web Conference, Virtual Event, October 23--27, 2022, Proceedings},
  pages={575--591},
  year={2022},
  organization={Springer}
}
```