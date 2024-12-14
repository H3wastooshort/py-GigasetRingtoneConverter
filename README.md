# Gigaset-Ringtone-Converter
Gigaset propritary ringtone format (L22 / 722) encoder/decoder, written in Python

``` 
Gigaset L22 / 722 ringtone file format contains the following header:
	4 bytes magic "GRT1"
	4 bytes total file length (including header), little endian
	1 byte filename string length
	n bytes filename (ASCII)
	16 bytes MD5 checksum of decoded G722 data
	4 bytes decoded payload length, little endian
	n bytes payload, XOR encrypted with (MD5 checksum at (read offset % 16)) + read offset. 
```

### Decode
```bash
python3 LG22.py decode test.g722 test.g722
ffmpeg -f g722 -i test.g722 -ar 22050 test.wav
```

### Encode
```bash
ffmpeg -i test.mp3 -ar 22050 test.g722
python3 LG22.py encode test.g722 test.L22
```