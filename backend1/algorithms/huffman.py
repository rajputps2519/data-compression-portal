# Path: backend/algorithms/huffman.py

import heapq
import collections
import pickle

# The Node for the Huffman Tree
class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    # Define a method for comparison in the heap
    def __lt__(self, other):
        return self.freq < other.freq

def make_frequency_dict(data):
    # Count the frequency of each byte in the data
    return collections.Counter(data)

def make_heap(frequency):
    # Create a priority queue (min-heap) of Huffman nodes
    heap = []
    for byte, freq in frequency.items():
        node = HuffmanNode(byte, freq)
        heapq.heappush(heap, node)
    return heap

def merge_nodes(heap):
    # Build the Huffman tree by merging nodes
    while len(heap) > 1:
        node1 = heapq.heappop(heap)
        node2 = heapq.heappop(heap)
        merged = HuffmanNode(None, node1.freq + node2.freq)
        merged.left = node1
        merged.right = node2
        heapq.heappush(heap, merged)
    # The last remaining node is the root of the tree
    return heap[0]

def make_codes_helper(root, current_code, codes):
    if root is None:
        return
    # If it's a leaf node, save the code
    if root.char is not None:
        codes[root.char] = current_code
        return
    # Recursively traverse the tree
    make_codes_helper(root.left, current_code + "0", codes)
    make_codes_helper(root.right, current_code + "1", codes)

def make_codes(root):
    codes = {}
    make_codes_helper(root, "", codes)
    return codes

def get_encoded_text(data, codes):
    # Generate the string of bits from the data
    encoded_text = ""
    for byte in data:
        encoded_text += codes[byte]
    return encoded_text

def pad_encoded_text(encoded_text):
    # Pad the bit string to make its length a multiple of 8
    extra_padding = 8 - len(encoded_text) % 8
    if extra_padding == 8:
        extra_padding = 0
        
    padded_info = "{0:08b}".format(extra_padding)
    encoded_text += "0" * extra_padding
    
    return padded_info + encoded_text

def get_byte_array(padded_encoded_text):
    # Convert the bit string to a byte array
    b = bytearray()
    for i in range(0, len(padded_encoded_text), 8):
        byte = padded_encoded_text[i:i+8]
        b.append(int(byte, 2))
    return bytes(b)


# --- Main Encode and Decode Functions ---

def encode_huffman(data):
    if not data:
        return b''
    
    # Build the Huffman tree and codes
    frequency = make_frequency_dict(data)
    heap = make_heap(frequency)
    root = merge_nodes(heap)
    codes = make_codes(root)
    
    # Encode the data
    encoded_text = get_encoded_text(data, codes)
    padded_encoded_text = pad_encoded_text(encoded_text)
    byte_array = get_byte_array(padded_encoded_text)
    
    # The header contains the frequency map, needed for decoding
    # We use pickle to serialize the frequency dictionary
    header = pickle.dumps(frequency)
    header_len = len(header).to_bytes(4, 'big') # Use 4 bytes to store header length
    
    return header_len + header + byte_array


def decode_huffman(encoded_data):
    # Read the header to rebuild the tree
    header_len = int.from_bytes(encoded_data[:4], 'big')
    frequency = pickle.loads(encoded_data[4 : 4 + header_len])
    
    # Rebuild the Huffman tree
    heap = make_heap(frequency)
    root = merge_nodes(heap)
    
    # The rest of the data is the compressed content
    encoded_data_body = encoded_data[4 + header_len:]

    # Convert the byte array back to a bit string
    encoded_bits = ""
    for byte in encoded_data_body:
        bits = bin(byte)[2:].rjust(8, '0')
        encoded_bits += bits

    # Remove the padding information
    padded_info = encoded_bits[:8]
    extra_padding = int(padded_info, 2)
    encoded_bits = encoded_bits[8:]
    if extra_padding > 0:
        encoded_bits = encoded_bits[:-extra_padding]

    # Decode the bit string using the tree
    decoded_bytes = bytearray()
    current_node = root
    for bit in encoded_bits:
        if bit == '0':
            current_node = current_node.left
        else:
            current_node = current_node.right

        if current_node.char is not None:
            decoded_bytes.append(current_node.char)
            current_node = root
            
    return bytes(decoded_bytes)