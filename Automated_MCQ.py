import csv
import random
# import scrapes
import os
# TODO: POTENTIAL GUI FOR THIS MODULE.


class CSV_MCQ:
    def __init__(self):
        pass

    # def SCRAPER(self):
        # scrapes.scraping_site(0)  # it needs alot of side programs to run!!!

    def file_opener(self, text_file):  # (text_file)
        global tap
        dic_replace = {"â€“": "-", "Ã—": "X", "  ": " x ",  " –": " - ", "Ï„": "(torque)", "Î»": "(lambda)",
           "a)": "(A)", "b)": "(B)", "c)": "(C)", "d)": "(D)",
           "(a)": "(A)", "(b)": "(B)", "(c)": "(C)", "(d)": "(D)", "μ0": "(Epsilon naught)",
           "Ï€": "(Pi)", "â†’": "->", "Â±": "(+-)", "ï»¿": "",
           "Î±": "(alpha)", "Î": "(alpha)", "µ": "(Epsilon)", "(alpha)¼0": "(Epsilon naught)",
           "(alpha)¼o": "(Epsilon naught)", "Â(Epsilon)": "(micro)", "(alpha)¸": "(Theta)",
           "(alpha)©": "(ohm)", "(alpha)£": "(Sigma)", "(alpha)¦": "(Phi)", "Â°": "(degree)", "(alpha)”": "(Delta)",
           "(alpha)²": "(Beta)", "Â²": "^2",}
        lister = []
        num = []
        with open(text_file) as text:
            text_vomit = text.read().splitlines()
            for i in text_vomit:
                for k in dic_replace:
                    i = i.replace(k, dic_replace[k])
                num.append(i)
        text.close()
        for i in num:
            string = i.encode( "ascii",errors="ignore" )
            string.decode()
            lister.append(((str(string)).lstrip('b\'')).rstrip("'"))
        return lister

    def csv_opener_questions(self, csv_file_name):  # (file.csv)
        lister = []
        with open(csv_file_name, 'r', encoding='utf-8') as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:
                lister.append(dict(row))
            return lister

    def csv_opener_questions_trainer(self, csv_file_name):  # (file.csv)
        with open(csv_file_name, 'r') as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:
                print(f"{list( row.values() )[0]}) {list( row.values() )[1]}", end="\n\n")
                for i in range(2, 6):
                    print(f"{list(row.values())[i]}")
        file.close()

    def csv_opener_answers(self, csv_file_name):  # (file.csv)
        lister = []
        with open(csv_file_name, 'r') as file:
            csv_file = csv.DictReader(file)
            for row in csv_file:
                lister.append(dict(row["answer"]))
        file.close()

    def WRITE_NEW_DATABASE(self, header, filename, text_file):
        dic = {}
        folder = []
        count = 0

        with open(filename, 'w', newline='') as file:
            file_header = csv.DictWriter(file, fieldnames=header)
            file_header.writeheader()

            lister = self.file_opener(text_file)

            for i in range(int(len(lister)/7)):
                for j in range(len(header)):
                    dic[header[j]] = lister[j + count]
                folder.append(dic.copy())
                dic.clear()
                count += len(header)

            for i in range(len(folder)):
                file_header.writerow(folder[i])
            file.close()
            return folder

    def APPEND_NEW_QUESTION(self, insert_data_txt, file_to_be_opened_csv, header):  # (file, csv_file_to_be_opened)
        dic = {}
        folder = []
        count = 0

        with open(file_to_be_opened_csv, 'a', newline='') as file:
            file_header = csv.DictWriter(file, fieldnames=header)
            lister = self.file_opener(insert_data_txt)

            for i in range(int(len(lister) / 7)):
                for j in range(len(header)):
                    dic[header[j]] = lister[j + count]
                folder.append(dic.copy())
                dic.clear()
                count += len(header)
                # TODO: revision needed
                #   ADD MORE FLEXIBLE CODE

            for i in range(len(folder)):
                file_header.writerow(folder[i])
            file.close()
            return folder


class TESTING(CSV_MCQ):
    def __init__(self, name, database_csv):
        super().__init__()
        self.name = name
        self.database_csv = database_csv
        self.score = 0
        self.total_lifetime_score = 0
        self.total_tests = 0

    def GUI_trainer(self, question_per_loop):
        choosen_ones = random.sample(self.csv_opener_questions(self.database_csv), 10)
        return choosen_ones

    def trainer(self, questions_per_loop):
        global wrong_questions
        database = [0, self.name]
        lister = []
        memory = []
        print("OPT OPTIONS AS [a, b ,c ,d], in situation of not knowing answer\n "
              "opt in guess or fill anything atleast. \n"
              "[CAUTION: ONLY USE ENGLISH LETTERS]")
        # question = self.csv_opener_questions(self.database_csv)
        # print(question)

        for i in range(questions_per_loop):
            question = self.csv_opener_questions(self.database_csv)
            T = (random.choice(question))
            if T['index'] not in memory:
                memory.append(T['index'])
                print(f"QUESTION NUMBER - {i}")
                print(T["question"])
                print(T["A"])
                print(T["B"])
                print(T["C"])
                print(T["D"])
                take = input("OPT ONE OPTION: ")
                if take == T["Answer"][-1].lower():
                    self.score += 1
                    print("correct!")
                    database[0] += 1
                else:
                    lister.append(T["question"])
                    print("wrong!")
                    database.append(T["index"])
            else:
                questions_per_loop += 1
        return self.score, lister, database
        # TODO: DECISION FOR HOW TO STORE:
        #   A) ISOLATE ALL WRONG QUESTIONS.
        #   B) STORE REFERENCED PRIMARY KEYS ONLY.

    def evaluator(self, data_score_by_playing):
        print(f"Questions wrong by you in database index - {data_score_by_playing[2:len(data_score_by_playing)]}")
        # TODO: STATISTICAL SHOWCASE.

    def find(self, name, path):
        for root, dirs, files in os.walk(path):
            print(dirs)
            if name in dirs:
                return os.path.join(root, name)

    def Profiler(self, data, profile_name="UNDEFINED"):
        pass
        # TODO: SQL BASED STORAGE SYSTEM THEN TAKE OUT OF DATA TO EXCEL FOR CHARTS.

    def tesing_type1(self, val_1):
        f = open(val_1, 'r', encoding='utf-8')
        d = csv.DictReader(f)
        container = list(d)
        num = int(input('How many questions?'))
        total = []
        for i in range(num):
            n = container[i]
            n1 = n['Answer']
            n2 = n1[-1]
            print(n['question'])
            print('')
            print(n['A'])
            print(n['B'])
            print(n['C'])
            print(n['D'])
            print('')
            f = input('Select The Correct Option(a/b/c/d)')
            if f == n2:
                print('correct')
            total.append(list(n))
        return total

        # TODO: MORE TYPES OF TESTING METHODS

