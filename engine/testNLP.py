import spacy
import string
import requests
import pandas as pd
import numpy as np
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize import TweetTokenizer
from nltk.tokenize.toktok import ToktokTokenizer
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import re, time
from bs4 import BeautifulSoup
import unicodedata
import dateutil.parser as dparser

verbes_list = ['trouver', 'donner', 'parler','aider','atteindre', 'aimer','essayer' ,'passer', 'demander', 'sembler', 'laisser', 'rester', 'penser', 'regarder', 'arriver', 'chercher', 'porter', 'entrer', 'appeler', 'tomber', 'commencer', 'montrer', 'arreter', 'jeter', 'monter', 'lever', 'ecouter', 'continuer', 'ajouter', 'jouer', 'marcher', 'garder', 'manquer', 'retrouver', 'rappeler', 'quitter', 'tourner', 'crier', 'songer', 'presenter', 'exister', 'envoyer', 'expliquer', 'manger', 'finir', 'agir', 'etre', 'avoir', 'faire', 'dire', 'pouvoir', 'aller', 'voir', 'savoir', 'vouloir', 'venir', 'falloir', 'devoir', 'croire', 'prendre', 'mettre', 'tenir', 'entendre', 'repondre', 'rendre', 'connaître', 'paraître', 'sentir', 'attendre', 'vivre', 'sentir', 'comprendre', 'devenir', 'retenir', 'ecrire', 'reprendre', 'suivre', 'partir', 'mourir', 'ouvrir', 'lire', 'servir', 'recevoir', 'perdre', 'sourire', 'apercevoir', 'reconnaître', 'descendre', 'courir', 'permettre', 'offrir', 'apprendre', 'souffrir']
pronoms_list = ['je', 'me','comme', 'm', 'moi', 'qui', 'que','quoi','quand','dont','où','ou','jusqu','pourquoi','ou','est','donc','or','ni','car' ,'quoi','si', 'qui', 'on', 'toutun', 'une', 'un', 'une', 'uns', 'unes', 'autre', 'autres', 'd', 'l', 'aucun', 'aucune', 'aucuns', 'aucunes', 'certains', 'certaine', 'certains', 'certaines', 'tel', 'telle', 'tels', 'telles', 'tout', 'toute','ns', 'tous', 'toutes', 'meme', 'memes', 'nul', 'nulle', 'nuls', 'nulles', 'quelqu', 'quelques', 'autrui', 'quiconque', 'aucuns', 'quoi', 'qu', 'est-ce', 'lequel', 'auquel', 'duquel', 'laquelle', 'laquelle', 'lesquels', 'auxquels', 'desquels', 'lesquelles', 'auxquelles', 'desquelles', 'dont', 'ou', 
'lequel', 'auquel', 'duquel','via','la','bon','plus', 'laquelle', 'a', 'lesquels', 'auxquels', 'desquels', 'lesquelles','lequel','jusqu','jusqu a','jusqu on','jusqu il', 'auxquelles', 'desquelles', 'tu', 'te', 't', 'toi', 'nous', 'vous', 'il', 'elle', 'ils', 'elles', 'se', 'en', 'y', 'le', 'la', 'l', 'les', 'lui', 'soi', 'leur', 'eux', 'celui', 'ci', 'celle', 'ceux', 'celles', 'ce', 'ceci', 'cela', 'ça', 'lui', 'leur', 'mien', 'tien', 'sien', 'mien', 'ne', 'tienne', 'sienne', 'miens', 'tiens', 'siens', 'miennes', 'tiennes', 'siennes', 'notre', 'votre', 'leur', 'notre', 'votre', 'leur', 'notres', 'votres', 'leurs']


nlp = spacy.load("fr_core_news_md", parse=True, tag=True, entity=True)

def token(sentence): #Tokenize et retourne les labels
    doc = nlp(sentence)
    return [(X.text, X.label_) for X in doc.ents]

def remove_accented_chars(text):
    text = unicodedata.normalize('NFKD', text).replace(u'œ', 'oe').encode('ascii', 'ignore').decode('utf-8', 'ignore')
    return text

def remove_special_characters(text, remove_digits=False):
    pattern = r'[^A-Za-z0-9\s]+' if not remove_digits else r'[^A-Za-z\s]+'
    text = re.sub(pattern, '', text)
    return text

def lemmatize_text(text):
    text = nlp(text)
    text = ' '.join([token.lemma_ if token.lemma_ != '-PRON-' else "" for token in text])
    text = nlp(text)
    text = ' '.join([token.text if token.pos_ != "AUX" else "" for token in text]) 
    return text

def normalize_corpus(text):
    text = text.lower()
    
    normalize_text = lemmatize_text(text)
    #print("1 lem :",normalize_text)
    normalize_text = remove_stopwords(normalize_text)
    #print("2 stopwords :",normalize_text)
    normalize_text = remove_accented_chars(normalize_text)
    #print("3 rm_accent_char :",normalize_text)
    normalize_text = remove_special_characters(normalize_text)
    #print("4 rm_special_char :",normalize_text)
    normalize_text = remove_uniqueCarac(normalize_text)
    #print("5 rm_unique_char :",normalize_text)
    normalize_tokens = word_tokenize(normalize_text)
    
    return normalize_tokens

def remove_stopwords(text):
    stopword_list = stopwords.words('french')
    stopword_list.extend(['rt','fav','al'])
    tokens = word_tokenize(text)
    tokensWithoutSW = []
    delete = -1
    for i in range(len(tokens)) :
        if "@" == tokens[i] :
            delete=i+1
        if i != delete :
            if tokens[i] not in stopword_list and tokens[i] not in verbes_list and tokens[i] not in pronoms_list and "http" not in tokens[i] and "@" not in tokens[i] and "t.co" not in tokens[i] :
                tokensWithoutSW.append(tokens[i])
    filtered_text = ' '.join(tokensWithoutSW)
    return filtered_text

def remove_uniqueCarac(text):
    t = ""
    words = text.split()
    for w in words :
        if len(w)>1 :
            t += w + " "
    return t
