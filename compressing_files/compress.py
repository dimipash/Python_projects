import zlib, base64

data = open('demo.txt', 'r').read()
data_bytes = bytes(data, 'utf-8')
compressed_data = base64.b64encode(zlib.compress(data_bytes, 9)) 
decoded_data = compressed_data.decode('utf-8')
compressed_file = open('compressed.txt', 'w')
compressed_file.write(decoded_data)