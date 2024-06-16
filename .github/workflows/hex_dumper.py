
import os

def create_sample_bin_file(filename, size_in_bytes):
    with open(filename, 'wb') as file:
        random_data = os.urandom(size_in_bytes)
        file.write(random_data)

# Specify the filename and size in bytes for your sample binary file
sample_filename = 'sample.bin'
sample_size = 1024  # Change this to the desired size in bytes

create_sample_bin_file(sample_filename, sample_size)
print(f"Sample binary file '{sample_filename}' with size {sample_size} bytes created.")


def hex_dump(filename, bytes_per_line=16):
    with open(filename, 'rb') as file:
        offset = 0
        while True:
            chunk = file.read(bytes_per_line)
            if not chunk:
                break
            
            hex_chunk = ' '.join(f'{byte:02X}' for byte in chunk)
            ascii_chunk = ''.join(chr(byte) if 32 <= byte <= 126 else '.' for byte in chunk)
            
            print(f'{offset:08X}  {hex_chunk:<{bytes_per_line*3}}  {ascii_chunk}')
            offset += bytes_per_line

# Replace 'sample.bin' with the path to your binary file
hex_dump('sample.bin')



