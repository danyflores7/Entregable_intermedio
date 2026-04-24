import re

with open('selec_proc.h', 'r') as f:
    text = f.read()

# Replace variables
text = text.replace('int row_padded = (width * 3 + 3) & (~3);', '''short bpp = *(short*)&header[28];
    int bytes_per_pixel = bpp / 8;
    int row_padded = (width * bytes_per_pixel + 3) & (~3);''')

# Now fix x * 3 to x * bytes_per_pixel
text = text.replace('int idx = x * 3;', 'int idx = x * bytes_per_pixel;')
text = text.replace('int orig_idx = x * 3;', 'int orig_idx = x * bytes_per_pixel;')
text = text.replace('int new_idx = (width - 1 - x) * 3;', 'int new_idx = (width - 1 - x) * bytes_per_pixel;')
text = text.replace('int index = x * 3;', 'int index = x * bytes_per_pixel;')

# There are a few other hardcoded * 3 instances:
# for (int p = width * 3; p < row_padded; p++)
text = text.replace('for (int p = width * 3; p < row_padded; p++)', 'for (int p = width * bytes_per_pixel; p < row_padded; p++)')

# for (int dx = -k; dx <= k; dx++) { int nx = x + dx; if (...) { int idx = nx * 3;
text = text.replace('nx * 3;', 'nx * bytes_per_pixel;')
text = text.replace('sum += input_rows[y][nx * 3];', 'sum += input_rows[y][nx * bytes_per_pixel];')
text = text.replace('sum += temp_rows[ny][x * 3];', 'sum += temp_rows[ny][x * bytes_per_pixel];')

# For the alpha channel, whenever we assign new_idx+2 or idx+2, we also need to copy new_idx+3 if bytes_per_pixel == 4
# Actually, the simplest fix is to initialize out_row with the original row so alpha is preserved, THEN update RGB!
# Wait, for inversion, we need to move alpha.
# Let's just do a regex replace to catch assignments.

# Instead of complex regex, let's just make the C code copy the bytes dynamically:
def fix_func(match):
    return match.group(0)

# Writing a clean C file parser is hard. Let's just do targeted replacements.
# In inv_img: (vertical invert grey)
text = text.replace('''            out_row[idx] = pixel;
            out_row[idx+1] = pixel;
            out_row[idx+2] = pixel;''', '''            out_row[idx] = pixel;
            out_row[idx+1] = pixel;
            out_row[idx+2] = pixel;
            if (bytes_per_pixel == 4) out_row[idx+3] = rows[y][idx+3];''')

# In inv_img_grey_horizontal:
text = text.replace('''            out_row[new_idx] = pixel;
            out_row[new_idx+1] = pixel;
            out_row[new_idx+2] = pixel;''', '''            out_row[new_idx] = pixel;
            out_row[new_idx+1] = pixel;
            out_row[new_idx+2] = pixel;
            if (bytes_per_pixel == 4) out_row[new_idx+3] = rows[y][orig_idx+3];''')

# In inv_img_color_horizontal:
text = text.replace('''            out_row[new_idx+2] = rows[y][orig_idx+2];''', '''            out_row[new_idx+2] = rows[y][orig_idx+2];
            if (bytes_per_pixel == 4) out_row[new_idx+3] = rows[y][orig_idx+3];''')

# In desenfoque (color) vertical and horizontal, we calculate sum. 
# We should copy the alpha channel from input_rows/temp_rows if bpp=4
text = text.replace('''            temp_rows[y][index + 2] = sumR / count;''', '''            temp_rows[y][index + 2] = sumR / count;
            if (bytes_per_pixel == 4) temp_rows[y][index + 3] = input_rows[y][index + 3];''')
text = text.replace('''            output_rows[y][index + 2] = sumR / count;''', '''            output_rows[y][index + 2] = sumR / count;
            if (bytes_per_pixel == 4) output_rows[y][index + 3] = temp_rows[y][index + 3];''')

# In desenfoque_grey:
text = text.replace('''            input_rows[y][idx+2] = pixel;''', '''            input_rows[y][idx+2] = pixel;
            if (bytes_per_pixel == 4) input_rows[y][idx+3] = input_rows[y][idx+3];''')
text = text.replace('''            temp_rows[y][index + 2] = prom;''', '''            temp_rows[y][index + 2] = prom;
            if (bytes_per_pixel == 4) temp_rows[y][index + 3] = input_rows[y][index + 3];''')
text = text.replace('''            output_rows[y][index + 2] = prom;''', '''            output_rows[y][index + 2] = prom;
            if (bytes_per_pixel == 4) output_rows[y][index + 3] = temp_rows[y][index + 3];''')


with open('selec_proc.h', 'w') as f:
    f.write(text)
