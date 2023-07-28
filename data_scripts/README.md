### Dataset Construction Scripts

- `umls_scripts`: related to UMLS reference mapping and semantic type extraction.  
- `generate_refs_subs.py`: used to generate reference subsumption mappings from a given set of reference equivalence mappings.
- `generate_cand_maps.py`: used to generate candidate mappings for a given set of reference mappigns.
for creating subsumption mappings and canddiate mappings.

The above scripts are related to the OAEI 2022 version and cannot be directly used for the OAEI 2023 version because it has enriched entities that should not be used in alignment.

### Dataset Display Scripts

- `om_statistics.py`: used to display statistics about an OM pair.
