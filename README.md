# OAEI :: Bio-ML: A ML-friendly Biomedical track for Equivalence and Subsumption Matching

This repository provides dataset pointer and evaluation scripts for the Bio-ML Track of the OAEI. 

> Example code of OM evaluation is available at `bertmap_scripts/bertmap_eval.ipynb`. 

## Links

- **Official OAEI Page**: <https://www.cs.ox.ac.uk/isg/projects/ConCur/oaei/index.html> (Results will be published on the OAEI webpage.)
- **Instructions of Use**: <https://krr-oxford.github.io/DeepOnto/bio-ml/> (For a comprehensive information of Bio-ML. please carefully read this documentation.)
- **Resource Paper**: <https://arxiv.org/abs/2205.03447>
- **Dataset Download**:
    - **OAEI 2023**: to be released
    - **OAEI 2022**: <https://zenodo.org/record/6946466>

## Data Statistics

### OAEI 2023

For the OAEI 2023 version, we add in **locality modules** ([code](https://github.com/ernestojimenezruiz/logmap-matcher/blob/master/src/test/java/uk/ac/ox/krr/logmap2/test/oaei/CreateModulesForBioMLTrack.java)) for each entity in the pruned ontologies to provide additional context. The added entities are marked as **not used in alignment** through the annotation property `use_in_alignment` with a value of `false`.

The changes compared to the previous version are reflected in the `+` numbers of ontology classes. 

<center>
<small>

| Source | Task        | Category | #SrcCls | #TgtCls | #TgtCls (subs) | #Ref (equiv) | #Ref (subs)  |
|--------|:-----------:|:--------:|:-------:|:-------:|:--------------:|:------------:|:------------:|
| Mondo  | OMIM-ORDO   | Disease  | 9,648 (+6)      | 9,275 (+437)    | 9,271 (+536) | 3,721 | 103   |
| Mondo  | NCIT-DOID   | Disease  | 15,762 (+8,927) | 8,465 (+17)     | 5,722 (+609) | 4,684 | 3,339 | 
| UMLS   | SNOMED-FMA  |Body | 34,418 (+10,236)|88,955 (+24,229)|88,648 (+20,081)| 7,256  | 5,506    |
| UMLS   | SNOMED-NCIT |Pharm| 29,500 (+13,455)|22,136 (+6,886) |20,113 (+7,651) | 5,803  | 4,225    |
| UMLS   | SNOMED-NCIT | Neoplas  | 22,971 (+11,700) | 20,247 (+6291) | 20,113 (+6,323) | 3,804 | 213|

</small>
</center>


### OAEI 2022

Statistics for the original version of Bio-ML, used in the OAEI-2022.

In the **Category** column, *"Disease"* indicates that the Mondo data are mainly about disease concepts, while *"Body"*, *"Pharm"*, and *"Neoplas"* denote semantic types of *"Body Part, Organ, or Organ Components"*, *"Pharmacologic Substance*"*, and *"Neoplastic Process"* in UMLS, respectively.

Note that each subsumption matching task is constructed from an equivalence matching task subject to target side class deletion, therefore `#TgtCls (subs)` is different with `#TgtCls`.

<center>
<small>

| Source | Task        | Category | #SrcCls | #TgtCls | #TgtCls (subs) | #Ref (equiv) | #Ref (subs) |
|--------|:-----------:|:--------:|:-------:|:-------:|:--------------:|:------------:|:-----------:|
| Mondo  | OMIM-ORDO   | Disease  | 9,642   | 8,838   | 8,735          | 3,721        | 103         |
| Mondo  | NCIT-DOID   | Disease  | 6,835   | 8,448   | 5,113          | 4,684        | 3,339       | 
| UMLS   | SNOMED-FMA  | Body     | 24,182  | 64,726  | 59,567         | 7,256        | 5,506       |
| UMLS   | SNOMED-NCIT | Pharm    | 16,045  | 15,250  | 12,462         | 5,803        | 4,225       |
| UMLS   | SNOMED-NCIT | Neoplas  | 11,271  | 13,956  | 13,790         | 3,804        | 213         |

</small>
</center>



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