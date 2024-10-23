from validate_email import validate_email
import numpy as np
import pandas as pd

def detectar_duplicados(df, columna, keep='last'):
    """Detecta duplicados en una columna específica de un DataFrame.

    Args:
        df: DataFrame de entrada.
        columna: Nombre de la columna a verificar.
        keep: 'first' para marcar los primeros como duplicados,
              'last' para marcar los últimos como duplicados.

    Returns:
        Series con el valor 'Duplicado' si hay duplicados, 'Nuevo' si no.
    """
    return np.where(df[columna].duplicated(keep=keep), 'Duplicado', 'Nuevo')

# Ruta del archivo CSV intermedio
archivo_csv = 'C:\\ProgramData\\Jenkins\\.jenkins\\jobs\\PIPELINE_TPARCIAL\\clientes.csv'

try:
    data = pd.read_csv(archivo_csv)
    # Leer el archivo CSV    
    data['Validacion1'] = np.where((data['Telefono'].apply(lambda x : len(str(x))) != 9) &
                                 (data['Email Cliente'].apply(lambda x: not validate_email(x))),'No Gestionable','Gestionable')

    # Combinar fecha y hora
    data['FechaHora'] = pd.to_datetime(data['Fecha Solicitud'] + ' ' + data['Hora Solicitud'], format='%d/%m/%Y %H:%M:%S')

    # Ordenar por fecha y hora descendente
    data = data.sort_values(by='FechaHora', ascending=False)

    # Detectar duplicados en el teléfono considerando la fecha y hora
    data['Estado Ingreso'] = detectar_duplicados(data, 'Telefono', 'last')

    # Ordenar los datos por nombre
    data_ordenada = data.sort_values(by='Nombre Completo')

    # Exportar a Excel
    archivo_excel = 'C:\\ProgramData\\Jenkins\\.jenkins\\jobs\\PIPELINE_TPARCIAL\\clientes_ordenados.xlsx'
    data_ordenada.to_excel(archivo_excel, index=False)

    data = pd.read_excel(archivo_excel)
  # Añadir columna Estado Lead  
    data['Estado Lead'] = np.where((data['Validacion1'] == 'Gestionable') &
                                 (data['Estado Ingreso'] =='Nuevo'),'Asignar','No asignar')
    # Ordenar los datos por nombre
    data_fasignar = data.sort_values(by='Nombre Completo')
    # Crear columna Cod Vend
    data_fasignar['Codigo_vendedor'] = ""
    # Exportar a Excel
    archivo2_csv = 'C:\\ProgramData\\Jenkins\\.jenkins\\jobs\\PIPELINE_TPARCIAL\\clientes_EstadoLead.csv'
    data_fasignar.to_csv(archivo2_csv, index=False)
    print(f"Datos exportados exitosamente a {archivo_csv}")
except Exception as e:
    print(f"Error al transformar los datos: {e}")
