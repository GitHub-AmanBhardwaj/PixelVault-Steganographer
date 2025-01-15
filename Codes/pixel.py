#### Encodes a secret message into an image by manipulating pixel values.

def encode_message_in_image(image_path, message):

    img = Image.open(image_path)
    pixels = img.load()
    message+='***'
    mode=img.mode
    print(mode)
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    message_length = len(binary_message)

    width, height = img.size
    if message_length > width * height * 3:
        raise ValueError("Image is too small to hold the message.")

    bit_index = 0
    for y in range(height):
        for x in range(width):
            pixel = pixels[x, y]

            if mode == 'RGB':
                r, g, b = pixel
            elif mode == 'RGBA':
                r, g, b, a = pixel 
            elif mode == 'L':
                r = g = b = pixel

            if bit_index < message_length:
                r = (r & 0xFE) | int(binary_message[bit_index])
                bit_index += 1
            if bit_index < message_length:
                g = (g & 0xFE) | int(binary_message[bit_index])
                bit_index += 1
            if bit_index < message_length:
                b = (b & 0xFE) | int(binary_message[bit_index])
                bit_index += 1

            if mode == 'RGB':
                pixels[x, y] = (r, g, b)
            elif mode == 'RGBA':
                pixels[x, y] = (r, g, b, a)
            elif mode == 'L':
                pixels[x, y] = r

            if bit_index >= message_length:
                break
        if bit_index >= message_length:
            break

    encoded_path = os.path.join(app.config['ENCODED_FOLDER'], "encoded_image.png")
    img.save(encoded_path)
    return encoded_path

#### Decodes a secret message from an image by extracting pixel values.

def decode_message_from_image(image_path):
    
    img = Image.open(image_path)
    pixels = img.load()
    mode=img.mode

    binary_message = ''

    width, height = img.size
    for y in range(height):
        for x in range(width):
            pixel= pixels[x, y]

            if mode == 'RGB':
                r, g, b = pixel
            elif mode == 'RGBA':
                r, g, b, a = pixel
            elif mode == 'L':
                r = g = b = pixel

            binary_message += str(r & 1)
            binary_message += str(g & 1)
            binary_message += str(b & 1)

    message = ''
    sc=0
    for i in range(0, len(binary_message), 8):
        byte = binary_message[i:i+8]
        if len(byte) == 8:
            message += chr(int(byte, 2))
            if chr(int(byte, 2))=='*':
                sc+=1 
            if sc>2:
                break
    if '***' not in message:
        return None

    return message[:len(message)-3]