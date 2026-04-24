with open('selec_proc.h', 'r') as f:
    text = f.read()

old_block = """    unsigned char header[54];
    fread(header, sizeof(unsigned char), 54, image);
    fwrite(header, sizeof(unsigned char), 54, outputImage);"""

new_block = """    unsigned char header[54];
    fread(header, sizeof(unsigned char), 54, image);
    int offset = *(int*)&header[10];
    int remaining_header = offset - 54;
    fwrite(header, sizeof(unsigned char), 54, outputImage);
    if (remaining_header > 0) {
        unsigned char* extra_hdr = (unsigned char*)malloc(remaining_header);
        fread(extra_hdr, 1, remaining_header, image);
        fwrite(extra_hdr, 1, remaining_header, outputImage);
        free(extra_hdr);
    }"""

text = text.replace(old_block, new_block)

with open('selec_proc.h', 'w') as f:
    f.write(text)
