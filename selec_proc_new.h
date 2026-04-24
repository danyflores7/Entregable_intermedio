#ifndef SELEC_PROC_H
#define SELEC_PROC_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Función itoa proporcionada en el ejemplo
extern void itoa(int N, char *str) {
    int i = 0;
    int sign = N;
    if (N < 0) N = -N;
    do {
        str[i++] = N % 10 + '0';
        N /= 10;
    } while (N > 0);
    if (sign < 0) str[i++] = '-';
    str[i] = '\0';
    for (int j = 0, k = i - 1; j < k; j++, k--) {
        char temp = str[j];
        str[j] = str[k];
        str[k] = temp;
    }
}

// 1. Inversión de imagen vertical en escala de grises
extern void inv_img(char mask[10], char path[80]) {
    FILE *image, *outputImage;
    char add_char[80] = "./img/";
    strcat(add_char, mask);
    strcat(add_char, ".bmp");
    
    image = fopen(path, "rb");
    if(!image) { printf("Error: No se pudo abrir %s\n", path); return; }
    outputImage = fopen(add_char, "wb");
    
    unsigned char header[54];
    fread(header, sizeof(unsigned char), 54, image);
    fwrite(header, sizeof(unsigned char), 54, outputImage);
    
    int width = *(int*)&header[18];
    int height = *(int*)&header[22];
    int row_padded = (width * bytes_per_pixel + 3) & (~3);
    
    unsigned char** rows = (unsigned char**)malloc(height * sizeof(unsigned char*));
    for (int i = 0; i < height; i++) {
        rows[i] = (unsigned char*)malloc(row_padded);
        fread(rows[i], sizeof(unsigned char), row_padded, image);
    }
    
    // Invertimos verticalmente leyendo desde el último renglón al primero
    for (int y = height - 1; y >= 0; y--) {
        unsigned char* out_row = (unsigned char*)malloc(row_padded);
        for(int p = 0; p < row_padded; p++) out_row[p] = rows[y][p]; // copiar padding
        
        for (int x = 0; x < width; x++) {
            int idx = x * bytes_per_pixel;
            unsigned char b = rows[y][idx];
            unsigned char g = rows[y][idx+1];
            unsigned char r = rows[y][idx+2];
            unsigned char pixel = (unsigned char)(0.21 * r + 0.72 * g + 0.07 * b);
            out_row[idx] = pixel;
            out_row[idx+1] = pixel;
            out_row[idx+2] = pixel;
        }
        fwrite(out_row, sizeof(unsigned char), row_padded, outputImage);
        free(out_row);
    }
    
    for (int i = 0; i < height; i++) free(rows[i]);
    free(rows);
    fclose(image);
    fclose(outputImage);
    printf("Imagen generada: %s\n", add_char);
}

// 2. Inversión de imagen vertical a color
extern void inv_img_color(char mask[10], char path[80]) {
    FILE *image, *outputImage;
    char add_char[80] = "./img/";
    strcat(add_char, mask);
    strcat(add_char, ".bmp");
    
    image = fopen(path, "rb");
    if(!image) { printf("Error: No se pudo abrir %s\n", path); return; }
    outputImage = fopen(add_char, "wb");
    
    unsigned char header[54];
    fread(header, sizeof(unsigned char), 54, image);
    fwrite(header, sizeof(unsigned char), 54, outputImage);
    
    int width = *(int*)&header[18];
    int height = *(int*)&header[22];
    int row_padded = (width * bytes_per_pixel + 3) & (~3);
    
    unsigned char** rows = (unsigned char**)malloc(height * sizeof(unsigned char*));
    for (int i = 0; i < height; i++) {
        rows[i] = (unsigned char*)malloc(row_padded);
        fread(rows[i], sizeof(unsigned char), row_padded, image);
    }
    
    for (int y = height - 1; y >= 0; y--) { 
        fwrite(rows[y], sizeof(unsigned char), row_padded, outputImage);
    }
    
    for (int i = 0; i < height; i++) free(rows[i]);
    free(rows);
    fclose(image);
    fclose(outputImage);
    printf("Imagen generada: %s\n", add_char);
}

