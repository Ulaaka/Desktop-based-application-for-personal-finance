
from decouple import config
import os, tempfile
from BASE_Classes import cryptography, password_class
from queries import query_processor


password = 'Ulaaka_1223'
username = "test5"
account_name =  "savings"
email = "urnaa@gmail.com"
account_type = "Bank"
account_currency = "GBP"


class file_handling():
    def __init__(self, username, password, account_name, email, account_type, account_currency):
        self.username = username
        self.password = password
        self.account_name = account_name
        self.email = email
        self.account_type = account_type
        self.account_currency = account_currency
        self.crypto = cryptography()
        self.password_manager = password_class()
        self.query = query_processor()

    def show_decrypted_pdf(self, decrypted_text):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
            tmp.write(decrypted_text)
            tmp.flush()
        return tmp.name

    def delete_temp_file(self, temp_name):
        os.unlink(temp_name)

    def open_temp_file(self, temp_name):
        os.system(f"open {temp_name}")

    # needs to be fixed
    def check_file_exists(self, sub_save_folder, file_path, accountID, filename):

        found = False
        for encrypted_file in os.listdir(sub_save_folder):
            decrypted = self.crypto.decrypt(sub_save_folder, password, username, account_name, hashed_filename=encrypted_file)
            # check the size of the file, avoiding reading the whole files

            if os.path.getsize(file_path) == len(decrypted):
                # if the same size, then read them
                with open(file_path, 'rb') as file:
                    if file.read() == decrypted:
                        # find the submitted existing file_name in the folder
                        existing_name = self.query.get_file_name_from_hashed(accountID, encrypted_file)
                        found = True
                        print(f"The file {filename} already exists as: {existing_name}")
                        break
        return found

