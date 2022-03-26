from django.shortcuts import render
from jira import JIRA
from jira.exceptions import JIRAError
import sys
import string
import matplotlib.pyplot as plt
import matplotlib 
matplotlib.use('Agg')
import pandas as pd
import io
import urllib, base64
from wordcloud import WordCloud
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import stopwords
import requests
from requests.auth import HTTPBasicAuth
from io import BytesIO
import time

def remove_Stopwords(text ):
        stop_words = set(stopwords.words('english')) 
        words = word_tokenize( text.lower() ) 
        sentence = [w for w in words if not w in stop_words]
        return " ".join(sentence)
        
def lemmatize_text(text):
        wordlist=[]
        lemmatizer = WordNetLemmatizer() 
        sentences=sent_tokenize(text)
        for sentence in sentences:
            words=word_tokenize(sentence)
            for word in words:
                wordlist.append(lemmatizer.lemmatize(word))
        return ' '.join(wordlist) 

def clean_text(text ): 
        delete_dict = {sp_character: '' for sp_character in string.punctuation} 
        delete_dict[' '] = ' ' 
        table = str.maketrans(delete_dict)
        text1 = text.translate(table)
        textArr= text1.split()
        text2 = ' '.join([w for w in textArr]) 
        
        return text2.lower()

def word_cloud(text):
    wc = WordCloud(width=1600, height=800).generate(' '.join(text))
    plt.figure(figsize=(15,15), facecolor='k')
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.savefig('d1app/static/data2.png',facecolor='k', bbox_inches='tight')
    image = io.BytesIO()
    plt.savefig(image, format='png')
    image.seek(0)  # rewind the data
    string = base64.b64encode(image.read())

    image_64 = 'data:image/png;base64,' + urllib.parse.quote(string)
    return image_64





def home(request):
    # import the installed Jira library
#import libraries


    # options = {'server': 'https://jira.extremenetworks.com/'}

    # try:
    #     print("start!")
    #     jira = JIRA(options=options, auth=('bseetharaman', 'Bluebird$450'))
    # except JIRAError as e:
    #     if e.status_code == 401:
    #         print ("Login to JIRA failed. Check your username and password")
    # print ("done!")


    # # Fetch all fields
    # allfields = jira.fields()
    # #print(allfields) 
    # # Make a map from field name -> field id
    # name_map = {field['name']:field['id'] for field in allfields} 
    # #print(name_map)
    # Summary_list = []
    # size = 1000
    # start = 0
    # for singleIssue in jira.search_issues('project = "EXOS" AND "Found In Build" ~ "31.7" AND type = Defect',start,size):
    #     issue = jira.issue(singleIssue.key)
    #     #print(issue)
    #     #print(issue.fields[name_map['Feature']])
    #     Summary_list.append((singleIssue.key,singleIssue.fields.summary))
    #     #Summary_list.append(((singleIssue.key),(singleIssue.fields.summary),getattr(singleIssue.fields.name_map["Feature"]).value,getattr(singleIssue.fields.name_map["Function"].value)))

    # print(Summary_list) 

    # #print(len(Summary_list))
    # df =  pd.DataFrame(Summary_list,columns =['Key', 'Summary'])
    # #df =  pd.DataFrame(Summary_list,columns =['ID', 'Summary', 'Feature', 'Function'])
    # df.name ='Summary'
    # print (df)
    # df.to_csv('d1app/static/data.csv')
    theurl = 'https://jira.extremenetworks.com/rest/com.midori.jira.plugin.betterexcel/1.0/xls/xls-view/64/render?tempMax=1000&context=issue_navigator&filterId=44341&columns=filter'
    r=requests.get(theurl, auth=HTTPBasicAuth('bseetharaman', 'mo-api-lTV8X2lNeoEupoW4rkiqP13K'))
    xd = pd.read_excel(BytesIO(r.content))
    xd.drop(xd.tail(n).index,inplace=True)
    #print(xd)
    xd = xd[['Key', 'Feature','Function','Summary']]
    xd.to_csv('jira.csv')
    df = pd.read_csv('jira.csv')

    df['Summary'] = df['Summary'].apply(clean_text)
    df['Summary'] = df['Summary'].apply(remove_Stopwords)
    df['Summary'] = df['Summary'].apply(lemmatize_text)
    df['Num_words_text'] = df['Summary'].apply(lambda x:len(str(x).split())) 
    wordcloud = word_cloud(df['Summary'].tolist())
    #plot(df['Summary'].tolist())

    return render(request,'d1app/home.html',{'wordcloud':wordcloud})
    

