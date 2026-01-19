import os
import time
from concurrent.futures import ThreadPoolExecutor

# Function to generate Fibonacci sequence up to n terms
def fibonacci_sequence(n):
    fib_sequence = [0, 1]
    for i in range(2, n):
        fib_sequence.append(fib_sequence[-1] + fib_sequence[-2])
    return fib_sequence

# Function to read the encrypted binary file
def read_encrypted_file(file_path):
    with open(file_path, 'rb') as file:
        encrypted_content = file.read()
    return encrypted_content

# Function to decrypt a chunk of content using Fibonacci sequence with XOR and XNOR
def decrypt_chunk(chunk, fib_sequence, start_index):
    decrypted_chunk = bytearray()
    for i, byte in enumerate(chunk):
        # Reverse XNOR by applying NOT, then reverse XOR with the Fibonacci key
        xnor_byte = ~byte & 0xFF  # Perform NOT operation and mask with 0xFF to keep it within byte range
        decrypted_byte = xnor_byte ^ (fib_sequence[(start_index + i) % len(fib_sequence)] % 256)  # XOR decryption
        
        # Append the decrypted byte to the result
        decrypted_chunk.append(decrypted_byte)
    return decrypted_chunk


# Function to perform parallel decryption of the content
def parallel_decrypt_content(encrypted_content, fib_sequence, num_threads=4):
    # Divide the content into chunks
    chunk_size = len(encrypted_content) // num_threads
    chunks = [encrypted_content[i * chunk_size: (i + 1) * chunk_size] for i in range(num_threads)]
    
    # Handle any remaining bytes
    if len(encrypted_content) % num_threads != 0:
        chunks[-1] += encrypted_content[num_threads * chunk_size:]
    
    decrypted_content = bytearray()
    
    # Use ThreadPoolExecutor to decrypt each chunk in parallel
    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        futures = [
            executor.submit(decrypt_chunk, chunk, fib_sequence, i * chunk_size)
            for i, chunk in enumerate(chunks)
        ]
        
        # Collect decrypted chunks as they complete
        for future in futures:
            decrypted_content.extend(future.result())
    
    return decrypted_content

# Function to save the decrypted content to a new file
def save_decrypted_file(decrypted_content, output_path):
    with open(output_path, 'wb') as file:
        file.write(decrypted_content)

# Main decryption function
def decrypt_word_file(encrypted_file_path, output_folder, num_threads=4):
    start_time = time.time()

    # Step 1: Read encrypted binary content
    encrypted_content = read_encrypted_file(encrypted_file_path)
    
    # Step 2: Generate the Fibonacci sequence based on content length
    fib_sequence = fibonacci_sequence(len(encrypted_content))
    
    # Step 3: Decrypt the content in parallel
    decrypted_content = parallel_decrypt_content(encrypted_content, fib_sequence, num_threads)
    
    # Define output path and save decrypted content
    output_path = os.path.join(output_folder, "parallerly_decrypted_file.docx")
    save_decrypted_file(decrypted_content, output_path)
    
    # Calculate and print the time taken
    end_time = time.time()
    print(f"Decryption completed. Time taken: {end_time - start_time} seconds.")
    print(f"Decrypted file saved at: {output_path}")

# Example usage
encrypted_file_path = "C:\\Desktop\\parallerly_encrypted_file.bin"  # Path to encrypted file
output_folder = "C:\\Desktop"  # Destination folder

# Run decryption with parallel processing
decrypt_word_file(encrypted_file_path, output_folder, num_threads=4)
