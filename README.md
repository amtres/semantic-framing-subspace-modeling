# LISBETH
## Análisis Computacional de la Representación Mediática mediante Subespacios Semánticos Dinámicos

**Laboratorio - Máster en Metodología de las Ciencias del Comportamiento y de la Salud | UNED**
* **Profesor**: Alejandro Martínez-Mingo
* **Proyecto**: `LISBETH`

---

## Descripción del Proyecto

**Lisbeth** es un sistema de investigación computacional ("Laboratorio") diseñado para analizar la evolución semántica de conceptos en prensa. El sistema combina técnicas avanzadas de **NLP (Modelos Transformadores Adaptados al Dominio)** con **Sociología Digital** para cuantificar cómo un concepto concreto evoluciona en el tiempo. Aunque desarrollado inicialmente para el contexto peruano, la arquitectura es **agnóstica al idioma y país**, permitiendo experimentos en inglés (ej. "Lockdown" en UK), español, o cualquier otro idioma soportado por modelos Hugging Face.

El núcleo metodológico reside en la corrección de la **Anisotropía** del espacio vectorial y el análisis de **Subespacios Semánticos** dinámicos, permitiendo medir matemáticamente conceptos abstractos como la "Deriva Semántica" y la "Proyección Sociológica".

---

## Arquitectura y Fases del Proyecto

El sistema se orquesta mediante una CLI maestra: `pipeline_manager.py`.

### Fase 1: Data Harvesting (Recolector Granular)
*Infraestructura de recolección de noticias resiliente.*

*   **Estrategia "Day x Media"**: A diferencia de scrapers tradicionales que hacen consultas masivas, Lisbeth itera **día por día** y **medio por medio**. Esto bypass-ea las limitaciones de retorno de GDELT (max 250 registros) y asegura una completitud histórica cercana al 100%.
*   **Fuentes Híbridas**: GDELT (primaria), Google News (backup), RSS (tiempo real).
*   **Resiliencia**:
    *   Manejo de "Soft 404s" y contenido renderizado por JS (Client-Side) mediante selectores CSS específicos por dominio (`src/news_harvester/domains.py`).
    *   Fallback automático a la librería `trafilatura` para extracción de texto limpio.

### Fase 2: Infraestructura NLP
*Transformación de texto en tensores matemáticos ajustados.*

#### 2.1 Model Management
El sistema soporta cualquier modelo de Hugging Face, pero está optimizado para modelos monolingües en español:
*   **`PlanTL-GOB-ES/roberta-large-bne`**: SOTA (State of the Art) entrenado por la Biblioteca Nacional de España.
*   **`dccuchile/bert-base-spanish-wwm-uncased`** (BETO): Alternativa robusta y ligera.

#### 2.2 DAPT (Domain-Adaptive Pretraining)
Antes de extraer embeddings, el modelo base se somete a un "re-entrenamiento" ligero (**DAPT**) utilizando el corpus recolectado en Fase 1.
*   **Por qué**: Un modelo genérico no entiende ciertos términos concretos del contexto del estudio. Por ejemplo, que "Yapear" es un verbo o que "Plin" es un competidor, no un sonido.
*   **Parámetros**:
    *   MLM (Masked Language Modeling): Se ocultan aleatoriamente palabras del corpus peruano y el modelo aprende a predecirlas.
    *   Epochs: Configurable (default 3).

#### 2.3 Extracción de Embeddings Contextuales
Para cada mención de la palabra clave (ej. "Yape"):
1.  **Tokenización**: Se localiza la palabra en la oración. Si se fragmenta en sub-tokens (`['Yap', '##ear']`), se aplica **Mean Pooling** para obtener un único vector.
2.  **Layer Strategy**: Se extraen las activaciones ocultas.
    *   **`penultimate`**: La capa anterior a la última (mejor para representaciones geométricas generales).
    *   **`last4_concat`**: Concatenación de las últimas 4 capas (4096 dims para RoBERTa-large), capturando matices sintácticos y semánticos profundos.

### Fase 3: Análisis de Subespacios (El "Laboratorio Matemático")
*Donde ocurre la magia sociológica.*

