import os
import math 
import requests
import sys 
import pandas as pd
from datetime import datetime

# Responde al punto 1
def get_search_info(lista_term: list, cant_items: int):
    """
    Función que se encarga de hacer la búsqueda de items usando la API de MercadoLibre con un offset dinámico para evitar tener el problema de los límites
    del servicio público.
    args:
        lista_term: Lista con los nombres de cada término que se desee buscar.
        cant_items: Cantidad de items que se desean buscar.
    return:
        item_list: Lista de jsons con los resultado de la búsqueda.

    docs:
        Offset: https://developers.mercadolibre.com.ar/devsite/paging-results-global-selling#Offset
        Limit: https://developers.mercadolibre.com.ar/devsite/paging-results-global-selling#Limit
    """

    item_list = []

    # Verifico si la cantidad de items a buscar tiene sentido
    if cant_items < 0:
        print(f'ERROR {datetime.now()} - Se ha intentado buscar un número inválido de items.')
        sys.exit(1)

    # Defino un numero de items a barrer en base a la cantidad de terminos. Si se quieren buscar 150 y son 3 terminos, cada uno deberia traer, al menos, 50
    cant_items_term = math.ceil(cant_items / (len(lista_term)))
    cant_items_requests = math.ceil(cant_items_term / 50)
    print(f'INFO {datetime.now()} - Se van a buscar {cant_items_term} por cada término.')


    print(f'INFO {datetime.now()} - Se tienen {len(lista_term)} terminos a buscar, por lo que se buscaran, al menos, {cant_items_term} por cada uno.')

    # Bucle para realizar las requests con un offset dinámico y limite=50 (limite publico).
    for term in lista_term:
        limit = cant_items_term

        print(f'INFO {datetime.now()} - Comienzo de la request para el item: {term}')

        # Bucle encargado de realizar las n request por cada término.
        for i in range(0,cant_items_requests,1): 
            
            # Agrego logica para definir el limit dinamico con mayor exactitud. Podría pensarse una forma distinta para evitar usar tantos ifs, pero como
            # Se que el servicio público permite hasta 50 (número estático), lo dejo así.
            if limit < 50 and limit >0:
                limit_filter = limit 
                limit -= 50
            elif limit >= 50:
                limit_filter = 50
                limit -= 50

            # Defino el Offset: si el limit es mayor a 50, se setea limit = 50 y no genera problema con el servicio público.
            offset = int(i * 50)
            url = f"https://api.mercadolibre.com/sites/MLA/search?q={term}&limit={limit_filter}&offset={offset}"
            
            # Ejecución de la request.
            try:
                response = requests.get(url)
                data = response.json()
                # Me quedo con la key "results" que contiene la info de los productos.
                resultados = data['results']

                # A la lista vacia le agrego los jsons.
                # Utilizo este método para que, a la lista, se le agreguen los elementos y siga siendo una sola lista (y que no se agreguen listas).
                item_list.extend(resultados)

                # ## Escribo el output para analisis.
                # with open('resultados.json', 'w', encoding='utf-8') as f:
                #     f.write(str(item_list))
                #     f.close

                if len(resultados) == 0:
                    print(f'INFO {datetime.now()} - La request numero: {i + 1} se realizó correctamente y se registraron {len(resultados)} resultados.')
                    break
                else:
                    print(f'INFO {datetime.now()} - La request numero: {i + 1} se realizó correctamente y se registraron {len(resultados)} resultados.')

            except Exception as e:
                print(f'ERROR {datetime.now()} - La ejecución de la request no se realizó correctamente.\n {e}')
                sys.exit(1)

    if len(item_list) != 0:
        print(f'INFO {datetime.now()} - Se han encontrado {len(item_list)} resultados.')
    else:
        print(f'WARN {datetime.now()} - No han encontrado resultados.')           

    if len(item_list) <= cant_items:
        print(f'INFO {datetime.now()} - Al menos uno de los términos no cuenta con los items esperados. Cantidad encontrada: {len(item_list)}, cantidad buscada: {cant_items}')
    

    return item_list

# Responde al punto 2
def get_item_info(search_list: list):
    """
    Esta funcion toma como argumento una lista de jsons y obtiene el ID de cada item que esta incluya para, posteriormente, buscar la información de los Items en 
    el servicio de MercadoLibre.

    args:
        search_list: Lista de jsons donde se tienen los resultados de la búsqueda.
    
    returns:
        item_list: Lista de listas que contiene la información (en jsons) de cada item buscado.
    """
    item_list = []

    # Del resultado de la busqueda, filtro solamente los ID de los productos.
    for i in range(0, len(search_list), 1):
        # Busco solos los ids de los items.
        item_id = search_list[i]['id']
        url = f'https://api.mercadolibre.com/items/{item_id}'
        
        # Realizo la request del item
        response = requests.get(url)
        data = response.json()
        # A la lista vacia le agrego los jsons para generar una lista de elementos (en este caso, lista de jsons)
        item_list.append(data)
    
    return item_list

