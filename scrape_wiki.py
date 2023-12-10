'''
Description - Scrape the MSM wiki for breeding info,
              monster pictures, islands, etc.

Authors - Jordyn Kuhn
Date Created - 7.7.2023
Last Updated - 7.16.2023
Last Tested - 7.16.2023
Status - Working
'''

#import
import requests
from bs4 import BeautifulSoup
import re

#global variables for exporting data
islands = []
images = []
rare_images = []
names = []
rare_names = []
all_names = ''
statue_list = []

#Check if an item is in a list
def in_list(item, list):
    for i in range(0, len(list)):
        if list[i] == item:
            return True
    return False

#removes empty strings in a list
def remove_empty(list):
    while '' in list:
        list.remove('')

#Scrape and return the islands for each monster
def scrape_islands():
    URL = "https://mysingingmonsters.fandom.com/wiki/Islands#List_of_Islands"
    req = requests.get(URL)
    content = req.text
    soup = BeautifulSoup(content, features="html.parser")
    soup.prettify()
    table = soup.find(class_ = "article-table")
    info_big = table.find_all("a")
            
    for i in range(0, len(info_big)):
        islands.append((info_big[i].get_text()))
    
    remove_empty(islands)

    return islands

            
#scrape monsters and images
def scrape_mons():
    URL = "https://mysingingmonsters.fandom.com/wiki/Monster_Portraits"
    req = requests.get(URL)
    content = req.text
    soup = BeautifulSoup(content, features="html.parser")
    soup.prettify()
    gal_one = soup.find(id = "gallery-1")
    gallery_one = gal_one.find_all(class_='wikia-gallery-item')
    gallery_one_img = gal_one.find_all('img')
    gal_two = soup.find(id = 'gallery-2')
    gallery_two = gal_two.find_all(class_='wikia-gallery-item')
    gallery_two_img = gal_two.find_all('img')

    for i in range(0, len(gallery_one)):
        names.append(gallery_one[i].get_text())

    for i in range(0, len(gallery_one_img)):
        images.append(gallery_one_img[i].get('src'))

    for i in range(0, len(gallery_two)):
        rare_names.append(gallery_two[i].get_text())

    for i in range(0, len(gallery_two_img)):
        rare_images.append(gallery_two_img[i].get('src'))

    for str in reversed(rare_images):
        if 'data:image/gif' in str:
            rare_images.remove(str)
    
    for str in reversed(images):
        if 'data:image/gif' in str:
            images.remove(str)

#Scrape breeding combinations
def scrape_breed():
    breed_combo = ""
    for monster in names:
        URL = "https://mysingingmonsters.fandom.com/wiki/" + monster
        req = requests.get(URL)
        content = req.text
        soup = BeautifulSoup(content, features="html.parser")
        soup.prettify()
        market = False
        statue = False
        
        table = soup.find(class_='mw-parser-output')
        element = table.find_all("p")
        text = table.find_all("li")
        
        print(monster)

        for i in range(0, len(element)):
            if ("Market") in element[i].get_text() :
                market = True
                if("zapping") in element[i].get_text() :
                    statue = True
                    statue_list.append(monster)
                    zap_info = find_statue_info(table)
                
        if statue:
            print(" + Zap")
            print(zap_info)
        elif market:
            print(" + Buy From Market")

        for i in range(0, len(text)):
            if text[i].get_text().startswith(" + "):
                print(text[i].get_text())

#Scrape Statue Information
def find_statue_info(table):
    table_two = table.find_all("div")
    print (table_two)
    eggs = table_two.find_all("a")
    num_eggs = table_two.find_all("sup")
    print(eggs)
    count = 0
    zap_info = ""

    try:
        for i in range(0, len(eggs)):
            if "Island" not in eggs[i].get('title'):
                zap_info += (" - " + eggs[i].get('title') +"\n")
                zap_info += (" -- " + num_eggs[count].get_text()+'\n')
                count += 1
    except:
        return
    
    return(zap_info)





#updates
def update_data():
    with open('C:\\1My Files\\Code\\AutoMSM\\data\\all_names.txt', 'w') as out:
        all_names = str(names) + '\n' + str(rare_names)
        out.write(str(all_names))

    with open('C:\\1My Files\\Code\\AutoMSM\\data\\names.txt', 'w') as out:
        out.write(str(names))

    with open('C:\\1My Files\\Code\\AutoMSM\\data\\rare_names.txt', 'w') as out:
        out.write(str(rare_names))

    with open('C:\\1My Files\\Code\\AutoMSM\\data\\islands.txt', 'w') as out:
        out.write(str(islands))

    with open('C:\\1My Files\\Code\\AutoMSM\\data\\images_list.txt', 'w') as out:
        out.write(str(images))

    with open('C:\\1My Files\\Code\\AutoMSM\\data\\rare_images_list.txt', 'w') as out:
        out.write(str(rare_images))

#Download the image files to the corr. folder
def update_img():
    for i in range(0, len(rare_images)):
        file = 'C:\\1My Files\\Code\\AutoMSM\\data\\images\\monster_icons\\' + rare_names[i] + '.png'
        r = requests.get(rare_images[i], allow_redirects = True)
        open(file, 'wb').write(r.content)

    for i in range(0, len(images)):
        file = 'C:\\1My Files\\Code\\AutoMSM\\data\\images\\monster_icons\\' + names[i] + '.png'
        r = requests.get(images[i], allow_redirects = True)
        open(file, 'wb').write(r.content)

#main program
if __name__ == '__main__':
    scrape_mons()
    scrape_islands()
    scrape_breed()
    update_data()
    update_img()

