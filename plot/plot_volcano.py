from imports import pd, np, plt, sns, inspect
from plot.save_figure_to_file import save_figure_to_file
from data import Data

def plot_volcano(data: Data, observed, control, threshold_fc, threshold_pvalue):
    # Converti observed.data e control.data in DataFrame se non lo sono già
    if isinstance(observed.data, list):
        observed_data = pd.DataFrame(observed.data)
    elif isinstance(observed.data, np.ndarray):
        observed_data = pd.DataFrame(observed.data)
    elif isinstance(observed.data, pd.DataFrame):
        observed_data = observed.data
    else:
        raise ValueError("observed.data must be a list, numpy array, or pandas DataFrame")

    if isinstance(control.data, list):
        control_data = pd.DataFrame(control.data)
    elif isinstance(control.data, np.ndarray):
        control_data = pd.DataFrame(control.data)
    elif isinstance(control.data, pd.DataFrame):
        control_data = control.data
    else:
        raise ValueError("control.data must be a list, numpy array, or pandas DataFrame")

    # Calcola il valore -log10(adjusted p-value)
    log10_pvalue = -np.log10(data.pval_adj)
    log10_pvalue[np.isinf(log10_pvalue)] = 0  # Sostituisce i valori infiniti con zero
    log10_pvalue = np.nan_to_num(log10_pvalue)  # Sostituisce NaN con zero

    # Calcola la media log2 dei gruppi observed e control
    #observed_log2_mean = observed_data.mean(axis=1)
    #control_log2_mean = control_data.mean(axis=1)

    # Calcola il fold-change log2 come differenza tra le medie log2
    #log2_fold_change = observed_log2_mean - control_log2_mean

    # Verifica che log2_fold_change e log10_pvalue abbiano la stessa lunghezza
    if len(data.log2_fold_change) != len(log10_pvalue):
        raise ValueError(f"Mismatch in length: log2_fold_change ({len(data.log2_fold_change)}) and log10_pvalue ({len(log10_pvalue)})")

    # Crea un DataFrame per facilitare la gestione dei dati
    df = pd.DataFrame({'log2_fold_change': data.log2_fold_change, 'log10_pvalue': log10_pvalue})

    # Aggiungi una colonna per identificare i dati da eliminare
    df['category'] = 'neutral'
    df.loc[(df['log2_fold_change'] >  np.log2(threshold_fc)) & (data.pval_adj < threshold_pvalue), 'category'] = 'up'
    df.loc[(df['log2_fold_change'] < -np.log2(threshold_fc)) & (data.pval_adj < threshold_pvalue), 'category'] = 'down'

    # Colori per le categorie
    palette = {'neutral': 'grey', 'down': 'blue', 'up': 'yellow'}

    # Crea il volcano plot
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x='log2_fold_change', y='log10_pvalue', hue='category', palette=palette)

    plt.title('RNA', fontsize=20, weight='bold')
    plt.xlabel('Log2 Fold-change (FC)')
    plt.ylabel('-Log10(adjusted p-value)')

    # Aggiungi linee di soglia
    plt.axvline(x=-np.log2(threshold_fc), color='black', linestyle='--')
    plt.axvline(x=np.log2(threshold_fc), color='black', linestyle='--')
    plt.axhline(y=-np.log10(threshold_pvalue), color='black', linestyle='--')

    plt.legend(title='Legend')
    plt.draw()
    plt.pause(0.01)
    save_figure_to_file(inspect.currentframe().f_code.co_name)