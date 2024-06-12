from imports import pd,np, ttest_ind, multipletests, tqdm

def preprocess_data(data, observed_data, control_data, threshold_perc_zeros=75,threshold_iqr=1.5, threshold_fc=3.4, threshold_pval_adj=0.05):
    # Calcola i log2 dei dati, aggiungendo 1 per evitare log(0)
    observed_data_log2 = observed_data.data.apply(lambda col: col.map(lambda x: np.log2(x + 1)))
    control_data_log2 = control_data.data.apply(lambda col: col.map(lambda x: np.log2(x + 1)))

    # Funzione per calcolare l'IQR
    def calculate_IQR(row):
        Q1 = np.percentile(row, 25)
        Q3 = np.percentile(row, 75)
        return Q3 - Q1

    # Liste per memorizzare i valori calcolati
    IQR_values = []
    #p_values = []
    perc_zeros = []

    for i in tqdm(range(data.data.shape[0]), desc="filter_data, processing rows"):
        # Estrai la riga i-esima, sostituisci NaN con 0
        obs_values = observed_data_log2.iloc[i].fillna(0).values
        ctrl_values = control_data_log2.iloc[i].fillna(0).values

        # Calcola la percentuale di valori pari a zero o NaN
        total_values = len(obs_values) + len(ctrl_values)
        zero_nan_count = np.sum(obs_values == 0) + np.sum(ctrl_values == 0)
        perc_zero_nan = (zero_nan_count / total_values) * 100
        perc_zeros.append(perc_zero_nan)

        # Calcola l'IQR per la riga combinata observed e control
        combined_values = np.concatenate((obs_values, ctrl_values))
        IQR = calculate_IQR(combined_values)
        IQR_values.append(IQR)

    # Calcola gli indici da rimuovere
    drops = [idx for idx in range(data.data.shape[0])
             if (perc_zeros[idx] > threshold_perc_zeros) or
                (IQR_values[idx] < threshold_iqr)]

    return IQR_values, perc_zeros, drops
