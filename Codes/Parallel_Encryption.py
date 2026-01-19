import time
import os
from concurrent.futures import ThreadPoolExecutor

# Step 1: Generate a Fibonacci sequence up to n terms
def fibonacci_sequence(n):
    fib_sequence = [0, 1]
    for i in range(2, n):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence

# Step 2: Read the .docx file as binary
def read_word_file(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
    return content

# Encrypt a chunk of content using the Fibonacci sequence with XOR and XNOR
def encrypt_chunk(chunk, fib_sequence, start_index):
    encrypted_chunk = bytearray()
    for i, byte in enumerate(chunk):
        # XOR each byte with the corresponding Fibonacci number, adjusted for the start index
        xor_byte = byte ^ (fib_sequence[(start_index + i) % len(fib_sequence)] % 256)
        
        # Apply XNOR by flipping the bits of the XOR result
        xnor_byte = ~xor_byte & 0xFF  # Mask with 0xFF to keep it within a byte range (0-255)
        
        # Append the XNOR result to the encrypted chunk
        encrypted_chunk.append(xnor_byte)
    return encrypted_chunk

# Step 3: Parallel encryption of the content using multiple threads
def parallel_encrypt_content(content, fib_sequence, num_threads=4):
    # Divide the content into chunks
    chunk_size = len(content) // num_threads
    chunks = [content[i * chunk_size: (i + 1) * chunk_size] for i in range(num_threads)]
    
    # Handle any remaining bytes
    if len(content) % num_threads != 0:
        chunks[-1] += content[num_threads * chunk_size:]
    
    encrypted_content = bytearray()
    
    # Use ThreadPoolExecutor to encrypt each chunk in parallel
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [
            executor.submit(encrypt_chunk, chunk, fib_sequence, i * chunk_size)
            for i, chunk in enumerate(chunks)
        ]
        
        # Collect encrypted chunks as they complete
        for future in futures:
            encrypted_content.extend(future.result())
    
    return encrypted_content

# Step 4: Save encrypted content to a new binary file
def save_encrypted_file(encrypted_content, output_path):
    with open(output_path, 'wb') as file:
        file.write(encrypted_content)

# Main encryption function
def encrypt_word_file(input_path, output_folder, num_threads=4):
    start_time = time.time()

    # Step 2: Read file content as binary
    content = read_word_file(input_path)
    
    # Step 1: Generate Fibonacci sequence based on content length
    fib_sequence = fibonacci_sequence(len(content))
    
    # Step 3: Encrypt the content in parallel
    encrypted_content = parallel_encrypt_content(content, fib_sequence, num_threads)
    
    # Define output path and save encrypted content
    output_path = os.path.join(output_folder, "parallerly_encrypted_file.bin")
    save_encrypted_file(encrypted_content, output_path)
    
    # Calculate and print the time taken
    end_time = time.time()
    print(f"Encryption completed. Time taken: {end_time - start_time} seconds.")
    print(f"Encrypted file saved at: {output_path}")

# Example usage
input_path = "C:\\Desktop\\Text.docx"  # Path to input file
output_folder = "C:\\Desktop"  # Destination folder

# Run encryption with parallel processing
encrypt_word_file(input_path, output_folder, num_threads=4)
