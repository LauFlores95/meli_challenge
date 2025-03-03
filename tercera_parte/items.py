from functions import *


""" 
Mejoras a lo propuesto:

1. A la hora de definir el limit en la URL del servicio público de MercadoLibre, se podría establecer una lógica que permita completar los faltantes de items pertenecientes a un término. Por ejemplo, si defino dos términos 'Google Tv' y 'Apple TV', 
junto con un abarrida total de 100 items, actualmente se establece una correspondencia de 50 items a cada término. Si en Google Tv, se encuentran solo 22 y en Apple TV se encuentran los 50, el total de items  encontrados es 77 != 100. Posibles soluciones:
    1.1 Consensuar una regla de negocio que permita este "faltante" de datos.
    1.2 Establecer que los faltantes de un término pasen a ser parte de la busqueda del siguiente
        término.

2. Se puede establecer un parámetro que indique si se quiere hacer una barrida sobre todos los términos indicados o si solamente se desea buscar/actualizar un set de términos.

3. Integrar un sistema de logs que disponibilice un .log (con la libreria logging) que reemplaze los prints.

Contexto:
Se desea realizar un estudio sobre el estado de situación de N artículos presentes en X términos, para saber como es la distribución geográfica, precios y condiciones (como grarantía) de los puntos de venta de este tipo de los mismos. Por eso
en base a la información extraída de los servicios públicos de MercadoLibre, se decide definir un CSV con esta información para un posterior tratamiento/desarrollo.
"""



if __name__ == '__main__':
    # Cantidad de items que se desean buscar.
    cant_items_por_termino = 237

    # A los terminos que estan a modo de ejemplo, le agrego algunos extraidos desde los 
    # en los recomendados de MercadoLibre, seccion "Mas vendido"
    terminos_list = ['Google Home','Apple TV','Amazon Fire TV', 'Google TV', 'Roku', 'Tv Stick']
    search_list = get_search_info(terminos_list, cant_items_por_termino)
    item_list = get_item_info(search_list)

    output_path = 'output'
    file_name = 'item_info.csv'
    item_parser(item_list, output_path, file_name)
