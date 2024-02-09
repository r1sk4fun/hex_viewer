import os
import sys


def readable_bytes(bytes_data: bytes) -> str:
    """
    Function to create string of readable characters from the given bytes data.
    
    Parameters: bytes_data (bytes): the input bytes data to be processed.

    Returns: string
    """
    output_line = ""
    for readable_byte in bytes_data:
        if readable_byte >= 32 and readable_byte <= 126:
            output_line += chr(readable_byte)
        else:
            output_line += "."
    
    return output_line


def partial_batch(bytes_data: bytes) -> str:
    """
    Function to create missing string from the partial batch of bytes data.

    Parameters: bytes_data (bytes): the input bytes data to be processed

    Returns: string
    """
    output_line = " " * ((3 * (16 - len(bytes_data)))) + "|" + " "
    output_line += readable_bytes(bytes_data)

    return output_line


def read_file(file_path: str) -> None:
    """
    Function to read a file and print its contents in a hexadecimal and readable format.
    
    Parameters: file_path (string): the path to the file to be read

    Returns: None
    """
    with open(file_path, 'rb') as file:
        for step in range(0, os.path.getsize(file_path), 16):
            bytes_data = file.read(16)
            output_line = ""
            for byte_counter, byte in enumerate(bytes_data):
                output_line += "{:02x}".format(byte, 2) + " "
                if (byte_counter + 1) % 16 == 0:
                    output_line += "| " + readable_bytes(bytes_data)
            if step + 16 >= os.path.getsize(file_path):
                output_line += partial_batch(bytes_data)
            print(output_line)


if __name__ == "__main__":
    read_file(sys.argv[1])
