from selenium import webdriver
from bs4 import BeautifulSoup
import re
import csv


def scraping_site(counter_1=0):
    driver = webdriver.Chrome(r"C:\Users\shaina\Desktop\MCQ\Chrome_Driver\chromedriver.exe")
    listing_dict = []

    subject = "mathematics"
    main_page = f"1000-{subject}-questions-answers-class-12/"
    driver.get(f'https://www.sanfoundry.com/{main_page}')
    content = driver.page_source
    soup = BeautifulSoup(content, features="html.parser")
    ar = soup.find('div', attrs={'class': 'entry-content', 'itemprop': 'text'})
    sub_links = ar.findAll('a', href=True)
    listy = []
    for a in sub_links:
        if re.search(rf'https://www.sanfoundry.com/{subject}-questions-answers-', a.get('href')):
            listy.append(a.get('href'))


    questions_intake = []
    answers = []
    counter = 0
    for i in listy:
        driver.get(str(i))
        content = driver.page_source
        soup = BeautifulSoup(content, features="html.parser")
        ar = soup.find('div', attrs={'class': 'entry-content', 'itemprop': 'text'})
        price = ar.findAll("p")
        ans = list(ar.findAll('div', attrs={'class': 'collapseomatic_content'}))
        for a in price:
            # name = a.find('div', attrs={'class': '_3wU53n'})
            # rating = a.find('div', attrs={'class': 'hGSR34 _2beYZw'})
            # products.append(name.text)
            a = (a.text).splitlines()
            if len(a) >= 1:
                if re.search(r'\d\.', a[0][:4]):
                    questions_intake.append(a)
                    if len(a) > 1:
                        if re.search( r'[d][)]',a[-2][:4] ) == None:
                            print( questions_intake[-1], a[-2][:4])
                            # print( re.search( r'[c][)]',a[-2][:4] ) != None )
                            # print( re.search( r'[dc][)]',a[-2][:4] ) )
                            questions_intake[-1].extend( ["c) NONE","d) NONE"] )
                        if questions_intake[-1][1] != '':
                            print(questions_intake[-1])
                            questions_intake[-1].insert(1, '')
                    else:
                        questions_intake[-1].append('')
                if a.count("View Answer") == 1:
                    a.remove("View Answer")
                if re.search(r'[abcd][)]', a[0][:4]):
                    questions_intake[-1].extend(a)
                    if re.search(r'[d][)]', a[-2][:4]) is None:
                        print(questions_intake[-1])
                        # print(re.search( r'[d][)]',a[-1][:4] ) != None)
                        questions_intake[-1].extend(["c) NONE", "d) NONE"])
            # print(a)
            # ratings.append(rating.text)
        # print(len(prices))

        for a in ans:
            a = (a.text).splitlines()
            answers.append(a)
            # print(prices[counter])
            # print(ans[counter][0])
            try:
                questions_intake[counter].append(a[0])
                print(questions_intake[counter])
            except:
                print(answers[counter])
                print(questions_intake[counter])
                answers.pop(-1)
                counter -= 1
            # print(a)
            counter += 1
            # print(counter)
        # print(prices)
        print(len(questions_intake), len(answers))
        print(f"percentage_completed : {round(((listy.index(i)+1)/len(listy)) * 100, 1)}%")
    for n in questions_intake:
        counter_1 += 1
        dict = {}
        dict["index"] = counter_1
        dict["question"] = n[0]
        dict["img_opt"] = n[1]
        dict["A"] = n[2]
        dict["B"] = n[3]
        dict["C"] = n[4]
        dict["D"] = n[5]
        dict["Answer"] = n[6]
        listing_dict.append(dict)
        print(listing_dict[counter_1-1])
    print("processed!")
    Fields = ["index", "question", "img_opt", "A", "B", "C", "D", "Answer"]
    with open(f'full_{subject}_v-3.1.csv', 'w', encoding='utf-8') as file:
        writer = csv.DictWriter(file, Fields)
        writer.writeheader()
        writer.writerows(listing_dict)
    return "Completed!"
