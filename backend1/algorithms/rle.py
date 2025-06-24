# Path: backend/algorithms/rle.py

def encode_rle(data):
    """
    Encodes binary data using Run-Length Encoding.
    The format is [count, byte_value].
    """
    if not data:
        return b''
    
    encoded_data = bytearray()
    count = 1
    # Iterate through the data from the second byte
    for i in range(1, len(data)):
        # If the current byte is the same as the previous one and count is less than 255
        if data[i] == data[i-1] and count < 255:
            count += 1
        else:
            # Append the count and the byte value for the previous run
            encoded_data.append(count)
            encoded_data.append(data[i-1])
            # Reset the counter for the new byte
            count = 1
            
    # Append the last run
    encoded_data.append(count)
    encoded_data.append(data[-1])
    
    return bytes(encoded_data)

def decode_rle(encoded_data):
    """
    Decodes binary data that was encoded with our RLE format.
    """
    decoded_data = bytearray()
    i = 0
    # The encoded data is in pairs of (count, byte_value)
    while i < len(encoded_data):
        count = encoded_data[i]
        char_to_repeat = encoded_data[i+1]
        # Extend the decoded data with the repeated byte
        decoded_data.extend([char_to_repeat] * count)
        i += 2
        
    return bytes(decoded_data)