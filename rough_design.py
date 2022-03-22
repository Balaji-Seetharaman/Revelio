# import the installed Jira library
#import libraries
from jira import JIRA
from jira.exceptions import JIRAError
import sys
import string
import matplotlib.pyplot as plt
import numpy
from wordcloud import WordCloud
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import stopwords

options = {'server': 'https://jira.extremenetworks.com/'}

try:
    print("start!")
    jira = JIRA(options=options, auth=('', ''))
except JIRAError as e:
    if e.status_code == 401:
        print ("Login to JIRA failed. Check your username and password")
print ("done!")


# Fetch all fields
allfields = jira.fields()
#print(allfields) 
# Make a map from field name -> field id
name_map = {field['name']:field['id'] for field in allfields} 
#print(name_map)
Summary_list = []
size = 1000
start = 0
for singleIssue in jira.search_issues('project = "EXOS" AND "Found In Build" ~ "31.7" AND type = Defect',start,size):
    issue = jira.issue(singleIssue.key)
    #print(issue)
    #print(issue.fields[name_map['Feature']])
    Summary_list.append((singleIssue.key,singleIssue.fields.summary))
    #Summary_list.append(((singleIssue.key),(singleIssue.fields.summary),getattr(singleIssue.fields.name_map["Feature"]).value,getattr(singleIssue.fields.name_map["Function"].value)))

print(Summary_list) 
#print(len(Summary_list))
df =  pd.DataFrame(Summary_list,columns =['Key', 'Summary'])
#df =  pd.DataFrame(Summary_list,columns =['ID', 'Summary', 'Feature', 'Function'])
df.name ='Summary'
print (df)

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

df['Summary'] = df['Summary'].apply(clean_text)
df['Summary'] = df['Summary'].apply(remove_Stopwords)
df['Summary'] = df['Summary'].apply(lemmatize_text)
df['Num_words_text'] = df['Summary'].apply(lambda x:len(str(x).split())) 

wordcloud = WordCloud(background_color="white",width=1600, height=800).generate(' '.join(df['Summary'].tolist()))
plt.figure( figsize=(20,10), facecolor='k')
plt.imshow(wordcloud)
plt.savefig('data2.png')






