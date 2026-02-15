import pandas as pd
import numpy as np
import ast

# CONFIGURACIÓN
FILE_PATH = r".\data\interim\embeddings\spain_covidMHstrict_occurrences_2020-03_2021-03_CLEANED.csv"

# FECHAS DE LA VENTANA 7 (Aprox: Septiembre, Octubre, Noviembre 2020)
START_DATE = "2020-09"
END_DATE = "2020-11" 

print(f"🕵️ CARGANDO DATOS PARA INSPECCIÓN...")
df = pd.read_csv(FILE_PATH)
df['date'] = pd.to_datetime(df['year_month'])

# FILTRAR SOLO VENTANA 7
mask = (df['date'] >= START_DATE) & (df['date'] < END_DATE)
window_df = df[mask].copy()

print(f"📅 Ventana 7 ({START_DATE} a {END_DATE})")
print(f"📊 Filas encontradas: {len(window_df)}")

if len(window_df) == 0:
    print("❌ ERROR CRÍTICO: No hay datos en esta ventana.")
    exit()

# RECOLECTAR EMBEDDINGS
# Buscamos columnas que parezcan embeddings
emb_cols = [c for c in df.columns if "embedding" in c]
print(f"🧬 Columnas de embeddings: {emb_cols}")

matrices = []
for col in emb_cols:
    # Convertir string "[0.1, 0.2]" a lista real
    # Nota: Si ya es objeto, ast.literal_eval podría fallar, por eso el try
    try:
        vals = window_df[col].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x).tolist()
    except Exception as e:
        print(f"⚠️ Error parseando columna {col}: {e}")
        continue
        
    mat = np.array(vals)
    matrices.append(mat)
    
    # CHEQUEOS DE SALUD
    has_nan = np.isnan(mat).any()
    has_inf = np.isinf(mat).any()
    
    print(f"   > Columna: {col}")
    print(f"     Shape: {mat.shape}")
    print(f"     Tiene NaNs? {'❌ SÍ' if has_nan else '✅ No'}")
    print(f"     Tiene Infs? {'❌ SÍ' if has_inf else '✅ No'}")
    
    if has_nan or has_inf:
        print("     🔥 ¡CULPABLE ENCONTRADO! Datos corruptos en esta columna.")

# Chequeo final de consistencia
full_matrix = np.hstack(matrices)
print(f"\n🧩 Matriz Completa Ventana 7: {full_matrix.shape}")
if np.isnan(full_matrix).any():
    print("❌ LA MATRIZ CONTIENE NANS. EL SVD FALLARÁ.")
elif np.isinf(full_matrix).any():
    print("❌ LA MATRIZ CONTIENE INFINITOS. EL SVD FALLARÁ.")
else:
    print("✅ LOS DATOS ESTÁN LIMPIOS. Es un problema puramente matemático (Singularidad).")