// 3. Inversión de imagen horizontal en escala de grises
extern void inv_img_grey_horizontal(char mask[10], char path[80]) {
    FILE *image, *outputImage;
    char add_char[80] = "./img/";
    strcat(add_char, mask);
    strcat(add_char, ".bmp");
    
    image = fopen(path, "rb");
    if(!image) { printf("Error: No se pudo abrir %s\n", path); return; }
    outputImage = fopen(add_char, "wb");
    
    unsigned char header[54];
    fread(header, sizeof(unsigned char), 54, image);
    fwrite(header, sizeof(unsigned char), 54, outputImage);
    
    int width = *(int*)&header[18];
    int height = *(int*)&header[22];
    int row_padded = (width * bytes_per_pixel + 3) & (~3);
    
    unsigned char** rows = (unsigned char**)malloc(height * sizeof(unsigned char*));
    for (int i = 0; i < height; i++) {
        rows[i] = (unsigned char*)malloc(row_padded);
        fread(rows[i], sizeof(unsigned char), row_padded, image);
    }
    
    for (int y = 0; y < height; y++) {
        unsigned char* out_row = (unsigned char*)malloc(row_padded);
        for(int p = 0; p < row_padded; p++) out_row[p] = rows[y][p]; // padding
        
        for (int x = 0; x < width; x++) {
            int orig_idx = x * bytes_per_pixel;
            int new_idx = (width - 1 - x) * 3;
            
            unsigned char b = rows[y][orig_idx];
            unsigned char g = rows[y][orig_idx+1];
            unsigned char r = rows[y][orig_idx+2];
            unsigned char pixel = (unsigned char)(0.21 * r + 0.72 * g + 0.07 * b);
            
            out_row[new_idx] = pixel;
            out_row[new_idx+1] = pixel;
            out_row[new_idx+2] = pixel;
        }
        fwrite(out_row, sizeof(unsigned char), row_padded, outputImage);
        free(out_row);
    }
    
    for (int i = 0; i < height; i++) free(rows[i]);
    free(rows);
    fclose(image);
    fclose(outputImage);
    printf("Imagen generada: %s\n", add_char);
}

// 4. Inversión de imagen horizontal a color
extern void inv_img_color_horizontal(char mask[10], char path[80]) {
    FILE *image, *outputImage;
    char add_char[80] = "./img/";
    strcat(add_char, mask);
    strcat(add_char, ".bmp");
    
    image = fopen(path, "rb");
    if(!image) { printf("Error: No se pudo abrir %s\n", path); return; }
    outputImage = fopen(add_char, "wb");
    
    unsigned char header[54];
    fread(header, sizeof(unsigned char), 54, image);
    fwrite(header, sizeof(unsigned char), 54, outputImage);
    
    int width = *(int*)&header[18];
    int height = *(int*)&header[22];
    int row_padded = (width * bytes_per_pixel + 3) & (~3);
    
    unsigned char** rows = (unsigned char**)malloc(height * sizeof(unsigned char*));
    for (int i = 0; i < height; i++) {
        rows[i] = (unsigned char*)malloc(row_padded);
        fread(rows[i], sizeof(unsigned char), row_padded, image);
    }
    
    for (int y = 0; y < height; y++) {
        unsigned char* out_row = (unsigned char*)malloc(row_padded);
        for(int p = 0; p < row_padded; p++) out_row[p] = rows[y][p]; // padding
        
        for (int x = 0; x < width; x++) {
            int orig_idx = x * bytes_per_pixel;
            int new_idx = (width - 1 - x) * 3;
            out_row[new_idx] = rows[y][orig_idx];
            out_row[new_idx+1] = rows[y][orig_idx+1];
            out_row[new_idx+2] = rows[y][orig_idx+2];
        }
        fwrite(out_row, sizeof(unsigned char), row_padded, outputImage);
        free(out_row);
    }
    
    for (int i = 0; i < height; i++) free(rows[i]);
    free(rows);
    fclose(image);
    fclose(outputImage);
    printf("Imagen generada: %s\n", add_char);
}

