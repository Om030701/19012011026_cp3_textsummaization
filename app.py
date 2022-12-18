
#adding core packages
import tkinter as tk
from tkinter import *
#this module is for adding tabs
from tkinter import ttk
from tkinter.scrolledtext import *
#FOR OPEN FILE
from tkinter import filedialog
from tkinter import messagebox
#adding user defined modules
from abstractive import abs_summary
from abstractive_1 import abs_large_summary
from abstractive_2 import abs_tifu_summary
#some other packages
import time
#sumy packages
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer


timestr=time.strftime("%Y%m%d-%H%M%S")
#adding web scrapping packages
from bs4 import BeautifulSoup
from urllib.request import urlopen


#SPACY SUMMARIZATION
# NLP Pkgs
import spacy
nlp=spacy.load('en_core_web_sm')

# Pkgs for Normalizing Text
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
# Import Heapq for Finding the Top N Sentences
from heapq import nlargest

def text_summarizer(raw_docx):
    raw_text = raw_docx
    docx = nlp(raw_text)
    stopwords = list(STOP_WORDS)
    # Build Word Frequency # word.text is tokenization in spacy
    word_frequencies = {}
    for word in docx:
        if word.text not in stopwords:
            if word.text not in word_frequencies.keys():
                word_frequencies[word.text] = 1
            else:
                word_frequencies[word.text] += 1

    maximum_frequncy = max(word_frequencies.values())

    for word in word_frequencies.keys():
        word_frequencies[word] = (word_frequencies[word] / maximum_frequncy)
    # Sentence Tokens
    sentence_list = [sentence for sentence in docx.sents]

    # Sentence Scores
    sentence_scores = {}
    for sent in sentence_list:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if len(sent.text.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_frequencies[word.text.lower()]
                    else:
                        sentence_scores[sent] += word_frequencies[word.text.lower()]

    summarized_sentences = nlargest(7, sentence_scores, key=sentence_scores.get)
    final_sentences = [w.text for w in summarized_sentences]
    print(final_sentences)
    summary = ' '.join(final_sentences)
    return summary



window=Tk()
window.title("CP3 text summarrizer")
window.geometry('700x500')
#style (to make the tabs go from up to down)
style = ttk.Style(window)
style.configure('lefttab.TNotebook',tabposition = 'wn')


#adding tabs
tab_control= ttk.Notebook(window,style='lefttab.TNotebook')
tab1= ttk.Frame(tab_control)
tab2= ttk.Frame(tab_control)
tab3= ttk.Frame(tab_control)
tab4= ttk.Frame(tab_control)
tab5= ttk.Frame(tab_control)


#Adding tabs to controller
tab_control.add(tab1,text='HOME')
tab_control.add(tab2,text='FILE')
tab_control.add(tab3,text='URL')
tab_control.add(tab4,text='COMPARE')
tab_control.add(tab5,text='ABOUT')

#Adding labels
label1=Label(tab1,text='Summarizer',padx= 5,pady = 5,cursor='dot',font=('Times', 24))
label1.grid(column=0,row=0)
label2=Label(tab2,text='File Processing',padx= 5,pady = 5,font=('Times', 24))
label2.grid(column=0,row=0)
label3=Label(tab3,text='URL',padx= 5,pady = 5,font=('Times', 24))
label3.grid(column=0,row=0)
label4=Label(tab4,text='Comparer',padx= 5,pady = 5,font=('Times', 24))
label4.grid(column=0,row=0)
label5=Label(tab5,text='Conclusion',padx= 5,pady = 5,font=('Times', 24))
label5.grid(column=0,row=0)

tab_control.pack(expand=1,fill = 'both')
#functions
def get_summary():
    raw_text=entry.get('1.0',tk.END)
    final_text = text_summarizer(raw_text)
    print(final_text)
    result = '\nSummary: {}'.format(final_text)
    tab1_display.insert(tk.END,result)

def save_summary():
    raw_text = entry.get('1.0', tk.END)
    if raw_text.compare("end-1c", "==", "1.0"):

        print("none")

    else:
        final_text = text_summarizer(raw_text)
        file_name='yoursummary'+timestr+'.txt'
        with open(file_name,'w') as f:
            f.write(final_text)
        result = '\nName of file: {}\nSummary: {}'.format(file_name,final_text)
        tab1_display.insert(tk.END,result)
def get_file_summary():
    raw_text=displayed_file.get('1.0',tk.END)
    final_text = text_summarizer(raw_text)
    print(final_text)
    result = '\nSummary: {}'.format(final_text)
    tab2_display_text.insert(tk.END,result)
#clear functions
def clear_text():
    entry.delete('1.0',END)
def clear_display_result():
    tab1_display.delete('1.0',END)

def clear_text_file():
    displayed_file.delete('1.0',END)
def clear_text_result():
    tab2_display_text.delete('1.0',END)

# Clear For URL
def clear_url_entry():
	url_entry.delete(0,END)

def clear_url_display():
	tab3_display_text.delete('1.0',END)

#open file function
def openfiles():
   file1=tk.filedialog.askopenfilename(filetype=(('Text Files',".txt"),("All files","*")))
   read_text=open(file1).read()
   displayed_file.insert(tk.END,read_text)


# Fetch Text From Url
def get_text():
    raw_text = str(url_entry.get())
    page=urlopen(raw_text)
    soup=BeautifulSoup(page)
    fetched_text=' '.join(map(lambda p:p.text,soup.find_all('p')))
    url_display.insert(tk.END,fetched_text)
def get_url_summary():
	raw_text = url_display.get('1.0',tk.END)
	final_text = text_summarizer(raw_text)
	result = '\nSummary:{}'.format(final_text)
	tab3_display_text.insert(tk.END,result)

# COMPARER FUNCTIONS

def use_spacy():
	raw_text = entry1.get('1.0',tk.END)
	final_text = text_summarizer(raw_text)
	print(final_text)
	result = '\nSpacy Summary:{}\n'.format(final_text)
	tab4_display.insert(tk.END,result)

def use_abs():
	raw_text = str(entry1.get('1.0',tk.END))
	final_text =abs_summary(raw_text)
	print(final_text)
	result = '\nPegasus xsum  Summary:{}\n'.format(final_text)
	tab4_display.insert(tk.END,result)

def use_abs_large():
	raw_text = entry1.get('1.0',tk.END)
	final_text = abs_large_summary(raw_text)
	print(final_text)
	result = '\nParaphrase summary:{}\n'.format(final_text)
	tab4_display.insert(tk.END,result)

def use_abs_tifu():
    raw_text = str(entry1.get('1.0', tk.END))
    final_text = abs_tifu_summary(raw_text)
    print(final_text)
    result = '\nCNN Daily Summary:{}\n'.format(final_text)
    tab4_display.insert(tk.END, result)

# Clear entry widget
def clear_compare_text():
	entry1.delete('1.0',END)

def clear_compare_display_result():
	tab4_display.delete('1.0',END)

#main Home tab
l1=Label(tab1,text='Enter Text to Summarize :')
l1.grid(column=0,row=1)
entry=ScrolledText(tab1,height=10,wrap=tk.WORD)
entry.grid(row=2,column=0,columnspan=2,pady=5,padx=5)

#buttons
button1=Button(tab1,text="Reset",command=clear_text, width=12,bg='#ff80ff',fg='#000000',bd=10,activebackground="white")
button1.grid(row=4,column=0,padx=10,pady=10)

button2=Button(tab1,text="Summarize",command=get_summary, width=12,bg='#ff80ff',fg='#000000',bd=10,activebackground="white")
button2.grid(row=4,column=1,padx=10,pady=10)

button3=Button(tab1,text="Clear Result", command=clear_display_result,width=12,bg='#ff80ff',fg='#000000',bd=10,activebackground="white")
button3.grid(row=5,column=0,padx=10,pady=10)

button4=Button(tab1,text="Save Summary",command=save_summary, width=12,bg='#ff80ff',fg='#000000',bd=10,activebackground="white")
button4.grid(row=5,column=1,padx=10,pady=10)

#Display screen for results
tab1_display= ScrolledText(tab1,height=10,wrap=tk.WORD)
tab1_display.grid(row=7,column=0,columnspan=3,padx=5,pady=5)


#FILE PROCESSING TAB

l1=Label(tab2,text='Open file to summarize',padx=5,pady=5)
l1.grid(column=0,row=1)
displayed_file= ScrolledText(tab2,height=7)
displayed_file.grid(row=2,column=0,columnspan=3,padx=5,pady=3)


#buttons
b0=Button(tab2,text="Open file",command=openfiles, bd=10,width=12,bg='#25D366',fg='#000000',activebackground='white')
b0.grid(row=3,column=0,padx=10,pady=10)

b1=Button(tab2,text="Reset",command=clear_text_file, width=12,bg='#A020F0',fg='#000000',activebackground='white',bd=10)
b1.grid(row=3,column=1,padx=10,pady=10)

b2=Button(tab2,text="Summarize", command=get_file_summary,width=12,bg='#eedd82',fg='#000000',activebackground='white',bd=10)
b2.grid(row=4,column=0,padx=10,pady=10)

b3=Button(tab2,text="Clear result",command=clear_text_result, width=12,bg='#856363',fg='#000000',activebackground='white',bd=10)
b3.grid(row=4,column=1,padx=10,pady=10)

b4=Button(tab2,text="Close",command=window.destroy, width=12,bg='#03A9F4',fg='#000000',activebackground='white',bd=10)
b4.grid(row=3,column=2,padx=10,pady=10)

#display screen
#tab2_display_text=text(tab2)
tab2_display_text=ScrolledText(tab2,height=10,wrap=tk.WORD)
tab2_display_text.grid(row=7,column=0,columnspan=3,padx=5,pady=5)
#allows you to edit
tab2_display_text.config(state=NORMAL)

# URL TAB
l1=Label(tab3,text="Enter URL To Summarize :")
l1.grid(row=1,column=0)

raw_entry=StringVar()
url_entry=Entry(tab3,textvariable=raw_entry,width=50)
url_entry.grid(row=1,column=1)

# BUTTONS
button1=Button(tab3,text="Reset",command=clear_url_entry, width=12,bg='#B7ACA5',fg='#000000',activebackground='rosybrown',bd=10)
button1.grid(row=4,column=0,padx=10,pady=10)

button2=Button(tab3,text="Get Text",command=get_text, width=12,bg='#F7A06D',fg='#000000',bd=10,activebackground='rosybrown')
button2.grid(row=4,column=1,padx=10,pady=10)

button3=Button(tab3,text="Clear Result", command=clear_url_display,width=12,bg='#F1E9E3',fg='#000000',bd=10,activebackground='rosybrown')
button3.grid(row=5,column=0,padx=10,pady=10)

button4=Button(tab3,text="Summarize",command=get_url_summary, width=12,bg='#8B4500',fg='#000000',activebackground='rosybrown',bd=10)
button4.grid(row=5,column=1,padx=10,pady=10)

# Display Screen For Result
url_display = ScrolledText(tab3,height=10,wrap=tk.WORD)
url_display.grid(row=7,column=0, columnspan=3,padx=5,pady=5)


tab3_display_text = ScrolledText(tab3,height=10,wrap=tk.WORD)
tab3_display_text.grid(row=10,column=0, columnspan=3,padx=5,pady=5)



#COMPARER TAB

l1=Label(tab4,text="Enter Text To Summarize :")
l1.grid(row=1,column=0)

entry1=ScrolledText(tab4,height=10,wrap=tk.WORD)
entry1.grid(row=2,column=0,columnspan=3,padx=5,pady=3)

# BUTTONS
button1 = Button(tab4, text="Reset", command=clear_compare_text, width=12,bd=10, bg='#ff6699', fg='#000000',activebackground='lightpink')
button1.grid(row=4, column=0, padx=10, pady=10)

button2 = Button(tab4, text="SpaCy", command=use_spacy, width=12, bg='#0073e6',bd=10, fg='#000000',activebackground='lightpink')
button2.grid(row=4, column=1, padx=10, pady=10)

button3 = Button(tab4, text="Clear Result", command=clear_compare_display_result,bd=10, width=12, bg='#e6e600', fg='#000000',activebackground='lightpink')
button3.grid(row=5, column=0, padx=10, pady=10)

button4 = Button(tab4, text="Pegasus_xsum", command=use_abs, width=12, bg='#00e64d',bd=10, fg='#000000',activebackground='lightpink')
button4.grid(row=4, column=2, padx=10, pady=10)

button5 = Button(tab4, text="Paraphrase", command=use_abs_large, width=12, bg='#ff6633',bd=10, fg='#000000',activebackground='lightpink')
button5.grid(row=5, column=1, padx=10, pady=10)

button6 = Button(tab4, text="CNN-Daily Mail", command=use_abs_tifu, width=12,bd=10, bg='#1ba9c5',activebackground='lightpink', fg='#fff')
button6.grid(row=5, column=2, padx=10, pady=10)

# Display Screen For Result

tab4_display = ScrolledText(tab4,height=15,state='normal',wrap=tk.WORD)
tab4_display.grid(row=7,column=0, columnspan=3,padx=5,pady=5)

# About TAB
about_label = Label(tab5,text="This text summarizer was created to ensure that the user gets multiple options to summarize the text and get the best possible summary.\nCreated by Om(19012011026) and Akshat(19012011106) ",pady=5,padx=5)
about_label.grid(column=0,row=1)



window.mainloop()



































