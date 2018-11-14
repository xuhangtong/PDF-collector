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

#define the domain name
domain_name = "http://www.escocorp.com"

#intiate a list to store URLs to explore
urls_list = ['http://www.escocorp.com/EN/Products/Pages/securelift.aspx']

#i is an index
i = 0

#BEGIN THE LOOP
while i<100: 
        print(str(i)+ ': ' + urls_list[i])
        
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
                    response = requests.get(current_link)
                    file_name = current_link.split('/')[-1]
                    file_name = os.path.join(folder_name, file_name)
                    print (file_name)
                    if os.path.isfile(file_name):
                            print(file_name + " already exist")
                            continue
                    with open(file_name, 'wb') as f:
                            f.write(response.content)

                #ELSE SAVE THE HREF LINK TO URL LIST FOR FURTHER VISIT
                else:
                        if current_link .startswith('/'):
                                current_link = domain_name + current_link
                        if current_link not in urls_list:
                                if current_link.startswith('http'):
                                        urls_list.append(current_link)

        i+=1
        print('current url numbers: ' + str(len(urls_list)))


                        
        
