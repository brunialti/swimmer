from imports import np, DataFrame

def compute_correlation(d: DataFrame, method='pearson'):
    if method not in ['pearson', 'spearman']:
        raise ValueError("Method should be either 'pearson' or 'spearman'")

    # Applicazione della trasformazione log2 con controllo per valori non positivi
    data = d.map(lambda x: np.log2(x) if x > 0 else np.nan).T
    corr_matrix = data.corr()

    return corr_matrix