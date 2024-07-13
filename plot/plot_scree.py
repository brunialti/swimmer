from sklearn.cluster import KMeans
from imports import  plt, inspect, DataFrame,np
from plot.save_figure_to_file import save_figure_to_file

def plot_scree(data: DataFrame, rho,num_clusters, iter_max, num_repeats):

    # Lista per memorizzare la somma totale dei quadrati entro i cluster (TWSS)
    twss = []

    # Esegui K-means per ciascun numero di cluster da 1 a num_clusters
    #adj_matrix = np.where(np.abs(data) >= rho, 1, 0)
    for k in range(1, num_clusters + 1):
        kmeans = KMeans(n_clusters=k, max_iter=iter_max, n_init=num_repeats, random_state=42)
        kmeans.fit(data)
        twss.append(kmeans.inertia_)

    for i in range(len(twss),1):
        print(i,twss[i]-twss[i-1],(twss[i]-twss[i-1])/twss[1])

    # Plot del grafico a gomito
    plt.figure(figsize=(10, 8))
    plt.plot(range(1, num_clusters + 1), twss, marker='o')
    plt.axvline(x=num_clusters, linestyle='--', color='red')
    plt.title('Elbow Method for Optimal Number of Clusters')
    plt.xlabel('Number of clusters')
    plt.ylabel('Total Within Sum of Squares (TWSS)')
    plt.draw()
    save_figure_to_file(inspect.currentframe().f_code.co_name)