#### 3.1 Dual Anisotropy Correction
Los modelos de lenguaje sufren de "Anisotropía": todos los vectores tienden a ocupar un cono estrecho en el espacio, distorsionando las distancias (coseno).
Lisbeth implementa un protocolo estricto de comparación:
1.  **RAW (Crudo)**: Embeddings tal cual salen del modelo.
2.  **CORRECTED (Corregido)**: Se calcula el **Vector Medio Global** ($\mu_{global}$) de todo el corpus y se resta de cada embedding ($v' = v - \mu_{global}$). Esto "centra" la nube de puntos y revela la verdadera estructura semántica interna. Otros tipos de corrección de la Anisontropía se aplicarán en futuras actualizaciones del proyecto.

#### 3.2 Subespacios Dinámicos
Se agrupan los embeddings en **Ventanas Deslizantes** (ej. Trimestrales) y se aplica **SVD (Singular Value Decomposition)** para hallar los ejes principales de significado en ese periodo.

#### 3.3 Métricas
*   **Semantic Drift**: Distancia Grassmanniana entre el subespacio del tiempo $t$ y el tiempo $t+1$. Mide cuánto ha cambiado el significado.
*   **Entropía**: Dispersión de los valores singulares. Alta entropía = Significado difuso/polisémico.
*   **Proyección de Anclas**: Se definen vectores teóricos (ej. "Seguridad", "Comunidad") y se mide matemáticamente cuánto se acerca el concepto objetivo a ellos.

### Fase 4: Reportes Automáticos
Generación de Notebooks y Gráficos (Heatmaps, Series Temporales) que comparan visualmente las condiciones RAW vs CORRECTED para validar los hallazgos.

---

## Guía Exhaustiva de Parámetros y Ejecución

El script `pipeline_manager.py` es el punto de entrada único.

### 0. Configuración Inicial
```bash
# Definir lista de medios (disponible en repo)
cat data/media_list.csv
# name,domain,type
# elcomercio,elcomercio.pe,national
# ...
```

### 1. Descarga de Modelos
Pre-descarga los modelos para evitar latencia o errores de red durante el proceso.
```bash
python pipeline_manager.py phase2 download-models \
    --models "dccuchile/bert-base-spanish-wwm-uncased" "PlanTL-GOB-ES/roberta-large-bne"
```

### 2. Fase 1: Recolección (Harvesting)
**Parámetros Clave**:
*   `--pipeline granular`: (Implícito en lógica interna) Activa el loop "Day x Media".
*   `--media-list`: Ruta al CSV de medios. Si se omite, busca en todo GDELT (menos exhaustivo).
*   `--keyword`: Palabras a rastrear.

```bash
# Ejemplo Perú (Default)
python pipeline_manager.py phase1 \
    --keyword "Yape" "Yapear" \
    --from 2020-01-01 --to 2021-01-01 \
    --media-list data/media_list.csv \
    --output data/raw_news_2020.csv

# Ejemplo Reino Unido (UK)
python pipeline_manager.py phase1 \
    --keyword "lockdown" \
    --from 2020-03-01 --to 2020-06-30 \
    --country UK \
    --media-list english_experiment/media_list.csv \
    --output english_experiment/news_lockdown.csv
```

### 3. Fase 2: Procesamiento NLP

#### Paso 3.1: DAPT (Opcional pero Recomendado)
Entrena el modelo base sobre tu data.
*   `--model`: Modelo base de HuggingFace.
*   `--epochs`: 3 suele ser suficiente para adaptación ligera.

```bash
python pipeline_manager.py phase2 dapt \
    --data data/raw_news_2020.csv \
    --output models/lisbeth-adapted-2020 \
    --model "dccuchile/bert-base-spanish-wwm-uncased" \
    --epochs 3
```

#### Paso 3.2: Extracción
Genera el dataset vectorial.
*   `--dapt_model`: Ruta al modelo entrenado en 3.1.
*   `--model`: Modelo base (se usa para generar la línea base comparativa).

```bash
python pipeline_manager.py phase2 extract \
    --data_dir data/raw_news_dir_2020 \
    --output data/embeddings_2020.csv \
    --model "dccuchile/bert-base-spanish-wwm-uncased" \
    --dapt_model models/lisbeth-adapted-2020
```

### 4. Fase 3: Análisis de Subespacios
Ejecuta el cálculo masivo de métricas. Soporta configuración dinámica de modelos y anclas.
*   `--anchors`: JSON con definiciones de dimensiones (opcional).
*   `--baseline-model`: Modelo base para alineación.
*   `--dapt-model`: Modelo adaptado.
*   `--window-months`: Tamaño de la ventana deslizante.

```bash
# Ejemplo estándar
python pipeline_manager.py phase3 \
    --input data/embeddings_2020.csv \
    --output-dir results/analysis_2020

# Ejemplo Avanzado (Experimento en Inglés / Otra Configuración)
python pipeline_manager.py phase3 \
    --input english_experiment/embeddings.csv \
    --output-dir english_experiment/results \
    --baseline-model "roberta-base" \
    --dapt-model "english_experiment/models/dapt" \
    --anchors "english_experiment/anchors.json" \
    --window-months 1
```

### 5. Fase 4: Reporte
Genera el entregable final.
*   Crea un Notebook de Jupyter (`report.ipynb`) en la carpeta de destino con todas las gráficas pre-cargadas.

```bash
python pipeline_manager.py phase4 \
    --input results/analysis_2020/phase3_results.csv \
    --output_dir results/final_report_2020
```

---

## 📂 Estructura del Repositorio

```
LISBETH/
├── academic/               # Reportes y notebooks metodológicos
├── data/                   # Datos (Gitignored, salvo media_list.csv)
│   └── media_list.csv      # Catálogo de medios
├── notebooks/              # Demos interactivos y EDA
├── models/                 # Modelos (Gitignored)
├── scripts/                # Scripts de utilidad
├── tools/                  # Herramientas de diagnóstico
├── src/                    # Código Fuente
│   ├── news_harvester/     # Lógica scraping (Domains, Selectors)
│   ├── nlp/                # Lógica DAPT y tensores
│   ├── subspace_analysis/  # Matemáticas (SVD, Grassman, Procrustes)
│   └── reporting/          # Lógica de generación de reportes
├── pipeline_manager.py     # CLI Maestro
└── README.md               # Este archivo
```

## Data storage and backups

- This project repository was cloned and published to a **private GitHub repository** to avoid losing progress.
- We push and version-control **all project files except the large COVID broad dataset** outputs.
- The **MH-strict dataset** is stored in this repository:
  - `data/interim/datasets/spain_covidMHstrict_2020-03_2021-03_ALL.txt`
- The **COVID broad (ALL) dataset** is **not pushed to GitHub** (large files). It is backed up as a ZIP in **Google Drive** (TFG data backup folder).

Notes:
- Large harvesting outputs are ignored via `.gitignore` to prevent GitHub push issues (>100MB).

---
**Lisbeth v2.0 - Enero 2026**
