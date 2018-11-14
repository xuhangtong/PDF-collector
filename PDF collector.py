#continue working
#1. replace dictionary with list of string /done
#2. sort the files to folder according to html page names/done
#3. estimate how many links in total /done
#4. optimize speed
#5. optimize class structure
#6. avoid go to external links like youtube
from bs4 import BeautifulSoup
import requests
import os.path

#make a good folder name for sorting
def good_folder_name(folder_name):
        dosnames=['CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9']
        final=''
        for char in folder_name:
                if not (char in '<>:"/\|?*;'):
                    if ord(char)>31:
                      final+=char
        if final in dosnames:
          #oh dear...
          raise SystemError('final string is a DOS name!')
        elif final.replace('.', '')=='':
                final = 'no name'
          #raise SystemError('final string is all periods!')
        return final

#define the domain name
domain_name = "http://www.escocorp.com"

#intiate a list to store URLs to explore
urls_list = ['http://www.escocorp.com']

#i is an index
i = 0

#BEGIN THE LOOP
while i<1000: 
        print(str(i)+ ': ' + urls_list[i])


        if urls_list[i].endswith('.jpg') or \
           urls_list[i].endswith('.png') or \
           urls_list[i].endswith('.mp4') or \
           urls_list[i].endswith('.JPG') or \
           urls_list[i].endswith('.PNG'):
                   i+=1
                   continue

        #REQUEST THE URL, AND THROW A EXPECT IF ERROR
        try:
                result = requests.get(urls_list[i])
        except requests.exceptions.RequestException as e:
                print(e)
                i+=1
                continue
        print (result.status_code) #PRINT THE CODE

        #PASS THE REQUESTED PAGE TO BS4 FOR PROCESS, IF NO TITLE, SKIP THE PAGE
        c = result.content
        soup = BeautifulSoup(c)
        if soup.title == None:
                i+=1
                continue

        #CONTRUCT A FOLDER NAME TO MAKE A DIR 
        folder_name = ''.join(soup.title.string.split()) #folder name
        folder_name = good_folder_name(folder_name)
        print(folder_name)

        #FIND ALL HREF IN THE PAGE
        for link in soup.find_all('a', href=True):
                current_link = link['href']

                #IF THE HREF LINK TO AN PDF, CREAT A FOLDER AND SAVE
                if current_link.endswith('pdf'):
                    if current_link.startswith('/'):
                         current_link = domain_name+current_link
                    if not os.path.exists(folder_name): #create folder
                            os.makedirs(folder_name)
                    print (current_link)
                    file_name = current_link.split('/')[-1]
                    file_name = os.path.join(folder_name, file_name)
                    print (file_name)
                    if os.path.isfile(file_name):
                            print(file_name + " already exist")
                            continue
                    try :
                            response = requests.get(current_link)
                    except requests.exceptions.RequestException as er:
                            print(er)
                            continue
                    with open(file_name, 'wb') as f:
                            f.write(response.content)

                #ELSE SAVE THE HREF LINK TO URL LIST FOR FURTHER VISIT
                else:
                        if current_link.startswith('/'):
                                current_link = domain_name + current_link
                        if current_link not in urls_list:
                                if current_link.startswith(domain_name):
                                        urls_list.append(current_link)

        i+=1
        print('current url numbers: ' + str(len(urls_list)))



                        
        
