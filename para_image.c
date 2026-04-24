#include "selec_proc.h"
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
  FILE *fptr;
  char data[80] = "arcl.txt";

  // Crear archivo de texto de ejemplo
  fptr = fopen(data, "w");
  if (fptr == NULL) {
    printf("Error al crear arcl.txt\n");
    exit(1);
  }
  fprintf(fptr, "Ejemplo escribir\n");
  fprintf(fptr, "Emmanuel Torres Rios\n");
  fclose(fptr);

  /*
   * Se procesarán las imágenes asumiendo que "prueba1.bmp" o similar
   * se encuentran en el folder ./img/
   * El segundo argumento en las inversiones es el path o la imagen de entrada,
   * el primer argumento es la máscara (prefijo de salida).
   */

  // 1. Inversión vertical en escala de grises
  inv_img("inv_1", "./img/img2.bmp");

  // 2. Inversión vertical a color
  inv_img_color("inv_color_1", "./img/img2.bmp");

  // 3. Inversión horizontal en escala de grises
  inv_img_grey_horizontal("espejo", "./img/img2.bmp");

  // 4. Inversión horizontal a color
  inv_img_color_horizontal("espejo_color", "./img/img2.bmp");

  // 5. Desenfoque con kernel definido a color
  desenfoque("./img/img2.bmp", "desenfoque", 27);

  // 6. Desenfoque con kernel definido en escala de grises
  desenfoque_grey("./img/img2.bmp", "desenfoque_gris", 27);

  printf("Procesamiento terminado.\n");
  return 0;
}
