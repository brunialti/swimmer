from imports import pd,np, ttest_ind, multipletests, tqdm, bcolors, inspect

#data.log2_fold_change, data.p_values, data.pval_adj, data.drops = filter_data(observed,control,
def filter_data(observed, control, threshold_fc=3.4, threshold_pval_adj=0.05):

    if (observed.data.shape[0]!=control.data.shape[0]):
        print(observed.data.shape,control.data.shape)
        raise ValueError(f"{bcolors.FAIL}{inspect.currentframe().f_code.co_name}]{bcolors.ENDC}: observed and control data must have the same rows")

    # Estrai i dati pre-elaborati
    observed_data_log2 = observed.data.map(lambda x: np.log2(x + 1))
    control_data_log2 = control.data.map(lambda x: np.log2(x + 1))

    # Liste per memorizzare i valori calcolati
    p_values = []

    for i in tqdm(range(observed.data.shape[0]), desc="filter_data, processing rows",position=0,leave=False):
        # Estrai la riga i-esima, sostituisci NaN con 0
        observed_values = observed.log2.iloc[i].fillna(0).values
        control_values = control.log2.iloc[i].fillna(0).values

        # Effettua il t-test solo se ci sono dati sufficienti
        if len(observed_values) > 1 and len(control_values) > 1:
            _, p_value = ttest_ind(observed_values, control_values, equal_var=False)
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