// 5. Desenfoque con kernel definido a color
extern void desenfoque(const char* input_path, const char* name_output, int kernel_size) {
    FILE *image, *outputImage;
    char output_path[100] = "./img/";
    strcat(output_path, name_output);
    strcat(output_path, ".bmp");
    
    image = fopen(input_path, "rb");
    if(!image) { printf("Error: No se pudo abrir %s\n", input_path); return; }
    outputImage = fopen(output_path, "wb");
    
    unsigned char header[54];
    fread(header, sizeof(unsigned char), 54, image);
    fwrite(header, sizeof(unsigned char), 54, outputImage);
    
    int width = *(int*)&header[18];
    int height = *(int*)&header[22];
    int row_padded = (width * bytes_per_pixel + 3) & (~3);
    
    unsigned char** input_rows = (unsigned char**)malloc(height * sizeof(unsigned char*));
    unsigned char** output_rows = (unsigned char**)malloc(height * sizeof(unsigned char*));
    unsigned char** temp_rows = (unsigned char**)malloc(height * sizeof(unsigned char*));
    for (int i = 0; i < height; i++) {
        input_rows[i] = (unsigned char*)malloc(row_padded);
        output_rows[i] = (unsigned char*)malloc(row_padded);
        temp_rows[i] = (unsigned char*)malloc(row_padded);
        fread(input_rows[i], sizeof(unsigned char), row_padded, image);
    }
    
    int k = kernel_size / 2;
    // Desenfoque horizontal
    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            int sumB = 0, sumG = 0, sumR = 0, count = 0;
            for (int dx = -k; dx <= k; dx++) {
                int nx = x + dx;
                if (nx >= 0 && nx < width) {
                    int idx = nx * bytes_per_pixel;
                    sumB += input_rows[y][idx];
                    sumG += input_rows[y][idx+1];
                    sumR += input_rows[y][idx+2];
                    count++;
                }
            }
            int index = x * bytes_per_pixel;
            temp_rows[y][index] = sumB / count;
            temp_rows[y][index + 1] = sumG / count;
            temp_rows[y][index + 2] = sumR / count;
        }
        for (int p = width * bytes_per_pixel; p < row_padded; p++) {
            temp_rows[y][p] = input_rows[y][p];
        }
    }
    
    // Desenfoque vertical
    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            int sumB = 0, sumG = 0, sumR = 0, count = 0;
            for (int dy = -k; dy <= k; dy++) {
                int ny = y + dy;
                if (ny >= 0 && ny < height) {
                    int idx = x * bytes_per_pixel;
                    sumB += temp_rows[ny][idx];
                    sumG += temp_rows[ny][idx+1];
                    sumR += temp_rows[ny][idx+2];
                    count++;
                }
            }
            int index = x * bytes_per_pixel;
            output_rows[y][index] = sumB / count;
            output_rows[y][index + 1] = sumG / count;
            output_rows[y][index + 2] = sumR / count;
        }
        for (int p = width * bytes_per_pixel; p < row_padded; p++) {
            output_rows[y][p] = temp_rows[y][p];
        }
    }
    
    for (int i = 0; i < height; i++) {
        fwrite(output_rows[i], sizeof(unsigned char), row_padded, outputImage);
        free(input_rows[i]);
        free(temp_rows[i]);
        free(output_rows[i]);
    }
    
    FILE *outputLog = fopen("output_log.txt", "a");
    if (outputLog) {
        fprintf(outputLog, "Función: desenfoque color, con %s\n", input_path);
        fprintf(outputLog, "Localidades totales leídas: %d\n", width * height);
        fprintf(outputLog, "Localidades totales escritas: %d\n", width * height);
        fprintf(outputLog, "-------------------------------------\n");
        fclose(outputLog);
    }
    
    free(input_rows);
    free(temp_rows);
    free(output_rows);
    fclose(image);
    fclose(outputImage);
    printf("Imagen generada: %s\n", output_path);
}

