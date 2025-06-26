import pandas as pd
import openpyxl

# Leer el archivo Excel
try:
    # Primero, ver las hojas disponibles
    xlsx_file = pd.ExcelFile('DB_Rutas.xlsx')
    print("Hojas disponibles:", xlsx_file.sheet_names)
    
    # Leer la primera hoja
    df = pd.read_excel('DB_Rutas.xlsx', sheet_name=0)
    
    print("\nPrimeras 10 filas:")
    print(df.head(10))
    
    print(f"\nColumnas ({len(df.columns)}):")
    for i, col in enumerate(df.columns):
        print(f"{i+1}. {col}")
    
    print(f"\nCantidad de filas: {len(df)}")
    
    print("\nTipos de datos:")
    print(df.dtypes)
    
    # Ver valores únicos de algunas columnas clave si existen
    possible_contractor_columns = [col for col in df.columns if any(word in col.lower() for word in ['contrat', 'nombre', 'repartidor', 'vendedor'])]
    if possible_contractor_columns:
        print(f"\nPosibles columnas de contratistas: {possible_contractor_columns}")
        for col in possible_contractor_columns[:3]:  # Solo primeras 3
            unique_values = df[col].unique()[:10]  # Solo primeros 10 valores únicos
            print(f"\nValores únicos en '{col}' (primeros 10):")
            print(unique_values)

except Exception as e:
    print(f"Error: {e}")
