import re

with open("selec_proc.h", "r") as f:
    code = f.read()

# Replace header reading and writing with dynamic offset
header_read = r'''    unsigned char header\[54\];
    fread\(header, sizeof\(unsigned char\), 54, image\);
    fwrite\(header, sizeof\(unsigned char\), 54, outputImage\);
    
    int width = \*\((int\*)\&header\[18\]\);
    int height = \*\((int\*)\&header\[22\]\);
    int row_padded = \(width \* 3 \+ 3\) & \(\~3\);'''

header_fixed = r'''    unsigned char header[54];
    fread(header, sizeof(unsigned char), 54, image);
    int offset = *(int*)&header[10];
    int remaining_header = offset - 54;
    fwrite(header, sizeof(unsigned char), 54, outputImage);
    if (remaining_header > 0) {
        unsigned char* extra_hdr = (unsigned char*)malloc(remaining_header);
        fread(extra_hdr, 1, remaining_header, image);
        fwrite(extra_hdr, 1, remaining_header, outputImage);
        free(extra_hdr);
    }
    
    int width = *(int*)&header[18];
    int height = *(int*)&header[22];
    short bpp = *(short*)&header[28];
    int bytes_per_pixel = bpp / 8;
    int row_padded = (width * bytes_per_pixel + 3) & (~3);'''

code = re.sub(header_read, header_fixed, code)

# Replace all occurrences of * 3 with * bytes_per_pixel
# Wait, let's fix the pixel indexing
code = re.sub(r'idx \+ (\d)', r'idx+\1', code)
code = re.sub(r'nx \* 3', r'nx * bytes_per_pixel', code)
code = re.sub(r'x \* 3', r'x * bytes_per_pixel', code)
code = re.sub(r'width \* 3', r'width * bytes_per_pixel', code)
code = re.sub(r'idx,', r'idx ,', code)

with open("selec_proc_new.h", "w") as f:
    f.write(code)
