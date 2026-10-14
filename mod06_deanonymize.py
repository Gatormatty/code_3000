import pandas as pd

def load_data(anonymized_path, auxiliary_path):
    """
    Load anonymized and auxiliary datasets.
    """
    anon = pd.read_csv(anonymized_path)
    aux = pd.read_csv(auxiliary_path)
    return anon, aux


def link_records(anon_df, aux_df):
    """
    Attempt to link anonymized records to auxiliary records
    using exact matching on quasi-identifiers.

    Returns a DataFrame with columns:
      anon_id, matched_name
    containing ONLY uniquely matched records.
    """
    exclude_cols = {'anon_id', 'name', 'scrambled_name', 'id', 'Unnamed: 0'}
    qids = [col for col in anon_df.columns if col in aux_df.columns and col not in exclude_cols]
    
    anon_counts = anon_df.groupby(qids).size().reset_index(name='anon_count')
    aux_counts = aux_df.groupby(qids).size().reset_index(name='aux_count')
    
    merged = pd.merge(anon_df, aux_df, on=qids, how='inner')
    
    merged = merged.merge(anon_counts, on=qids).merge(aux_counts, on=qids)
    
    unique_matches = merged[(merged['anon_count'] == 1) & (merged['aux_count'] == 1)]
    
    name_col = 'name' if 'name' in aux_df.columns else [c for c in aux_df.columns if c not in qids and c != 'anon_id'][0]
    
    result = unique_matches[['anon_id', name_col]].rename(columns={name_col: 'matched_name'})
    return result

def deanonymization_rate(matches_df, anon_df):
    """
    Compute the fraction of anonymized records
    that were uniquely re-identified.
    """
    if len(anon_df) ==0:
        return 0.0
    return len(matches_df)/len(anon_df)
#trying to submit