# Responde al punto 3
def col_rename(df: pd.DataFrame, columns_dict: dict):
    """
    Función que reemplaza los nombres de las columnas de un DataFrame de Pandas.

    args:
        df: DataFrame al que se le desea cambiar el schema (a nivel nombre).
        columns_dict: Diccionario con el mapeo de nombres, donde las keys corresponden a los viejos valores y los values a los nuevos.

    returns:
        df: DataFrame de Pandas con las modificaciones indicadas.
    """
    # Cambio los nombres modificados:
    for key in columns_dict:
        if key in df.columns:
            df.rename(columns={key: columns_dict[key]}, inplace=True)
    
    return df

# Responde al punto 3
def item_parser(item_list: list, output_path: str, file_name: str):
    """
    Funcion que toma una lista de items, entregada por el servicio de MercadoLibre, y se queda con la información que se desee.
    En este caso, se desea limpiar la información con ciertos campos.
    
    args:
        item_list: Lista de items que se obtiene a partir de utilizar el servicio mencionado anteriormente.
        output_path: Path de salida donde se quiere disponibilizar el archivo.
        file_name: String con el nombre de archivo que desea tener a la salida.

    returns
        None: No retorna un objeto en sí, sino que se realiza la escritura de archivos dentro del cuerpo del código.
    """

    dfData = pd.DataFrame(item_list, index=None)
    # Filtro las columnas de interes
    columns = ['id', 'site_id', 'title', 'seller_id', 'category_id', 'official_store_id', 'price', 'base_price', 'original_price', 'currency_id', 'initial_quantity', 'condition', 'international_delivery_mode', 'seller_address', 'status', 'warranty', 'catalog_product_id', 'domain_id', 'date_created', 'last_updated']
    dfData = dfData[columns]

    # Transormación sobre el DataFrame:
    # De la columna seller_address obtengo solamente el state_id
    dfData['seller_address'] = dfData['seller_address'].apply(lambda x: x['state']['id'])

    # Renombramiento de columnas en caso de que se requiera:
    col_name_changes = {'seller_address': 'seller_location_id'}
    dfData = col_rename(dfData, col_name_changes)

    # Valido schema
    column_types = {'id': 'object', 'site_id': 'object', 'title': 'object', 'seller_id': 'int64', 'category_id': 'object', 'official_store_id': 'float64', 'price': 'int64', 'base_price': 'int64', 'original_price': 'object', 'currency_id': 'object', 'initial_quantity': 'int64', 'sale_terms': 'object', 'buying_mode': 'object', 'listing_type_id': 'object', 'condition': 'object', 'permalink': 'object', 'thumbnail_id': 'object', 'thumbnail': 'object', 'pictures': 'object', 'video_id': 'object', 'descriptions': 'object', 'accepts_mercadopago': 'bool', 'non_mercado_pago_payment_methods': 'object', 'shipping': 'object', 'international_delivery_mode': 'object', 'seller_location_id': 'object', 'seller_contact': 'object', 'location': 'object', 'coverage_areas': 'object', 'attributes': 'object', 'listing_source': 'object', 'variations': 'object', 'status': 'object', 'sub_status': 'object', 'tags': 'object', 'warranty': 'object', 'catalog_product_id': 'object', 'domain_id': 'object', 'parent_item_id': 'object', 'deal_ids': 'object', 'automatic_relist': 'bool', 'date_created': 'object', 'last_updated': 'object', 'health': 'float64', 'catalog_listing': 'bool'}
    try:
        for column in dfData.columns:
            dfData[column] = dfData[column].astype(column_types[column])
        print(f'INFO {datetime.now()} - Se verifircaron los tipos de datos satisfactoriamente.')

    except Exception as e:
        print(f'ERROR {datetime.now()} - Se ha encontrado un error de tipos. {e}')


    if not os.path.exists(output_path):
        os.makedirs(output_path)

    hoy = datetime.today().strftime('%Y-%m-%d')

    file_name = file_name.split('.')[0] + f'_{hoy}.' + file_name.split('.')[1]
    output_path = output_path + '/' + file_name
    print(file_name)

    try:
        dfData.to_csv(output_path, encoding='utf-8', index=False)
        print(f'INFO {datetime.now()} - Se ha almacenado el archivo .csv con la información de los items en {output_path}.')
    except Exception as e:
        print(f'ERROR {datetime.now()} - No se ha almacenado el archivo .csv en la ruta especificada.')
    
    return None



