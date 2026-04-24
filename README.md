# Proyecto de Procesamiento de Imágenes (GUI)

Este proyecto es una aplicación con interfaz gráfica para el procesamiento por lotes de imágenes en formato `.bmp`. Combina la facilidad de uso de una interfaz moderna en **Python (PyQt6)** con la velocidad de ejecución de **C** a nivel backend.

## 🚀 Características
El sistema permite arrastrar y procesar de forma iterativa hasta 10 imágenes a la vez, aplicando las siguientes transformaciones:
1. Inversión vertical (escala de grises y color).
2. Inversión horizontal (escala de grises y color).
3. Desenfoque / Blur (escala de grises y color) mediante ajuste de Kernel.

Al terminar cada proceso, la GUI muestra las estadísticas de tiempo de ejecución (milisegundos) y genera los archivos resultantes en la carpeta `img`.

## 🛠️ Requisitos Previos

Necesitarás tener instalados:
- **Python 3**
- Un compilador de **C** como `gcc`
- **Git** (Para clonar el repositorio)

## 📦 Instalación y Ejecución

Sigue estos pasos para instalar y ejecutar el proyecto desde cero:

### 1. Clonar el Repositorio
```bash
git clone https://github.com/danyflores7/Entregable_intermedio.git
cd Entregable_intermedio
```

### 2. Compilar la Librería de C
Para que Python pueda interactuar con el código de alto rendimiento, debes generar la librería dinámica compartida:

**En macOS:**
```bash
gcc -shared -o libprocesamiento.dylib -fPIC lib_wrapper.c
```

**En Linux:**
```bash
gcc -shared -o libprocesamiento.so -fPIC lib_wrapper.c
```

**En Windows (Git Bash o MinGW):**
```bash
gcc -shared -o libprocesamiento.dll -fPIC lib_wrapper.c
```

### 3. Crear el Entorno Virtual de Python e Instalar Dependencias
Se recomienda el uso de un entorno virtual para evitar conflictos con otras versiones de librerías en tu sistema (especialmente si usas distribuciones como Conda).

```bash
# Crear el entorno virtual (solo la primera vez)
python3 -m venv venv

# Activar el entorno (macOS y Linux)
source venv/bin/activate
# En Windows: venv\Scripts\activate

# Instalar PyQt6
pip install PyQt6
```

### 4. Ejecutar el Programa
Asegúrate de que el entorno virtual esté activado y ejecuta:
```bash
python main.py
```

## 🎮 Cómo usar la Interfaz
1. **Cargar:** Arrastra archivos `.bmp` al panel gris (máximo 10 archivos).
2. **Seleccionar Filtros:** Marca las casillas de los filtros que quieras procesar. Si marcas los filtros de "Desenfoque", deberás especificar un tamaño de **Kernel** que debe ser un **número entero, positivo e impar** (ej. 3, 5, 11).
3. **Ejecutar:** Presiona el botón "Ejecutar" en la esquina inferior derecha.
4. **Resultados:** Las imágenes procesadas se guardarán en la carpeta `/img` con un sufijo asociado (ej: `_vg` para vertical gris). El panel izquierdo te indicará el tiempo de ejecución.

## 📝 Notas Adicionales
- Las imágenes originales pesadas o cargadas temporalmente **no** se suben al repositorio.
- La extensión `.dylib` / `.so` no se rastrea en el control de versiones por diseño. Es necesario compilarla en cada nuevo equipo.
