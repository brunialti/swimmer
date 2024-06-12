from imports import plt,os,bcolors

def save_figure_to_file(function_name):

    # Crea la directory 'figures' se non esiste
    figures_dir = "figures"
    if not os.path.exists(figures_dir):
        os.makedirs(figures_dir)

    # Salva il grafico nella directory 'figures' con il nome della funzione
    file_path = os.path.join(figures_dir, f"{function_name}.png")
    plt.savefig(file_path)
    print(f"[{bcolors.OKGREEN}{function_name}{bcolors.ENDC}]: graph saved as {file_path}")