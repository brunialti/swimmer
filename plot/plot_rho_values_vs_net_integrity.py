from imports import plt,inspect
from plot.save_figure_to_file import save_figure_to_file

def plot_rho_values_vs_net_integrity(t_eq100, t_lt100, rho_values, lcc_sizes, subnet_counts, step):

    fig, ax1 = plt.subplots(figsize=(10, 6))

    ax1.plot(rho_values, lcc_sizes, 'b-', label='LCC Size')
    ax1.set_xlabel(f'Correlation threshold (step={step})')
    ax1.set_ylabel('Largest Connected Component (node ratio)', color='b')
    ax1.axvline(x=t_eq100, color='green', linestyle='--', label=f'Threshold LCC eq 100% at {round(t_eq100, 2)}')
    ax1.axvline(x=t_lt100, color='red', linestyle='-.', label=f'Threshold LCC lt 100% at {round(t_lt100, 2)}')

    ax2 = ax1.twinx()
    ax2.plot(rho_values, subnet_counts, 'orange', label='Subnet Counts')
    ax2.set_ylabel('Number of Subnets', color='orange')
    fig.suptitle(f'Network integrity check')
    ax1.grid(True, which='both', linestyle='--', color='lightgrey', linewidth=0.5)
    fig.tight_layout()
    fig.legend(loc='lower left', bbox_to_anchor=(0.1,0.2))
    plt.draw()
    #plt.pause(0.01)
    save_figure_to_file(inspect.currentframe().f_code.co_name)
