useage="LG22.py <encode,decode> <input_file> <output_file> (encoded_name)"


from struct import pack, unpack
from sys import argv as arguments
from hashlib import md5


#encode
def encode(decoded_filename,encoded_filename,trackname):
    data=b""
    with open(decoded_filename,"rb") as df:
        data = df.read()
    
    m = md5(usedforsecurity=False)
    m.update(data)
    key = m.digest()
    
    with open(encoded_filename,"wb") as ef:
        ef.write("GRT1".encode("ascii"))
        #little endian uint32_t followed by uint_8
        ef.write(pack("<LB", 4 + 4 + 1 + len(trackname) + 16 + 4 + len(data),  len(trackname) ))
        ef.write(trackname.encode("ascii"))
        ef.write(key)
        ef.write(pack("L", len(data)))
        #write "encrypted" data
        for i in range(0,len(data)):
            ef.write(pack("B", data[i] ^ ((key[i % 16] + i) & 0xFF)))


#decode
def decode(encoded_filename,decoded_filename):
    data=b""
    with open(encoded_filename,"rb") as ef:
        data = ef.read()
    
    # skip header "GRT1"
    data = data[4:]
    
    # extract length
    length = unpack("L", data[:4])[0]
    data = data[4:]
    
    # extract filename
    filename_length = unpack("B", data[:1])[0]
    data = data[1:]
    
    filename = data[:filename_length]
    data = data[filename_length:]
    
    print("filename: " + filename.decode("ascii"))
    
    # extract key
    key = data[:16]
    data = data[16:]
    
    print("key: " + key.hex())
    
    # extract payload length
    payload_length = unpack("L", data[:4])[0]
    data = data[4:]
    
    # "decrypt" payload
    with open(decoded_filename,"wb") as df:
        for i in range(0,len(data)):
            df.write(pack("B", data[i] ^ ((key[i % 16] + i) & 0xFF)))
    
    # ffmpeg -f g722 -i 1000weisseLilien.L22.decode.g722 -ar 22050 test.wav


#argument handling
if len(arguments) < 2:
    quit(useage)
mode = arguments[1]
if mode == "encode":
    if len(arguments) not in [4,5]:
        print("invalid argument count. correct useage:")
        print(useage)
        quit()
    mode==True
elif mode == "decode":
    if len(arguments) != 4:
        print("invalid argument count. correct useage:")
        print(useage)
        quit()
    mode=False
else:
    print("invalid arguments. correct useage:")
    print(useage)
    quit()

if mode:
    trackname=arguments[4] if len(arguments)==5 else arguments[3]
    encode(arguments[2],arguments[3], trackname)
else:
    decode(arguments[2],arguments[3])

