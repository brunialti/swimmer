from imports import pd, np, plt, inspect
from plot.save_figure_to_file import save_figure_to_file
from data import Data

def plot_iqr_histogram(data: Data, threshold):
    """Calcola gli IQR di ogni riga in base al percentile specificato e crea un istogramma delle frequenze degli IQR.

    Args:
        threshold (float): Soglia per categorizzar i dati in 'accept' e 'delete'.
    """
    # Utilizziamo self.IQR già calcolato
    iqr_values = pd.Series(data.iqr)

    # Categorizzazione in base alla soglia
    categories = iqr_values.apply(lambda x: 'accept' if x >= threshold else 'delete')

    # Calcolo dei percentili per il range dei bins
    lower_bound = 0
    upper_bound = np.percentile(iqr_values, 100)

    # Selezione del numero di bins per migliorare la visualizzazione
    bins = np.linspace(lower_bound, upper_bound, 100)

    plt.figure(figsize=(10, 6))

    # Istogramma per i dati "delete"
    deleted_iqr_values = iqr_values[categories == 'delete']
    plt.hist(deleted_iqr_values, bins=bins, alpha=0.5, color='gray', label='delete')

    # Istogramma per i dati "accept"
    accepted_iqr_values = iqr_values[categories == 'accept']
    plt.hist(accepted_iqr_values, bins=100, alpha=0.5, color='red', label='accept')

    plt.legend(title="Categories")

    plt.xlabel('Interquartile Range (IQR)')
    plt.ylabel('Frequency')
    plt.title(data.name)
    plt.draw()
    #plt.pause(0.01)
    save_figure_to_file(inspect.currentframe().f_code.co_name)