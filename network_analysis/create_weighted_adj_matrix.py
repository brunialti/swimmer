from imports import pd, np

def create_weighted_adj_matrix(correlation_matrix, threshold):
    adj_matrix = np.where(np.abs(correlation_matrix) >= threshold, correlation_matrix, 0)
    return adj_matrix
