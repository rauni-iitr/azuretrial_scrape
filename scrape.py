#! /home/raunak/xyz/my_env/bin/pip
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests


df_link=pd.read_excel('Link.xlsx')
ls=df_link.URL.tolist()
standard_link_from_csv=[x for x in ls if (x.split('/')[2]=='towardsdatascience.com'
                                        or x.split('/')[2]=='medium.com'
                                        or x.split('/')[2]=='www.kdnuggets.com'
                                        or x.split('/')[2]=='heartbeat.fritz.ai'
                                        or x.split('/')[2]=='realpython.com')]

#standard function to extract from any url, argument given as dict.
def extracted_csv(d):
    url=d['url']
    print('Searching data at: ',url)
    
    if(url[-1]=='/'):
        Name=url.split('/')[-2]
    else:
        Name=url.split('/')[-1]
        
    website=url.split('/')[2]
    
    element=d['element']
    print("Searching html element: ",element)
    
    id_=d.get('id_',None)
    print("Searching id attribute in element: ",id_)
    
    class_=d.get('class_',None)
    print("Searching class attribute in element: ",class_)
    
    path=d.get('path',None)
    
    response=requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    if(id_ is not None and class_ is not None):
        site_content=soup.find_all(name=element,attrs={'id':id_,'class':class_})
    elif(id_ is not None and class_ is None):
        site_content=soup.find_all(name=element,attrs={'id':id_})
    elif(id_ is None and class_ is not None):
        site_content=soup.find_all(name=element,attrs={'class':class_})
    else:
        site_content=soup.find_all(name=element)
    
    text_list=[]
    tags=[]
    d={'h1':'Header1','h2':'Header2','h3':'Header3','p':'Paragraph',
       'li':'List','pre':'code','table':'Table','img': 'Image'}
    
    for x in site_content:
        for tag in x.find_all(['h1','h2','h3','p','li','pre','table','img']):
            if(tag.name=='img' and tag.has_attr('src')):
                text_list.append('https://www.tutorialspoint.com'+tag.get('src'))
                tags.append(d[tag.name])
            elif((website=='www.tutorialspoint.com' or website=='tutorialspoint.com') and tag.name=='pre'):
                x=tag.get('class')
                if(x[0] == 'prettyprint'):
                    text_list.append(str(tag.get_text()))
                    tags.append('code')
                else:
                    text_list.append(str(tag.get_text()))
                    tags.append('output')
            else:
                text_list.append(str(tag.get_text()))
                tags.append(d[tag.name])
                
    df=pd.DataFrame({'Tag':tags,'content': text_list})

    if path is not None:
        path=path+Name+'.csv'
        df.to_csv(path,index=False)
        print("csv file saved with path {}".format(path))
    else:
        df.to_csv(Name+'.csv',index=False)
        print("csv file saved in current directory")
    print('\n')
        
    return

#function to extract chapter links from tutorial points category's topic
def get_chapters(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    chapters=soup.find_all('ul',class_="toc chapters")
    chapters_link_list=['https://www.tutorialspoint.com'+y.get('href') for x in chapters
                                                        for y in x.find_all('a')]
    return chapters_link_list

#one function to extract all the data
def call():
    
    #from links file 
    for x in standard_link_from_csv:
        standard_extract(x,'./all_csv/')
        
    #tp_category_machine_learning
    url_tp=["https://www.tutorialspoint.com/python_technologies_tutorials.htm",
            "https://www.tutorialspoint.com/machine_learning_tutorials.htm"]
    for url in url_tp:
        response = requests.get(url)
        category_soup = BeautifulSoup(response.text, 'html.parser')

        topics=category_soup.find_all('div',class_='course-box')
        topic_link_list=['https://www.tutorialspoint.com'+y.get('href') for x in topics
                                                                    for y in x.find_all('a')][:-6]
        for topic in topic_link_list:
            for chapter in get_chapters(topic):
                d={'url':chapter,'element':'div','class_':'mui-col-md-6 tutorial-content','path':'./all_csv/'}
                extracted_csv(d)
 
    #tp_jeremy_jordan
    url='https://www.jeremyjordan.me/data-science/'
    response = requests.get(url)
    category_soup = BeautifulSoup(response.text, 'html.parser')
    topics=category_soup.find_all('article')
    topic_link_list=[y.get('href') for x in topics
                                    for y in x.find_all('a') if y.get('href') is not None][1:]
    topic_link_list=[x for x in topic_link_list if x.split('/')[2] == 'www.jeremyjordan.me']
        
    for topic in topic_link_list:
        standard_extract(topic,'./all_csv/')
    
    return

standard_element_dict={
                        'medium.com':{'element':'article'},
                       'www.medium.com':{'element':'article'},
                      'towardsdatascience.com':{'element':'article'},
                       'www.towardsdatascience.com':{'element':'article'},
                        'www.tutorialspoint.com':{'element':'div','class_':'mui-col-md-6 tutorial-content'},
                        'tutorialspoint.com':{'element':'div','class_':'mui-col-md-6 tutorial-content'},
                        'jeremyjordan.me':{'element':'article'},
                        'www.jeremyjordan.me':{'element':'article'},
                        'www.kdnuggets.com':{'element':'div','id_':'post-',},
                         'kdnuggets.com':{'element':'div','id_':'post-'},
                        'heartbeat.fritz.ai':{'element':'article'},
                        'realpython.com':{'element':'div','class_':'article-body'},
                        'www.realpython.com':{'element':'div','class_':'article-body'}
                      }

#function to exract data from standard websites in standard dict
def standard_extract(url,path=None):
    website=url.split('/')[2]
    #print(website)
    d=standard_element_dict.get(website,None)
    if d is None:
        print("URL not standard.Try Basic Method by making dict")
    else:
        element=d['element']
        class_=d.get('class_',None)
        id_=d.get('id_',None)
    x={'url':url,'element':element,'path':path,'class_':class_,'id_':id_}
    
    return extracted_csv(x)
    
#print('ran')
        