import os
from decouple import config
from PyQt5.QtWidgets import QDialog
from disclaimer_widget import Ui_Disclaimer
from queries import query_processor

class Disclaimer_window(QDialog):
    def __init__(self, fileID, parent):
        super().__init__(parent)
        self.ui = Ui_Disclaimer()
        self.fileID = fileID
        self.accountID = parent.accountID
        self.query = query_processor()
        self.ui.setupUi(self)
        self.signal_connect()

    def signal_connect(self):
        self.ui.proceed_button.clicked.connect(self.proceed_button_clicked)
        self.ui.cancel_button.clicked.connect(self.cancel_button_clicked)
        self.setObjectName("disclaimer_widget")

    def proceed_button_clicked(self):
        hashed_name = self.query.get_hashed_name(self.accountID, fileID=self.fileID)

        self.query.delete_file(self.fileID)
        self.delete_encrypted_file(self.accountID, hashed_name)
        self.parent().show_files()
        self.close()

    def cancel_button_clicked(self):
        self.close()

    def delete_encrypted_file(self, accountID, hashed_name):
        sub_save_folder = os.path.join(config('SAVE_FOLDER'),f"account_{accountID}")
        for encrypted_file in os.listdir(sub_save_folder):
            if (hashed_name == encrypted_file):
                file_path = os.path.join(sub_save_folder, encrypted_file)
                os.remove(file_path)
