import re #Regular expression operasyonlari icin
import json 
from bs4 import BeautifulSoup
from selenium import webdriver
 

with open("data.json", "w") as f: #scraped datalarımızı data.json dosyasında tututacağız
    json.dump([], f)

def write_json(new_data, filename='data.json'): #Dictionary olarak elmizde olan scraped dataları dosyamıza yazılır
    with open(filename,'r+') as file:
        # Ilk başta dosyamızda olan data bir dict'te tutuyoruz
        file_data = json.load(file)
        # Sonra yeni gelen dict(scraped data) olan dict'imize append edilir 
        file_data.append(new_data)
        # Sets file's current position at offset.
        file.seek(0)
        # Son olarak tekrardan json'a donusturulur ... indent = 4 ==> json formati icin 
        json.dump(file_data, file, indent = 4)



driver = webdriver.Chrome()
page = driver.get('https://www.8notes.com/piano/classical/sheet_music/') # Getting page HTML through request
soup = BeautifulSoup(driver.page_source, 'html.parser') # Parsing content using beautifulsoup

links = soup.select("table tbody tr") # Selecting all the songs
difficulties = soup.select("table.table_list tbody tr td.level_type img")  ### ==>"difficulty"

i = 0
for difficulty in difficulties: #Tüm parçaların listelendiği sayfadan Parçanın zorluk bilgisi için
    difficulty = difficulty.get_attribute_list('alt')
    difficulties[i] = difficulty[0]
    i += 1

#print(difficulties)

j = 0
for link in links:  #Her parçanın özgün sayfasından data scrape işlemler için
    link_attribute = link.get_attribute_list('onclick')
    link_attribute = link_attribute[0][20:-1]
    #print(link_attribute)

    parcalarinUrl ='https://www.8notes.com/' + link_attribute
    #elements_url.append(parcalarinUrl)
    #print(parcalarinUrl)

    driver.get(parcalarinUrl) #Parçanın özgün sayfasına gidilir
    newSoup = BeautifulSoup(driver.page_source, 'html.parser')
    porteInfoList = newSoup.select('ul li a.mp3_list')[0]
    porteInfoList = porteInfoList.get_attribute_list('href')[0]
    #print(infoList)

    downloadUrl = 'https://www.8notes.com/' + porteInfoList[1:] ### ==>"img"
    #print(downloadUrl)

    midiInfoList = newSoup.select('div ul li a.midi_list')[0]
    midiInfoList = midiInfoList.get_attribute_list('href')[0]
    
    midiIndirUrl = 'https://www.8notes.com/' + midiInfoList[1:] ### ==>"midi"
    #print(midiIndirUrl)

    aboutInfoList = newSoup.select("table.comp_table tbody tr td div.artist_col2")
    if len(aboutInfoList) == 4 : #Bazı sayfaların about kismi digerlerden farkli oldugu icin
        aboutDict = {       ### ==>"about"
            "Title" : newSoup.select('table.comp_table tbody tr td h2')[0].text,
            "Artist" : re.sub('[^a-zA-Z0-9 \.]', ' ', aboutInfoList[0].text),
            "Born" : re.sub('[^a-zA-Z0-9 \.]', ' ', aboutInfoList[1].text),
            "Died" : re.sub('[^a-zA-Z0-9 \.]', ' ', aboutInfoList[2].text) ,
            "The Artist" : re.sub('[^a-zA-Z0-9 \.]', ' ', aboutInfoList[3].text) ,
        }
    else:
        aboutDict = { #about kismini digerlerden farkli olanlarin link yazilsin
            "about_url": parcalarinUrl
        }    
    #print(aboutDict)    

    totalScrapedInfo = {
        "img" : downloadUrl ,               #Parçanın porte imgesinin indirme bağlantısı
        "midi" : midiIndirUrl ,             #Parçanın MIDI dosya indirme bağlantısı
        "about" : aboutDict ,               #Parçanın hakkında bilgisi
        "difficulty" : difficulties[j] ,    #Parçanın zorluk bilgisi
    }
    j += 1


    #Artık datalarımızı json dosyamıza yazılır
    write_json(totalScrapedInfo) 

print("******************  Web Scraping Islemi Basariyla Tamamlanmistir!  ******************")

















#re.sub('[^a-zA-Z0-9 \.]', '', aboutInfoList[0].text)
#//table[@class = "comp_table"]/tbody/tr/td/div[@class='artist_col2']





    