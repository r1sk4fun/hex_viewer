import os
import sys
import webbrowser
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication
import ui


class GUI(QMainWindow, ui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.BLOCK_WIDTH = 16
        self.BLOCK_HEIGHT = 32
        self.BLOCK_SIZE = self.BLOCK_WIDTH * self.BLOCK_HEIGHT
        self.file_path: str | None = None

        self.openFile.triggered.connect(self.open_file)
        self.closeFile.triggered.connect(self.close_file)
        self.browseGitHub.triggered.connect(lambda: webbrowser.open('https://github.com/r1sk4fun/binary_viewer.git'))
        self.blockScrollBar.valueChanged.connect(self.scroll_handler)


    def scroll_handler(self):
        self.textView.clear()
        self.read_block()


    def set_scrollbar_maximum(self):
        self.blockScrollBar.setMaximum((os.path.getsize(self.file_path) // self.BLOCK_SIZE) * 16)


    def open_file(self):
        file_path = QFileDialog.getOpenFileName(self, 'Open File', 'C:/')
        if file_path[0]:
            self.file_path = file_path[0]
            self.set_scrollbar_maximum()
            self.textView.clear()
            self.read_block()


    def close_file(self):
        self.textView.clear()


    def read_block(self):
        if not self.file_path:
            return None
        with open(self.file_path, 'rb') as file:
            file.seek(self.blockScrollBar.value() * (2 * 16))
            block = file.read(self.BLOCK_SIZE)
        rows = [block[i:i + self.BLOCK_WIDTH] for i in range(0, len(block), self.BLOCK_WIDTH)]
        for num, row in enumerate(rows, start=1):
            self.textView.append(self.show_bytes_quantity(num) + self.show_bytes(row) + self.show_printable_bytes(row))


    def show_bytes_quantity(self, num: int) -> str:
        return "{:08x}".format((num * 16) + (self.blockScrollBar.value() * (2 * 16))) + ": "


    def show_bytes(self, row: bytes) -> str:
        output_line = ""
        for byte in row:
            output_line += "{:02x}".format(byte) + " "
        if len(row) < self.BLOCK_WIDTH:
            output_line += " " * (self.BLOCK_WIDTH - len(row)) * 3
        return output_line + "| "


    def show_printable_bytes(self, row: bytes) -> str:
        output_line = ""
        for byte in row:
            if byte >= 32 and byte <= 126:
                output_line += chr(byte)
            else:
                output_line += "."
        return output_line


def main():
    app = QApplication(sys.argv)
    window = GUI()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
