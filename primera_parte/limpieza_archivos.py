import os
import pandas as pd
import csv
import xlrd

def data_first_row(csv_path: str):
    # Leo los archivos
    with open(csv_path, 'r', encoding='utf-8') as f:
        csv_data = csv.reader(f)
        # Me devuelve listas, asi que parseo un poco y filtro para encontrar la que empieza con "Country Name", que es la que contiene el head.
        for i, fila in enumerate(csv_data):
            fila_cleansed = str(fila).replace('[', '').replace(']', '')
            if 'Country Name' in fila_cleansed:
                return i
    return -1


path_archivo_csv = './input/world_bank/servidores_internet_seguros_anual.csv'

# listo los archivos
input = './input/'
intermediate = './intermediate/'
output_path = './output'

if not os.path.exists('output'):
    os.makedirs('output')
if not os.path.exists('intermediate'):
    os.makedirs('intermediate')

source_folders = os.listdir('input')

# Busco la columna donde empieza el contenido:
for folder in source_folders:


    if folder == 'world_bank':
        file_list = os.listdir(input + '/' + folder)
        for files in file_list:
            full_input_file_path = input + '/' + folder + '/' + files
            first_row = data_first_row(full_input_file_path)
            print(files)
            dfData = pd.read_csv(full_input_file_path, skiprows= first_row)
            dfData = dfData.iloc[first_row:]
            dfData.to_excel(output_path + '/world_bank_' + files.split('.')[0] + '.xlsx', index = None, engine = 'openpyxl')

    if folder == 'indec':
        sheet_names = ['Cuadro 1','Cuadro 2','Cuadro 3','Cuadro 4','Cuadro 5',]
        file_list = os.listdir(input + '/' + folder)
        for files in file_list:
            # Lectura y split de archivo en base a las hojas
            full_input_file_path = input + '/' + folder + '/' + files
            for sheet_name in sheet_names:
                dfData = pd.ExcelFile(full_input_file_path, engine = 'xlrd')
                dfData = pd.read_excel(dfData, sheet_name = sheet_name)
                # Almaceno la info en etapa intermedia
                intermediate_path = f'./intermediate/indec_'
                dfData.to_excel(intermediate_path + files.split('.')[0] + f'_{sheet_name}.xlsx', index=None)

# for folder in source_folders: 
