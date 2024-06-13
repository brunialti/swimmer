from imports import pd, np, plt, nx, inspect, DataFrame
from plot.save_figure_to_file import save_figure_to_file

def plot_correlation_network(correlation_df: DataFrame, rho_threshold):

    # Assicurati che la matrice di correlazione sia simmetrica
    assert (correlation_df.values == correlation_df.values.T).all(), "La matrice di correlazione deve essere simmetrica."

    # Rimuovi le correlazioni di una variabile con se stessa (imposta la diagonale a 0)
    np.fill_diagonal(correlation_df.values, 0)

    # Crea la matrice di adiacenza in base alla soglia rho
    adj_matrix = np.where(np.abs(correlation_df.values) >= rho_threshold, 1, 0)

    # Crea il grafo a partire dalla matrice di adiacenza
    G = nx.from_numpy_array(adj_matrix)

    # Mappa gli indici ai nomi delle colonne per mantenere le etichette dei nodi
    mapping = {i: name for i, name in enumerate(correlation_df.columns)}
    G = nx.relabel_nodes(G, mapping)

    # Rimuovi i nodi isolati (senza connessioni)
    G.remove_nodes_from(list(nx.isolates(G)))

    # Usa il layout "kamada_kawai" per una visualizzazione esteticamente piacevole
    pos = nx.kamada_kawai_layout(G)

    # Disegna la rete
    plt.figure(figsize=(14, 10))
    nx.draw_networkx_nodes(G, pos, node_size=20, node_color='blue')
    nx.draw_networkx_edges(G, pos, alpha=0.3, width=0.5)
    #nx.draw_networkx_labels(G, pos, font_size=6, font_color='black')
    plt.title(f'Network with Correlation Threshold {rho_threshold}')
    plt.draw()
    #plt.pause(0.01)
    save_figure_to_file(inspect.currentframe().f_code.co_name)

