from bs4 import BeautifulSoup as soup
from webbot import Browser
import os
import pandas as pd

def remove_space(str):
    return str.replace(' ', '')

async def update_database():
    my_file = 'classes.csv'

    # check if file exists 
    if os.path.exists(my_file):
        os.remove(my_file)

        # Print the statement once the file is deleted  
        print(f'An existing {my_file} has been found. The file: {my_file} will be deleted.')
    else:
        print(f'The file: {my_file} does not exist. Creating file now...')

    web = Browser()
    web.go_to('http://aisis.ateneo.edu/')
    web.click('click here')

    mirror = web.get_current_url().split('j_aisis')

    # enters credentials into the site
    ID_NUM = os.getenv('ID_NUM')
    PASSWORD = os.getenv('PASSWORD')

    web.type(ID_NUM, into='userName')
    web.type(PASSWORD, into='password')

    web.click('Sign in') # successfully signs into AISIS
    # web.click('CLASS SCHEDULE')
    web.go_to(f'{mirror[0]}j_aisis/J_VCSC.do')

    # html parsing
    page_soup = soup(web.get_page_source(), "html.parser")

    filename = 'subjects.csv'
    f = open(filename, 'w')

    headers = 'subject_code,section,course_title,units,time,room,instructor,max_no,lang,level,free_slots,remarks,s,p\n'

    f.write(headers)

    # grabs each product
    departments = page_soup.findAll(
        lambda t: t.name == 'option' and t.parent.attrs.get('name') == 'deptCode'
    )

    subjects = []
    subject_info = []

    i = 1

    for dept in departments:
        web.click('Display Class Schedule')
        page_soup = soup(web.get_page_source(), "html.parser")
        raw_data = page_soup.findAll('td', {'class':'text02'}) # gets the info in the subjects table
        j = 0 # column counter
        
        for data in raw_data:
            if j == 14:
                j = 0
                subjects.append(subject_info)
                subject_info = []
                f.write('\n')
            f.write(data.text.replace(',', '|') + ',')
            subject_info.append(data.text)
            j += 1

        f.write('\n')
        
        if i < len(departments):
            web.click(departments[i].text)
            i += 1

    f.close()

    databasefile = 'subjects.csv'

    # rearranges the csv file for more optimal searching
    db = pd.read_csv(databasefile, skip_blank_lines=True, names=['subject_code', 'section', 'course_title', 'units', 'time', 'room', 'instructor', 'max_no', 'lang', 'level', 'free_slots', 'remarks', 's', 'p'])

    # removes space in subject code
    db['subject_code'] = db['subject_code'].apply(remove_space)

    db.sort_values(by=['subject_code'], ascending=True).to_csv(databasefile, index=False)