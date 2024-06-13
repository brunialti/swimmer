from imports import pd,np, ttest_ind, multipletests, tqdm, sys

def filter_data(data, observed_data, control_data, threshold_fc=3.4, threshold_pval_adj=0.05):
    # Calcola i log2 dei dati, aggiungendo 1 per evitare log(0)
    observed_data_log2 = observed_data.data.map(lambda x: np.log2(x + 1))
    control_data_log2 = control_data.data.map(lambda x: np.log2(x + 1))

    # Liste per memorizzare i valori calcolati
    p_values = []

    for i in tqdm(range(data.data.shape[0]), desc="filter_data, processing rows",position=0,leave=False):
        # Estrai la riga i-esima, sostituisci NaN con 0
        obs_values = observed_data_log2.iloc[i].fillna(0).values
        ctrl_values = control_data_log2.iloc[i].fillna(0).values

        # Effettua il t-test solo se ci sono dati sufficienti
        if len(obs_values) > 1 and len(ctrl_values) > 1:
            _, p_value = ttest_ind(obs_values, ctrl_values, equal_var=False)
        else:
            p_value = np.nan  # Usa NaN per rappresentare i dati insufficienti
        p_values.append(p_value)

    # Converti p_values in array numpy
    p_values = np.array(p_values)

    # Aggiustamento dei valori p usando il metodo di Benjamini-Hochberg
    if len(p_values) > 0:
        pval_adj = multipletests(p_values, method='fdr_bh')[1]
    else:
        pval_adj = np.array([])

    # Calcola la media log2 dei gruppi observed e control
    observed_log2_mean = observed_data_log2.mean(axis=1)
    control_log2_mean = control_data_log2.mean(axis=1)

    # Calcola il fold-change log2 come differenza tra le medie log2
    log2_fold_change = observed_log2_mean - control_log2_mean

    # Converti log2_fold_change e pval_adj in array numpy
    log2_fold_change_values = log2_fold_change.values
    pval_adj_values = pval_adj

    # Calcola gli indici da rimuovere in base a pval_adj
    drops_pval = [idx for idx in range(len(log2_fold_change_values)) if pval_adj_values[idx] > threshold_pval_adj]

    # Rimuove gli elementi in base a pval_adj
    if len(drops_pval) > 0:
        log2_fold_change_values = np.delete(log2_fold_change_values, drops_pval)
        p_values = np.delete(p_values, drops_pval)
        pval_adj_values = np.delete(pval_adj_values, drops_pval)

    # Calcola gli indici da rimuovere in base a log2_fold_change
    drops_fc = [idx for idx in range(len(log2_fold_change_values)) if
                abs(log2_fold_change_values[idx]) <= np.log2(threshold_fc)]

    # Rimuove gli elementi in base a log2_fold_change
    if len(drops_fc) > 0:
        log2_fold_change_values = np.delete(log2_fold_change_values, drops_fc)
        p_values = np.delete(p_values, drops_fc)
        pval_adj_values = np.delete(pval_adj_values, drops_fc)

    # Unisci gli indici dei dati da rimuovere
    drops = list(set(drops_pval + drops_fc))

    return log2_fold_change, p_values, pval_adj, drops

def old_filter_data(data, observed_data, control_data, threshold_fc=3.4, threshold_pval_adj=0.05):
    # Estrai i dati pre-elaborati
    observed_data_log2 = observed_data.data.map(lambda x: np.log2(x + 1))
    control_data_log2 = control_data.data.map(lambda x: np.log2(x + 1))

    # Liste per memorizzare i valori calcolati
    p_values = []

    for i in tqdm(range(data.data.shape[0]), desc="filter_data, processing rows"):
        # Estrai la riga i-esima, sostituisci NaN con 0
        obs_values = observed_data_log2.iloc[i].fillna(0).values
        ctrl_values = control_data_log2.iloc[i].fillna(0).values

        # Effettua il t-test solo se ci sono dati sufficienti
        if len(obs_values) > 1 and len(ctrl_values) > 1:
            _, p_value = ttest_ind(obs_values, ctrl_values, equal_var=False)
        else:
            p_value = np.nan  # Usa NaN per rappresentare i dati insufficienti
        p_values.append(p_value)

    # Converti p_values in array numpy
    p_values = np.array(p_values)

    # Aggiustamento dei valori p usando il metodo di Benjamini-Hochberg
    if len(p_values) > 0:
        pval_adj = multipletests(p_values, method='fdr_bh')[1]
    else:
        pval_adj = np.array([])

    # Calcola la media log2 dei gruppi observed e control
    observed_log2_mean = observed_data_log2.mean(axis=1)
    control_log2_mean = control_data_log2.mean(axis=1)

    # Calcola il fold-change log2 come differenza tra le medie log2
    log2_fold_change = observed_log2_mean - control_log2_mean

    # Converti log2_fold_change e pval_adj in array numpy
    log2_fold_change_values = log2_fold_change.values
    pval_adj_values = pval_adj

    # Calcola gli indici da rimuovere
    drops = [idx for idx in range(len(log2_fold_change_values))
             if (abs(log2_fold_change_values[idx]) < np.log2(threshold_fc)) or
             (pval_adj_values[idx] > threshold_pval_adj)]

    #return log2_fold_change, p_values, pval_adj, drops
    return log2_fold_change_values, p_values, pval_adj_values, drops
