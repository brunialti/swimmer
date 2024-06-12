from imports import pd, np, plt, sns, inspect, DataFrame
from plot.save_figure_to_file import save_figure_to_file
from pandas import DataFrame

def plot_fold_change_vs_count(data: DataFrame,log2_fold_change, threshold):

    # print('plot_fold_change_vs_count',data.data.shape, len(data.log2_fold_change), len(data.indedata.s['cols']), len(data.indexes['rows']))
    # Controlla se data è un DataFrame
    if not isinstance(data, DataFrame):
        raise ValueError("data should be a DataFrame")

    if (data.shape[0] != len(log2_fold_change)):
        raise ValueError("Columns or rows dimension of data and indexes are not the same")

    # Crea un istogramma del fold-change
    plt.figure(figsize=(10,6))

    # Calcola i bin edges
    bin_edges = np.histogram_bin_edges(log2_fold_change, bins=100)

    # Plot whole histogram
    sns.histplot(log2_fold_change, bins=bin_edges, color='gray', kde=False, label='delete')

    # Evidenzia le barre da accettare
    log2_threshold = np.log2(threshold)
    accepted_values = [value for value in log2_fold_change if abs(value) > log2_threshold]
    sns.histplot(accepted_values, bins=bin_edges, color='red', kde=False, label='accept')

    plt.title('RNA Fold-change vs Count', fontsize=20, weight='bold')
    plt.xlabel('Log2 Fold-change (FC)', fontsize=16)
    plt.ylabel('Count', fontsize=16)

    # Aggiungi la legenda
    plt.legend(title='Fold-change Categories', fontsize=14, title_fontsize='16')
    #plt.grid(True)

    # Salva la figura in un file
    save_figure_to_file(inspect.currentframe().f_code.co_name)
    plt.draw()
    plt.pause(0.01)
    save_figure_to_file(inspect.currentframe().f_code.co_name)