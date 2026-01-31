import dateutil.parser
from datetime import datetime
import bcrypt
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


class ParsingBase:
    def __init__(self):
        self.expecting = ["Date", ["Type" , "Category"], [ "Details", "Description", "Reference", "Narrative"], ["Credit Amount", "Withdrawal", "Out"], ["In", "Debit Amount", "Received", "Deposit"], "Balance"]

    def check_date_type(self, dateList):
        try:
            datetime.strptime(dateList[0], "%d/%m/%Y")
            return True
        except ValueError:
            return False
        
    # https://stackoverflow.com/questions/52206973/convert-different-date-formats-to-a-given-unique-date-format-in-python
    def change_type(self, dateList, column, dataframe):
        if not self.check_date_type(dateList):
            for i in column:
                column = column.replace([i], dateutil.parser.parse(i).strftime("%d/%m/%Y"))
        dataframe[dataframe.columns[0]] = column

    # need to do more debugging 
    def unify_amount_columns(self, df):
        same = df[df.columns[-3]].equals(df[df.columns[-2]])
        
        if (same):
            # if 2 columns are equal, drop the later one
            df.drop(df.columns[[-3]], axis=1, inplace=True)
        else:
            # change any non-numeric value to NaN
            df[df.columns[-3]] = pd.to_numeric(df[df.columns[-3]], errors='coerce')
            df[df.columns[-2]] = pd.to_numeric(df[df.columns[-2]], errors='coerce')

            corrected = (df[df.columns[-3]].fillna(0) - df[df.columns[-2]].fillna(0))
            pos = len(df.columns) - 3
            df.insert(pos, "Amount", corrected)
            df.drop(columns=[df.columns[-3], df.columns[-2]], inplace=True)

    # need to change the whole thing
    def order_dataframe(self, df, columns):

        missing = sorted(list(set(range(6)) - set(columns)))

        if (not missing):
            return df
        print("missing values:\n")
        print(missing)

        extra = 0
        for i in missing:
            pos = i + extra
            if (i == 1):
                df.insert(pos, "Type", "")
            elif (i == 2):
                df.insert(pos, "Description", "")
            else:
                raise Exception("Important column is not selected")
            extra+=1
        return df
    
    def choose_ratio(self, columns):
        mat1 = [0]*len(self.expecting)
        mat2 = []
        
        for idx, i in enumerate(self.expecting):
            if not isinstance(i, list):
                #mat1.append(process.extractOne(i, columns, scorer=fuzz.partial_ratio))
                mat1[idx] = process.extractOne(i, columns, scorer=fuzz.partial_ratio)
                
            else:
                group_results = []
                for j in i:
                    group_results.append(process.extractOne(j, columns, scorer=fuzz.partial_ratio))
                #mat1.append(group_results)
                mat1[idx] = group_results

        above = 70
        chosen_columns = []
        for idx, i in enumerate(mat1):
            if not isinstance(i, list):
                if (i[1] > above):
                    mat2.append(i[0])
                    chosen_columns.append(idx)
            else:
                highest = 0
                highIdx = None
                for sub_idx, j in enumerate(i):
                    if (j[1] > highest and j[1] >above):
                        highest = j[1]
                        highIdx = sub_idx

                if highIdx is not None:
                    element = i[highIdx][0]
                    mat2.append(element)
                    chosen_columns.append(idx)

        try:
            if (mat2[-1] == mat2[-2]):
                mat2.pop()
        except:
            print("The table is not related to transaction")
        return mat2, chosen_columns


class password_class:
    
    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # later used to check the password
    def check_password(self, plain_text_password, hashed_password):
        return bcrypt.checkpw(plain_text_password, hashed_password)
    
