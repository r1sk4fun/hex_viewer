import os
import sys


def print_readable_bytes(bytes_data):
    """
    Function to print readable characters from the given bytes data.
    
    Parameters: bytes_data (bytes): the input bytes data to be processed.

    Returns: None
    """
    for readable_byte in bytes_data:
        if readable_byte >= 32 and readable_byte <= 126:
            print(chr(readable_byte), end="")
        else:
            print(".", end="")


def print_partial_batch(bytes_data):
    """
    Function to print readable characters from the partial batch of bytes data.

    Parameters: bytes_data (bytes): the input bytes data to be processed

    Returns: None
    """
    print(" " * ((3 * (16 - len(bytes_data))) - 1), "|", end=" ")
    print_readable_bytes(bytes_data)


def read_file(file_path):
    """
    Function to read a file and print its contents in a hexadecimal and readable format.
    
    Parameters: file_path (string): the path to the file to be read

    Returns: None
    """
    with open(file_path, 'rb') as file:
        for step in range(0, os.path.getsize(file_path), 16):
            bytes_data = file.read(16)
            for byte_counter, byte in enumerate(bytes_data):
                print("{:02x}".format(byte, 2), end=" ")
                if (byte_counter + 1) % 16 == 0:
                    print("|", end=" ")
                    print_readable_bytes(bytes_data)
                    print("")
        print_partial_batch(bytes_data)


if __name__ == "__main__":
    read_file(sys.argv[1])
