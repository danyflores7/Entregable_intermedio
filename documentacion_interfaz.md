## Interfaz Gráfica de Procesamiento de Imágenes

Se ha desarrollado una Interfaz Gráfica de Usuario (GUI) utilizando **Python** y su librería **PyQt6** para facilitar la aplicación de las distintas transformaciones disponibles en nuestra librería de procesamiento de imágenes (`selec_proc.h`).

### Metodología de Integración
El código en C (`selec_proc.h`) fue encapsulado dentro de un componente `lib_wrapper.c` y compilado como una **Librería Dinámica Compartida** (`.dylib` o `.so` dependiente del SO). Posteriormente, mediante la librería `ctypes` de Python, se enlazaron estas rutinas de manipulación a nivel de bajo nivel, lo que expone eficientemente las funciones de conversión iterativa a la interfaz Python.

### Elementos Gráficos de la Interfaz

La aplicación se compone de los siguientes elementos gráficos, cada uno responsable de detonar un evento o recopilar información para el proceso:

1. **Zona de Arrastre (Drag & Drop):**
   * **Elemento Gráfico:** Un área interactiva de tipo `QLabel` (heredado para funcionalidad de drop).
   * **Función:** Permite al usuario arrastrar y soltar múltiples archivos `.bmp` desde el gestor de archivos hacia la aplicación.
   * **Restricción:** Soporta un máximo de 10 archivos y valida la extensión `.bmp`. Muestra una lista visual de los archivos cargados temporalmente.

2. **Panel de Transformaciones (RadioCheckboxes):**
   * **Elemento Gráfico:** Múltiples botones de verificación `QCheckBox`.
   * **Función:** Definen qué efecto de procesamiento será aplicado al lote completo de imágenes.
   * **Tipos de Eventos (Parámetros C):**
      - *1- Vertical escala de grises:* Llama a `inv_img()`. Acrónimo salida: `_vg`.
      - *2- Vertical escala a colores:* Llama a `inv_img_color()`. Acrónimo salida: `_vc`.
      - *3- Horizontal escala de grises:* Llama a `inv_img_grey_horizontal()`. Acrónimo salida: `_hg`.
      - *4- Horizontal escala a colores:* Llama a `inv_img_color_horizontal()`. Acrónimo salida: `_hc`.
      - *5- Desenfoque escala de grises:* Llama a `desenfoque_grey()`. Acrónimo salida: `_dg`. Requiere validación de kernel.
      - *6- Desenfoque escala a colores:* Llama a `desenfoque()`. Acrónimo salida: `_dc`. Requiere validación de kernel.

3. **Cuadros de Texto del Kernel (Input Validators):**
   * **Elemento Gráfico:** Dos elementos `QLineEdit` anexos a las opciones de desenfoque.
   * **Función:** Determina el tamaño del 'kernel' para los desenfoques.
   * **Restricción:** Cuenta con un `QIntValidator` modificado en Python que arroja advertencias si el usuario no introduce un número **impar y positivo**, garantizando la estabilidad de la matriz de desenfoque de C.

4. **Botón "Todas":**
   * **Elemento Gráfico:** Botón interactivo `QPushButton`.
   * **Función:** Alterna la selección masiva de todas las casillas de transformación. Garantizando una selección rápida de los 6 procesos.

5. **Botón "Ejecutar":**
   * **Elemento Gráfico:** Botón interactivo principal `QPushButton`.
   * **Función:** Actúa como detonador (Trigger) principal de la aplicación.
   * **Acciones asociadas:** 
      1. Verifica que existan archivos cargados.
      2. Valida la integridad del valor de los "kernels".
      3. Inicia un contador de tiempo (`time.time()`).
      4. Ejecuta un ciclo iterativo que recorre cada imagen, aplicando cada filtro que la UI tenga marcado activo mediante las llamadas en C (`ctypes`).
      5. Detiene el reloj, formatea el tiempo y rellena los textboxes de solo lectura con el resultado estadístico de ejecución empírica.

6. **Área de Recapitulación (Read-Only fields):**
   * **Elemento Gráfico:** Entradas `QLineEdit` configuradas como `ReadOnly`.
   * **Función:** Retornan al usuario la ruta absoluta (relativa a `./img/`) del resultado total, además de los milisegundos exactos que tomó el proceso (`Tiempo de ejecución`).

7. **Menú de Información (Acerca de):**
   * **Elemento Gráfico:** Barra superior `QMenuBar` conectada a un diálogo estricto `QDialog`.
   * **Función:** Presenta de manera modal el nombre de los participantes y el banner del ITESM, bloqueando temporalmente interacciones con la UI principal por seguridad hasta ser cerrado.

### [ESPACIO PARA VIDEO DEMOSTRATIVO]
*< Inserte aquí el enlace local o de YouTube al video demostrativo requerido por la rúbrica >*
