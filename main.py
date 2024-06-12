from data import *
from plot import *
from network_analysis import *
from preprocess_data import *

# Parametri di input
input_parameter = {
    'prc_iqr': 0.50,
    'threshold_prc_iqr': 0.11,
    'threshold_perc_zeros': 75,
    'threshold_fc': 3.4,
    'threshold_pval_adj': 0.05,
    'type_correlation': "pearson",
    'threshold_prc_corr': 0.8,
    'threshold_pval_adj_corr': 0.05,
    'min_rho': 0.2,
    'max_rho': 0.9,
    'step_rho': 0.02,
}

# Percorsi dei file
rna_matrix_path = "C:/Users/rober/OneDrive/Desktop old/BIOINFORMATICS/code swimmer/code/project/TCGA/dataset/brca/matrix/matrice__brca_RNASeq.txt"
rna_normal_list = "C:/Users/rober/OneDrive/Desktop old/BIOINFORMATICS/code swimmer/code/project/TCGA/dataset/brca/list/Lista__RNASeq_Normal__brca__4wayData.txt"
rna_tumor_list = "C:/Users/rober/OneDrive/Desktop old/BIOINFORMATICS/code swimmer/code/project/TCGA/dataset/brca/list/Lista__RNASeq_Tumor__brca__4wayData.txt"

# Inizializzazione del dataset
dataset = DataSet()

# Caricamento dei dati
data = Data()
d1 = Data()
d2 = Data()
data.load_numeric_dataframe("RNA", rna_matrix_path)
d1.load_numeric_dataframe("RNA_NORMAL_LIST", rna_normal_list)
d2.load_numeric_dataframe("RNA_TUMOR_LIST", rna_tumor_list)

# Clipping e preprocessamento
data.clip_extract(col_indices=d1.data + d2.data)
control=data.extract(name='CONTROL',col_indices=d1.data,mode='label')
observed=data.extract(name='OBSERVED',col_indices=d2.data,mode='label')

# Verifica che i dati siano caricati correttamente8

if data.data is not None:

    # Data preprocessing
    print('Data processing...')
    data.iqr, data.percZeros, data.drops, = preprocess_data(data,observed,control,
                                            threshold_fc=input_parameter["threshold_fc"],
                                            threshold_pval_adj=input_parameter["threshold_pval_adj"])
    plot_iqr_histogram(data, input_parameter["threshold_prc_iqr"])
    plot_iqr_vs_perc_non_zero(data, input_parameter["threshold_prc_iqr"], input_parameter["threshold_perc_zeros"])
    data.clip_delete(row_indices = data.drops, mode='index')

    # Filtraggio dei dati
    control = data.extract("CONTROL", col_indices=d1.data, mode='label')
    observed = data.extract("CASE", col_indices=d2.data, mode='label')

    print('Data filtering...')
    data.log2_fold_change, data.p_values, data.pval_adj, data.drops = filter_data(data,observed,control,
                                            threshold_fc=input_parameter["threshold_fc"],
                                            threshold_pval_adj=input_parameter["threshold_pval_adj"])
    plot_fold_change_vs_count(data.data,data.log2_fold_change,input_parameter["threshold_fc"])
    plot_volcano(data, d1, d2, input_parameter["threshold_fc"], input_parameter["threshold_pval_adj"])
    data.clip_delete(row_indices = data.drops, mode='index')
    data.save(name='FILTERED')

    # Create netwwork
    print('Create and plot correlation matrix...')
    correlation_matrix = compute_correlation(data.data, method=input_parameter['type_correlation'])
    plot_correlation_histogram(correlation_matrix, input_parameter['threshold_prc_corr'])

    print('Plot rho values vs net integrity %...')
    t_eq100,t_lt100,rho_values,lcc_sizes,subnet_counts=compute_rho_values_vs_net_integrity(correlation_matrix, min_threshold=input_parameter['min_rho'], max_threshold=input_parameter['max_rho'], step=input_parameter['step_rho'])
    plot_rho_values_vs_net_integrity(t_eq100,t_lt100,rho_values,lcc_sizes,subnet_counts,step=input_parameter['step_rho'])

    print('Plot correlation matrix and network...')
    #plot_correlation_matrix(correlation_matrix)
    #plot_correlation_network(correlation_matrix,t_eq100)

    print('Computing network degrees...')
    network_degrees = compute_network_integrity(correlation_matrix)

else:
    print("Errore nel caricamento dei dati.")

pass