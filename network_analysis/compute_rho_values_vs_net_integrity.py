from imports import np, tqdm, nx

def compute_rho_values_vs_net_integrity(correlation_matrix, min_threshold=0.1, max_threshold=0.9, step=0.05):

    rho_values = np.arange(min_threshold, max_threshold + step, step)
    lcc_sizes = []
    subnet_counts = []

    t_eq100 = 0
    t_lt100 = 0
    for rho in tqdm(rho_values, desc="compute_rho_values_vs_net_integrity, processing rho",position=0,leave=False):
        adj_matrix = np.where(np.abs(correlation_matrix) >= rho, 1, 0)
        G = nx.from_numpy_array(adj_matrix)
        largest_cc = max(nx.connected_components(G), key=len)
        ratio = len(largest_cc) / len(correlation_matrix)
        if ratio < 1 and t_eq100 == 0:
            t_eq100 = rho - step
            t_lt100 = rho
        lcc_sizes.append(ratio)
        subnet_counts.append(nx.number_connected_components(G))

    return t_eq100, t_lt100, rho_values, lcc_sizes, subnet_counts