from imports import pd, np, plt, sns, inspect
from plot.save_figure_to_file import save_figure_to_file
from data import Data

def plot_iqr_vs_perc_non_zero(data: Data, threshold_prc_iqr, threshold_perc_zeros):
    """
    Crea un grafico scatter plot dei valori di IQR contro la percentuale di valori non zero.

    Args:
        data: Dataset contenente le informazioni da tracciare.
        threshold_prc_iqr (float): Soglia per il valore IQR.
        threshold_perc_zeros (float): Soglia per la percentuale di zeri.
    """
    plt.figure(figsize=(10, 6))

    # Calcoliamo la percentuale di valori non zero
    perc_non_zeros = 100 - np.array(data.percZeros)

    # Creazione del DataFrame dai dati
    df = pd.DataFrame({
        'IQR': data.iqr,
        'perc_non_zeros': perc_non_zeros
    })

    # Categorizzazione in base alla soglia
    categories = ['accept' if i not in data.drops else 'delete' for i in range(len(data.iqr))]

    # Creazione del grafico scatter plot
    sns.scatterplot(x='IQR', y='perc_non_zeros', hue=categories, data=df, palette={'accept': 'red', 'delete': 'gray'})

    # Aggiunta delle linee tratteggiate con le etichette
    plt.axvline(x=threshold_prc_iqr, color='black', linestyle='-.', label=f'IQR threshold = {threshold_prc_iqr}')
    plt.axhline(y=100 - threshold_perc_zeros, color='black', linestyle='--', label=f'Non-zero threshold = {100 - threshold_perc_zeros}%')

    plt.title(data.name)
    plt.xlabel('Interquartile Range (IQR)')
    plt.ylabel('% of non-zero elements')

    # Aggiornamento della legenda per evitare duplicati
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), title='Legend')
    plt.draw()
    #plt.pause(0.01)
    save_figure_to_file(inspect.currentframe().f_code.co_name)