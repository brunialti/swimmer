from imports import np

def compute_network_integrity(adj_matrix):
    degrees = np.sum(adj_matrix > 0, axis=0)
    return degrees