// 6. Desenfoque con kernel definido en escala de grises
extern void desenfoque_grey(const char* input_path, const char* name_output, int kernel_size) {
    FILE *image, *outputImage;
    char output_path[100] = "./img/";
    strcat(output_path, name_output);
    strcat(output_path, ".bmp");
    
    image = fopen(input_path, "rb");
    if(!image) { printf("Error: No se pudo abrir %s\n", input_path); return; }
    outputImage = fopen(output_path, "wb");
    
    unsigned char header[54];
    fread(header, sizeof(unsigned char), 54, image);
    fwrite(header, sizeof(unsigned char), 54, outputImage);
    
    int width = *(int*)&header[18];
    int height = *(int*)&header[22];
    int row_padded = (width * bytes_per_pixel + 3) & (~3);
    
    unsigned char** input_rows = (unsigned char**)malloc(height * sizeof(unsigned char*));
    unsigned char** output_rows = (unsigned char**)malloc(height * sizeof(unsigned char*));
    unsigned char** temp_rows = (unsigned char**)malloc(height * sizeof(unsigned char*));
    for (int i = 0; i < height; i++) {
        input_rows[i] = (unsigned char*)malloc(row_padded);
        output_rows[i] = (unsigned char*)malloc(row_padded);
        temp_rows[i] = (unsigned char*)malloc(row_padded);
        fread(input_rows[i], sizeof(unsigned char), row_padded, image);
    }
    
    // Primero, convertir todo a escala de grises para el input
    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            int idx = x * bytes_per_pixel;
            unsigned char b = input_rows[y][idx];
            unsigned char g = input_rows[y][idx+1];
            unsigned char r = input_rows[y][idx+2];
            unsigned char pixel = (unsigned char)(0.21 * r + 0.72 * g + 0.07 * b);
            input_rows[y][idx] = pixel;
            input_rows[y][idx+1] = pixel;
            input_rows[y][idx+2] = pixel;
        }
    }
    
    int k = kernel_size / 2;
    // Desenfoque horizontal
    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            int sum = 0, count = 0;
            for (int dx = -k; dx <= k; dx++) {
                int nx = x + dx;
                if (nx >= 0 && nx < width) {
                    sum += input_rows[y][nx * bytes_per_pixel]; // Gris, canales iguales
                    count++;
                }
            }
            int index = x * bytes_per_pixel;
            unsigned char prom = sum / count;
            temp_rows[y][index] = prom;
            temp_rows[y][index + 1] = prom;
            temp_rows[y][index + 2] = prom;
        }
        for (int p = width * bytes_per_pixel; p < row_padded; p++) temp_rows[y][p] = input_rows[y][p];
    }
    
    // Desenfoque vertical
    for (int y = 0; y < height; y++) {
        for (int x = 0; x < width; x++) {
            int sum = 0, count = 0;
            for (int dy = -k; dy <= k; dy++) {
                int ny = y + dy;
                if (ny >= 0 && ny < height) {
                    sum += temp_rows[ny][x * bytes_per_pixel];
                    count++;
                }
            }
            int index = x * bytes_per_pixel;
            unsigned char prom = sum / count;
            output_rows[y][index] = prom;
            output_rows[y][index + 1] = prom;
            output_rows[y][index + 2] = prom;
        }
        for (int p = width * bytes_per_pixel; p < row_padded; p++) output_rows[y][p] = temp_rows[y][p];
    }
    
    for (int i = 0; i < height; i++) {
        fwrite(output_rows[i], sizeof(unsigned char), row_padded, outputImage);
        free(input_rows[i]);
        free(temp_rows[i]);
        free(output_rows[i]);
    }
    
    FILE *outputLog = fopen("output_log.txt", "a");
    if (outputLog) {
        fprintf(outputLog, "Función: desenfoque gris, con %s\n", input_path);
        fprintf(outputLog, "Localidades totales leídas: %d\n", width * height);
        fprintf(outputLog, "Localidades totales escritas: %d\n", width * height);
        fprintf(outputLog, "-------------------------------------\n");
        fclose(outputLog);
    }
    
    free(input_rows); free(temp_rows); free(output_rows);
    fclose(image); fclose(outputImage);
    printf("Imagen generada: %s\n", output_path);
}

#endif
