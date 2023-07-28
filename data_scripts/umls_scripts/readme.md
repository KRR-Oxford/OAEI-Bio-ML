Data scripts to generate mappings from UMLS and select the SCUIs to keep based on semantic types (or STYs).

**Main scripts**: `run_scripts_prune_SCUIs_and_maps.py` generates the selected SCUIs based on different settings (pre-defined in `get_SCUI_in_onto_from_STYs.py`) and filters the mappings from UMLS (implemented in `get_mappings.py`).

**Get mappings and STY distributions**: A separate script to get all mappings, regardless of semantic types, is in `umls_mrconso_with_CUI_and_STY.py`, where it also displays the CUI and STY of each mapping  (only the last STY is displayed if there are multiple STYs). It also outputs the distribution of STYs overlapped in every two ontologies matched in UMLS (which are used to choose the representative STYs across the ontologies, SNOMED CT, FMA, and NCI).

**Get ontology coverage statistics**: `cal_percent_onto_in_UMLS.py` and `check_snomed_classes_orig_vs_owl.py` calculate the percentage of each selected full ontologies covered by UMLS, and the number of classes in SNOMED CT (the one processed by snomed-owl-toolkit vs. the original one), respectively.
