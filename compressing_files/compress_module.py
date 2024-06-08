import zlib, base64

def compress(input_file, output_file):
    data = open(input_file, 'r').read()
    data_bytes = bytes(data, 'utf-8')
    compressed_data = base64.b64encode(zlib.compress(data_bytes, 9)) 
    decoded_data = compressed_data.decode('utf-8')
    compressed_file = open(output_file, 'w')
    compressed_file.write(decoded_data)

compress('demo.txt', 'ot.txt')

def decompress(input_file, output_file):
    file_content = open(input_file, 'r').read()
    encoded_data = file_content.encode('utf-8')
    decompressed_data = zlib.decompress(base64.b64decode(encoded_data))
    decoded_data = decompressed_data.decode('utf-8')
    file = open(output_file, 'w')
    file.write(decoded_data)
    file.close()

decompress('ot.txt', 'dc1.txt')