from imports import pd, np, plt, sns, inspect
from plot.save_figure_to_file import save_figure_to_file

def plot_correlation_histogram(correlation_matrix, threshold=0.5, title='Pearson Correlation Coefficient Distribution'):

    # Flatten the correlation matrix and filter out self-correlations
    corr_values = correlation_matrix.values[np.triu_indices_from(correlation_matrix, k=1)].astype(float)

    # Set thresholds for accepting or deleting correlations
    accept = np.abs(corr_values) > threshold
    delete = ~accept

    # Compute bin edges
    bin_edges = np.histogram_bin_edges(corr_values, bins=100)

    # Plot histogram
    plt.figure(figsize=(10, 6))

    sns.histplot(corr_values, bins=bin_edges, color='grey', label='delete', kde=False)
    sns.histplot(corr_values[accept], bins=bin_edges, color='red', label='accept', kde=False)

    plt.xlabel('Correlation')
    plt.ylabel('Count')
    plt.title(title)
    plt.legend(title='Legend')
    plt.draw()
    plt.pause(0.1)
    save_figure_to_file(inspect.currentframe().f_code.co_name)
