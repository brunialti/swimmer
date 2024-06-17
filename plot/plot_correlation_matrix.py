from imports import pd, np, plt, sns, inspect
from plot.save_figure_to_file import save_figure_to_file

def plot_correlation_matrix(correlation_matrix, title='Correlation Matrix'):

    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=False, cmap='coolwarm', cbar=True)
    plt.title(title)
    plt.draw()
    save_figure_to_file(inspect.currentframe().f_code.co_name)
