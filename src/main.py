import os
import sys
import webbrowser
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QApplication
import main_window


class GUI(QMainWindow, main_window.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.browseFile.triggered.connect(self.browse_file)
        self.browseGitHub.triggered.connect(lambda: webbrowser.open('https://github.com/r1sk4fun/binary_viewer.git'))


    def browse_file(self):
        file_path = QFileDialog.getOpenFileName(self, 'Open File', 'C:/')
        if file_path[0]:
            self.textEdit.setText(F"Path to selected file: {file_path[0]}")
            with open(file_path[0], 'rb') as file:
                for step in range(0, os.path.getsize(file_path[0]), 16):
                    bytes_data = file.read(16)
                    output_line = ""
                    for byte_counter, byte in enumerate(bytes_data):
                        output_line += "{:02x}".format(byte, 2) + " "
                        if (byte_counter + 1) % 16 == 0:
                            output_line += "| " + self.readable_bytes(bytes_data)
                            # real time update of GUI
                            # drastically increases execution time
                            QApplication.processEvents()
                    # if EOF is reached then pad the output line
                    if step + 16 >= os.path.getsize(file_path[0]):
                        output_line += " " * ((3 * (16 - len(bytes_data)))) + "|" + " "
                        output_line += self.readable_bytes(bytes_data)
                    self.textEdit.append(output_line)


    def readable_bytes(self, bytes_data: bytes) -> str:
        output_line = ""
        for readable_byte in bytes_data:
            if readable_byte >= 32 and readable_byte <= 126:
                output_line += chr(readable_byte)
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
