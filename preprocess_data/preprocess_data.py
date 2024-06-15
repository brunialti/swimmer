from imports import pd,np, ttest_ind, multipletests, tqdm


# data.log2, data.iqr, data.percZeros, data.drops, = preprocess_data(data)
def preprocess_data(data, threshold_perc_zeros=75, threshold_iqr=1.5):
    # Calcola i log2 dei dati, aggiungendo 1 per evitare log(0)
    data.log2 = data.data.apply(lambda col: col.map(lambda x: np.log2(x + 1)))

    # Funzione per calcolare l'IQR
    def calculate_IQR(row):
        Q1 = np.percentile(row, 25)
        Q3 = np.percentile(row, 75)
        return Q3 - Q1

    # Liste per memorizzare i valori calcolati
    data.iqr = []
    data.percZeros = []

    for i in tqdm(range(data.data.shape[0]), desc="filter_data, processing rows", position=0, leave=False):
        # Estrai la riga i-esima, sostituisci NaN con 0
        data_values = data.log2.iloc[i].fillna(0).values

        # Calcola la percentuale di valori pari a zero o NaN
        total_values = len(data_values)
        zero_nan_count = np.sum((data_values == 0) | np.isnan(data_values))
        perc_zero_nan = (zero_nan_count / total_values) * 100
        data.percZeros.append(perc_zero_nan)

        # Calcola l'IQR per la riga combinata observed e control
        IQR = calculate_IQR(data_values)
        data.iqr.append(IQR)

    # Calcola gli indici da rimuovere
    data.drops = [idx for idx in range(data.data.shape[0])
             if (data.percZeros[idx] > threshold_perc_zeros) or
                (data.iqr[idx] < threshold_iqr)]

    return data


def old_preprocess_data(data, threshold_perc_zeros=75, threshold_iqr=1.5):
    # Calcola i log2 dei dati, aggiungendo 1 per evitare log(0)
    log2 = data.data.apply(lambda col: col.map(lambda x: np.log2(x + 1)))

    # Funzione per calcolare l'IQR
    def calculate_IQR(row):
        Q1 = np.percentile(row, 25)
        Q3 = np.percentile(row, 75)
        return Q3 - Q1

    # Liste per memorizzare i valori calcolati
    IQR_values = []
    perc_zeros = []

    for i in tqdm(range(data.data.shape[0]), desc="filter_data, processing rows", position=0, leave=False):
        # Estrai la riga i-esima, sostituisci NaN con 0
        data_values = log2.iloc[i].fillna(0).values

        # Calcola la percentuale di valori pari a zero o NaN
        total_values = len(data_values)
        zero_nan_count = np.sum((data_values == 0) | np.isnan(data_values))
        perc_zero_nan = (zero_nan_count / total_values) * 100
        perc_zeros.append(perc_zero_nan)

        # Calcola l'IQR per la riga combinata observed e control
        IQR = calculate_IQR(data_values)
        IQR_values.append(IQR)

    # Calcola gli indici da rimuovere
    drops = [idx for idx in range(data.data.shape[0])
             if (perc_zeros[idx] > threshold_perc_zeros) or
                (IQR_values[idx] < threshold_iqr)]

    return log2, IQR_values, perc_zeros, drops
