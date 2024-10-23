import pandas as pd
from validate_email import validate_email
import numpy as np

# Ruta del archivo CSV intermedio
archivo_csv = 'C:\ProgramData\Jenkins\.jenkins\jobs\PIPELINE_PRUEBAPARCIAL_DEVOPS\clientes.csv'

try:
    data = pd.read_csv(archivo_csv)
    # Leer el archivo CSV    
    data['Validacion1'] = np.where((data.Telefono.astype(str).str.contains('^[9]')) &
        (data['Telefono'].apply(lambda x : len(str(x))) == 9) &
        (data['EmailCliente'].apply(lambda x:validate_email(x))),'Correcto','Incorrecto')
    # Ordenar los datos por nombre
    data_ordenada = data.sort_values(by='NombreCompleto')
    
    # Exportar a Excel
    archivo_excel = 'C:\ProgramData\Jenkins\.jenkins\jobs\PIPELINE_PRUEBAPARCIAL_DEVOPS\clientes_ordenados.xlsx'
    data_ordenada.to_excel(archivo_excel, index=False)
    
    print(f"Datos exportados exitosamente a {archivo_excel}")
    #print(data)
except Exception as e:
    print(f"Error al transformar los datos: {e}")
    
