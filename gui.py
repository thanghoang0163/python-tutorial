import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from PySide6.QtGui import *


class main(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Demo GUI")
        self.setGeometry(500, 100, 500, 500)
        self.setWindowIcon(QIcon.fromTheme(QIcon.ThemeIcon.SyncSynchronizing))

        layout = QVBoxLayout()

        self.label = QLabel("This is label")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet(
            "font-size: 30px; font-weight: bold; font-style: italic"
        )
        layout.addWidget(self.label)

        self.input = QLineEdit(self)
        self.input.setPlaceholderText("Enter anything to change the label")
        self.input.setStyleSheet("padding: 5px; font-size: 15px")
        layout.addWidget(self.input)

        self.button = QPushButton("Change label", self)
        self.button.clicked.connect(self.change_label)
        self.button.setStyleSheet(
            "background-color: white; font-size: 15px; color: black; font-weight: bold; border-radius: 5; padding: 5px"
        )
        layout.addWidget(self.button)

        self.button = QPushButton("Open Color Dialog", self)
        self.button.clicked.connect(self.handle_color)
        layout.addWidget(self.button)

        self.button = QPushButton("Close Window", self)
        self.button.clicked.connect(self.close_window)
        layout.addWidget(self.button)

        # self.setStyleSheet(" QPushButton { color: red }")

        self.setLayout(layout)

    def change_label(self):
        input_value = self.input.text()

        if input_value:
            self.label.setText(f"{input_value}")

        self.input.clear()

        if "color" in self.label.text():
            self.handle_color()

    def open_color(self):
        self.colorDialog = QColorDialog()
        self.colorDialog.open()
        self.colorDialog.setWindowIcon(QIcon.fromTheme(QIcon.ThemeIcon.FolderOpen))

    def handle_color(self):
        self.open_color()
        self.colorDialog.finished.connect(self.choose_color)

    def choose_color(self):
        selected_color = self.colorDialog.selectedColor().name()

        self.setStyleSheet(
            f"background-color: {selected_color if selected_color!='#000000'else''}"
        )

    def close_window(self):
        self.msgBox = QMessageBox()
        self.msgBox.setWindowTitle("Close window")
        self.msgBox.setText("Do you still want to exit?")
        self.msgBox.setIcon(QMessageBox.Warning)
        self.msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        self.msgBox.setWindowIcon(QIcon.fromTheme(QIcon.ThemeIcon.WindowClose))

        button = self.msgBox.exec()

        if button == QMessageBox.Ok:
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = main()
    ex.show()
    sys.exit(app.exec())
