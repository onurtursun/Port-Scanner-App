import sys
from PyQt6.QtGui import QIcon, QFont
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QPushButton, QVBoxLayout, QWidget,QMessageBox,QLabel
import socket
import os
import threading

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle('ITU RAL Port Scanner')
        self.setWindowIcon(QIcon('rck.png'))
        self.setStyleSheet('background-color:white')

        self.text_edit = QTextEdit(self)
        self.text_edit.setReadOnly(True)  # To prevent user input
        self.text_edit.setGeometry(10, 10, 580, 300)

        self.button = QPushButton('Run', self)
        self.button.setGeometry(10, 320, 580, 30)
        self.button.setStyleSheet('background-color:red')
        self.button.setFont(QFont("Times",18))
        self.button.clicked.connect(self.info_msg)
        self.button.clicked.connect(self.run_code)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.text_edit)
        self.layout.addWidget(self.button)

        self.container = QWidget()
        self.container.setLayout(self.layout)
        self.setCentralWidget(self.container)

    def info_msg(self):
        QMessageBox.information(self, "Warning", "Scanning will be started.")

    def run_code(self):
        # Clear the existing content
        self.text_edit.clear()
        output = []
        self.text_edit.setText("Scanning in Progress...")
        def get_file_path():
            return os.path.realpath(__file__)

        def scan_ports(start_port, end_port, range_in, range_out):
            try:
                range_in = int(range_in)
                range_out = int(range_out)
                start_port = int(start_port)
                end_port = int(end_port)
            except ValueError:
                print("Invalid input. Please enter integer values for port range and host ID range.")
                return

            for i in range(range_in, range_out + 1):
                ip = f"*.*.*.{i}"
                for port in range(start_port, end_port + 1):
                    try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        sock.settimeout(1)  # Adjust timeout as needed
                        result = sock.connect_ex((ip, port))
                        if result == 0:
                            print(f"{ip} device is open")
                            output.append(f">>{ip} device is open\n")
                        sock.close()
                    except socket.error as e:
                        print(f"Socket error occurred: {e}")
                    except Exception as e:
                        print(f"An error occurred: {e}")

        # Create a thread to run the scanning function
        def scan_thread():
            start_port = 80
            end_port = 80
            range_in = 1
            range_out = 256

            scan_ports(start_port, end_port, range_in, range_out)
            self.display_output(output)

        threading.Thread(target=scan_thread).start()

    def display_output(self, output):
        # Display the output in the QTextEdit
        self.text_edit.append("Scanning complete.\n")
        for line in output:
            self.text_edit.append(line)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MyMainWindow()
    mainWindow.show()
    sys.exit(app.exec())
