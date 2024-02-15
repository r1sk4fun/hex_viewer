import os
import sys


class HexViewer():
    def __init__(self):
        self.BLOCK_WIDTH: int = 16
        self.BLOCK_HEIGHT: int = 32
        self.BLOCK_SIZE: int = self.BLOCK_WIDTH * self.BLOCK_HEIGHT
        self.file_path: str | None = None
        self.pages_minimum: int = 0
        self.pages_maximum: int = 0
        self.current_page: int = 0


    def set_pages_maximum(self):
        self.pages_maximum = os.path.getsize(self.file_path) // self.BLOCK_SIZE


    def set_current_page(self):
        while True:
            page = input(f"Current page is {self.current_page} out of {self.pages_maximum}: ")
            match page:
                case page if not page.isnumeric():
                    print("Please enter a number")
                case page if int(page) < self.pages_minimum or int(page) > self.pages_maximum:
                    print("Page doesn't exist")
                case _:
                    self.current_page = int(page)
                    os.system('cls' if os.name == 'nt' else 'clear')
                    break


    def open_file(self):
        while True:
            file_path = input("Enter path to file: ")
            if os.path.isfile(file_path):
                self.file_path = file_path
                self.set_pages_maximum()
                os.system('cls' if os.name == 'nt' else 'clear')
                self.read_block()
                break
            else:
                print("File doesn't exist")
                pass


    def read_block(self):
        if not self.file_path:
            return None
        with open(self.file_path, 'rb') as file:
            file.seek(self.current_page * self.BLOCK_SIZE)
            block = file.read(self.BLOCK_SIZE)
        # split block into rows
        rows = [block[i:i + self.BLOCK_WIDTH] for i in range(0, len(block), self.BLOCK_WIDTH)]
        for num, row in enumerate(rows):
            print(self.show_bytes_quantity(num) + self.show_bytes(row) + self.show_printable_bytes(row))


    def show_bytes_quantity(self, num: int) -> str:
        # (num * 16) for current block offset
        # (self.current_page * self.BLOCK_SIZE) for current page offset
        return "{:08x}".format((num * 16) + (self.current_page * self.BLOCK_SIZE)).upper() + ": "


    def show_bytes(self, row: bytes) -> str:
        output_line = ""
        for byte in row:
            output_line += "{:02x}".format(byte) + " "
        if len(row) < self.BLOCK_WIDTH:
            # each byte is 3 characters long (2 hex characters + 1 space)
            output_line += " " * (self.BLOCK_WIDTH - len(row)) * 3
        return output_line.upper() + "| "


    def show_printable_bytes(self, row: bytes) -> str:
        output_line = ""
        for byte in row:
            # printable ASCII characters
            if byte >= 32 and byte <= 126:
                output_line += chr(byte)
            else:
                output_line += "."
        return output_line


def main():
    app = HexViewer()
    app.open_file()
    app.set_current_page()
    app.read_block()
    while True:
        try:
            app.set_current_page()
            app.read_block()
        except KeyboardInterrupt:
            sys.exit()


if __name__ == '__main__':
    main()
