from imports import pd,os,bcolors
import inspect

class Data:
    def __init__(self, name=None):
        self.name = name
        self.input_file = ''
        self.path = ''
        self.indexes = {}
        self.data = None
        self.drops = []
        self.log2_fold_change = None
        self.p_values = None
        self.pval_adj = None
        self.iqr = None
        self.percZeros = None

    def load_numeric_dataframe(self, name, file_path, separator='\t'):

        """Carica un DataFrame Pandas da un file CSV e verifica se contiene solo dati numerici o una lista di stringhe.
        """

        def is_numeric(df):
            """Verifica se il DataFrame contiene solo dati numerici."""
            return df.apply(lambda col: col.map(lambda x: isinstance(x, (int, float)))).all().all()

        def split_path_and_filename(file_path):
            # Utilizza os.path per dividere il percorso dal nome del file e l'estensione
            directory, filename = os.path.split(file_path)
            name, ext = os.path.splitext(filename)
            return directory, name, ext

        self.path, self.filename, self.extension = split_path_and_filename(file_path)
        self.name = name
        self.separator = separator

        # Prova a leggere il file come lista di stringhe
        try:
        #if True:
            with open(file_path, 'r') as file:
                lines = file.read().splitlines()
                if all(isinstance(line, str) and len(line.split(separator)) == 1 for line in lines):
                    self.data = lines
                    self.data_type = 'list'
                    print(f"[{bcolors.OKGREEN}{inspect.currentframe().f_code.co_name}{bcolors.ENDC}]: Loaded '{self.name}' list, dim={len(self.data)}")
                    return self
        except Exception as e:
            pass

        # Prova a leggere il file come se avesse un'intestazione delle colonne e delle righe
        #if True:
        try:
            self.data = pd.read_csv(file_path, index_col=0, sep=separator)
            if is_numeric(self.data):
                self.indexes['cols'] = self.data.columns.tolist()
                self.indexes['rows'] = self.data.index.tolist()
                self.data.reset_index(drop=True, inplace=True)
                self.data.columns = range(self.data.shape[1])
                self.data_type = 'matrix'
                print(f"[{bcolors.OKGREEN}{inspect.currentframe().f_code.co_name}]{bcolors.ENDC}: Loaded '{self.name}' matrix, vhead and hhead, dim={str(self.data.shape)}")
                return self
        except Exception as e:
            pass

        # Prova a leggere il file come se avesse solo un'intestazione delle colonne
        #if True:
        try:
            self.data = pd.read_csv(file_path, sep=separator)
            if is_numeric(self.data):
                self.indexes['cols'] = self.data.columns.tolist()
                self.data.columns = range(self.data.shape[1])
                self.data_type = 'matrix'
                print(f"{bcolors.OKGREEN}{inspect.currentframe().f_code.co_name}]{bcolors.ENDC}: Loaded '{self.name}', hhead, dim={str(self.data.shape)}")
                return self
        except Exception as e:
            pass

        # Prova a leggere il file senza intestazioni
        #if True:
        try:
            self.data = pd.read_csv(file_path, header=None, sep=separator)
            if is_numeric(self.data):
                self.data_type = 'matrix'
                print(f"{bcolors.OKGREEN}{inspect.currentframe().f_code.co_name}]{bcolors.ENDC}: Loaded '{self.name}', no heads, dim={str(self.data.shape)}")
                return self
        except Exception as e:
            pass

        raise ValueError("The file does not contain only numeric data or is in an unrecognized format")

    def restore_headers_and_indexes(self):
        if self.data is None or self.data_type != 'matrix':
            raise ValueError("Data is not loaded or is not a matrix")

        # Ripristina gli header delle colonne
        if 'cols' in self.indexes:
            self.data.columns = self.indexes['cols']

        # Ripristina gli indici delle righe
        if 'rows' in self.indexes:
            self.data.index = self.indexes['rows']
        #print(f"{{bcolors.OKGREEN}.WARNING}inspect.currentframe().f_code.co_name}]: headers and indexes restored for '{self.name}'")

    def save(self, name=''):
        if self.data is None:
            raise ValueError("No data to save")
        if name == '':
            name = self.name

        # Determina il nome del file
        save_filename = f"{self.filename}_{name}{self.extension}"
        save_path = os.path.join('', save_filename)

        self.restore_headers_and_indexes()

        if self.data_type == 'list':
            # Salva la lista come un file di testo
            with open(save_path, 'w') as file:
                file.write('\n'.join(self.data))
        elif self.data_type == 'matrix':
            # Salva il DataFrame nel formato originale
            self.data.to_csv(save_path, index=True, header=True, sep=self.separator)
        else:
            raise ValueError("Unrecognized data type")

        print(f"[{bcolors.OKGREEN}{inspect.currentframe().f_code.co_name}]{bcolors.ENDC}: data saved to {save_path}")

    def clip_extract(self, row_indices=None, col_indices=None, mode='label'):
        if row_indices is None and col_indices is None:
            raise ValueError("Clip: At least one of row_indices or col_indices must be provided, none detected")

        if self.data_type == 'list':
            raise ValueError("Clip: Clipping is not supported for list data type")

        if mode not in ['label', 'index']:
            raise ValueError("Mode must be either 'label' or 'index'")

        original_rows = self.indexes['rows']
        original_cols = self.indexes['cols']

        if row_indices is not None:
            if mode == 'label':
                valid_row_indices = [original_rows.index(idx) for idx in row_indices if idx in original_rows]
                self.indexes['rows'] = [idx for idx in row_indices if idx in original_rows]
            else:
                valid_row_indices = row_indices
                self.indexes['rows'] = [original_rows[i] for i in valid_row_indices]
            self.data = self.data.iloc[valid_row_indices, :]

        if col_indices is not None:
            if mode == 'label':
                valid_col_indices = [original_cols.index(idx) for idx in col_indices if idx in original_cols]
                self.indexes['cols'] = [idx for idx in col_indices if idx in original_cols]
            else:
                valid_col_indices = col_indices
                self.indexes['cols'] = [original_cols[i] for i in valid_col_indices]
            self.data = self.data.iloc[:, valid_col_indices]

        print(f"[{bcolors.OKGREEN}{inspect.currentframe().f_code.co_name}]{bcolors.ENDC}: Clipped data, new shape: {self.data.shape}")

    def extract(self, name='', row_indices=None, col_indices=None, mode='label'):

        if row_indices is None and col_indices is None:
            raise ValueError("Extract: At least one of row_indices or col_indices must be provided, none detected")

        if self.data_type == 'list':
            raise ValueError("Extract: Clipping is not supported for list data type")

        if mode not in ['label', 'index']:
            raise ValueError("Mode must be either 'label' or 'index'")

        exdata = Data(name)
        valid_row_indices=[]
        valid_col_indices=[]
        original_rows = self.indexes['rows']
        original_cols = self.indexes['cols']

        if row_indices is not None:
            if mode == 'label':
                valid_row_indices = [original_rows.index(idx) for idx in row_indices if idx in original_rows]
                exdata.indexes['rows'] = [idx for idx in row_indices if idx in original_rows]
            else:
                valid_row_indices = row_indices
                exdata.indexes['rows'] = [original_rows[i] for i in valid_row_indices]
            if valid_row_indices:
                exdata.data = self.data.iloc[valid_row_indices, :]
            else:
                exdata.data = pd.DataFrame()

        if col_indices is not None:
            if mode == 'label':
                valid_col_indices = [original_cols.index(idx) for idx in col_indices if idx in original_cols]
                exdata.indexes['cols'] = [idx for idx in col_indices if idx in original_cols]
            else:
                valid_col_indices = col_indices
                exdata.indexes['cols'] = [original_cols[i] for i in valid_col_indices]
            if valid_col_indices:
                exdata.data = self.data.iloc[:, valid_col_indices]
            else:
                exdata.data = pd.DataFrame()

        if exdata.data.empty:
            print(f"[{bcolors.OKGREEN}{inspect.currentframe().f_code.co_name}{bcolors.ENDC}]: extracted data {name}, but the result is empty.")

        return exdata

    def clip_delete(self, row_indices=None, col_indices=None, mode='label'):

        if row_indices is None and col_indices is None:
            raise ValueError("Clip: At least one of row_indices or col_indices must be provided, none detected")

        if self.data is None:
            raise ValueError("Clip: Data is not loaded")

        if self.data_type == 'list':
            raise ValueError("Clip: Clipping is not supported for list data type")

        if mode not in ['label', 'index']:
            raise ValueError("Mode must be either 'label' or 'index'")

        if row_indices is not None:
            print(f"[{bcolors.OKGREEN}{inspect.currentframe().f_code.co_name}{bcolors.ENDC}]: drop {len(row_indices)} of {self.data.shape[0]} rows")
            original_rows = self.indexes['rows']
            if mode == 'label':
                drop_row_indices = [idx for idx in row_indices if idx in original_rows]
                self.indexes['rows'] = [idx for idx in original_rows if idx not in row_indices]
            else:
                drop_row_indices = row_indices
                self.indexes['rows'] = [original_rows[i] for i in range(len(original_rows)) if i not in drop_row_indices]
            self.data = self.data.drop(index=self.data.index[row_indices])

        if col_indices is not None:
            print(f"[{bcolors.OKGREEN}{inspect.currentframe().f_code.co_name}[{bcolors.ENDC}]: drop {len(col_indices)} of {self.data.shape[1]} cols")
            original_cols = self.indexes['cols']
            if mode == 'label':
                drop_col_indices = [idx for idx in col_indices if idx in original_cols]
                self.indexes['cols'] = [idx for idx in original_cols if idx not in col_indices]
            else:
                drop_col_indices = col_indices
                self.indexes['cols'] = [original_cols[i] for i in range(len(original_cols)) if i not in drop_col_indices]
            self.data = self.data.drop(columns=self.data.index[row_indices])

        print(f"[{bcolors.OKGREEN}{inspect.currentframe().f_code.co_name}{bcolors.ENDC}]: Clipped data, new shape: {self.data.shape}")
        self.drops=[]
