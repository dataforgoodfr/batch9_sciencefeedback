import xmltodict
import datetime
import collections
import gzip
import shutil
import wget
import os
import re
import numpy as np
import time
import elasticsearch


def gunzip_shutil(source_filepath, dest_filepath, block_size=65536):
    with gzip.open(source_filepath, 'rb') as s_file, \
            open(dest_filepath, 'wb') as d_file:
        shutil.copyfileobj(s_file, d_file, block_size)

def download_file_and_open_as_dict(file_nb):
    if len(str(file_nb)) == 3:
        file_nb = str(0) + str(file_nb)
    elif len(str(file_nb))==4:
        file_nb = str(file_nb)
    
    [os.remove(elem) for elem in os.listdir() if 'tmp' in elem]

    url = f'https://ftp.ncbi.nlm.nih.gov/pubmed/baseline/pubmed21n{file_nb}.xml.gz'
    print(f'Beginning file {file_nb} download')
    wget.download(url, 'tmp_gzip_file')

    gunzip_shutil('tmp_gzip_file', 'tmp_xml_file', block_size=65536)
    
    print('parsing file')
    with open('tmp_xml_file', 'r') as myfile:
        articles_dict = xmltodict.parse(myfile.read())
        
    os.remove("tmp_xml_file") 
    os.remove("tmp_gzip_file")
    
    return articles_dict

def extract_date(article_dict):
    try:
        date = datetime.datetime(int(article_dict['MedlineCitation']['Article']['ArticleDate']['Year']), 
                                 int(article_dict['MedlineCitation']['Article']['ArticleDate']['Month']), 
                                 int(article_dict['MedlineCitation']['Article']['ArticleDate']['Day']))
    except KeyError:
        try:
            date = datetime.datetime(int(article_dict['MedlineCitation']['DateCompleted']['Year']), 
                                     int(article_dict['MedlineCitation']['DateCompleted']['Month']), 
                                     int(article_dict['MedlineCitation']['DateCompleted']['Day']))
        except KeyError:
            date = datetime.datetime(int(article_dict['MedlineCitation']['DateRevised']['Year']), 
                                     int(article_dict['MedlineCitation']['DateRevised']['Month']), 
                                     int(article_dict['MedlineCitation']['DateRevised']['Day']))
    return date

def extract_abstract(article_dict):
    final_abstract= None
    if 'Abstract' in article_dict['MedlineCitation']['Article']:
        if article_dict['MedlineCitation']['Article']['Abstract']['AbstractText']:
            abstract = article_dict['MedlineCitation']['Article']['Abstract']['AbstractText']
            if isinstance(abstract,list):
                final_abstract = []
                for item in abstract:
                    if isinstance(item,str):
                        final_abstract.append(item)
                    elif isinstance(item,collections.OrderedDict):
                        if '#text' in item:
                            final_abstract.append(item['#text'])
                final_abstract = '\n'.join(final_abstract)
            if isinstance(abstract,str) :
                final_abstract = article_dict['MedlineCitation']['Article']['Abstract']['AbstractText']
    return final_abstract

def extract_doi(article_dict):
    if 'ELocationID' in article_dict['MedlineCitation']['Article']:
        if isinstance(article_dict['MedlineCitation']['Article']['ELocationID'],collections.OrderedDict):
            type_eloc = article_dict['MedlineCitation']['Article']['ELocationID']['@EIdType']
            valid = article_dict['MedlineCitation']['Article']['ELocationID']['@ValidYN']
            if type_eloc == 'doi' and valid == 'Y':
                try:
                    return article_dict['MedlineCitation']['Article']['ELocationID']['#text']
                except: 
                    print(article_dict['MedlineCitation']['Article']['ELocationID'])
                    
        elif isinstance(article_dict['MedlineCitation']['Article']['ELocationID'],list):
            for dicto in article_dict['MedlineCitation']['Article']['ELocationID']:
                if dicto['@EIdType'] == 'doi' and dicto['@ValidYN'] == 'Y':
                    return dicto['#text']

    else:
        if 'ArticleIdList' in article_dict['PubmedData']:
            try:
                for sub_dict in article_dict['PubmedData']['ArticleIdList']['ArticleId']:
                    if '@IdType' in sub_dict:
                        if sub_dict['@IdType'] == 'doi':
                            return sub_dict['#text']
                    else:
                        print(article_dict['PubmedData']['ArticleIdList'])
            except TypeError:
                pass
    return None
            
def extract_authors(article_dict):
    if 'AuthorList' in article_dict['MedlineCitation']['Article']:
        authors = article_dict['MedlineCitation']['Article']['AuthorList']['Author']
        if not isinstance(authors,list):
            authors = [authors]
        
        authors = [{key:value for key,value in sub_dict.items() if key != '@ValidYN'} for sub_dict in authors if sub_dict['@ValidYN']=='Y']
        for author in authors:
            for elem in ['ForeName','Initials','LastName']:
                if elem not in author:
                    author[elem] = ''
            if 'AffiliationInfo' in author:
                if isinstance(author['AffiliationInfo'],list):
                    author['AffiliationInfo'] = [value['Affiliation'] for value in author['AffiliationInfo']]
                if isinstance(author['AffiliationInfo'],collections.OrderedDict):
                    affils = list(author['AffiliationInfo'].values())
                    try:
                        affils = [string.split(';') for string in affils]
                        affils = [elem.strip() for elem in sum(affils, [])]
                    except AttributeError:
                        affils = affils[0].strip()
                    
                    author['AffiliationInfo'] = affils
            else:
                author['AffiliationInfo'] = ['']

            try:
                first_affil = author['AffiliationInfo'][0][:20]
            except:
                display(author['AffiliationInfo'])

            author['ConcatId'] = (author['ForeName']+'-'+author['Initials']+'-'+author['LastName']+'_'+first_affil).replace(' ','')
            author['AffiliationInfo'] = set(author['AffiliationInfo'])
        return authors
    else:
        return []

def extract_keywords(article_dict):
    pattern = r"['.,\/!$%\^&\*;:{}=\-_`~()\#\]"
    keywords = None
    if 'KeywordList' in article_dict['MedlineCitation']:
        try:
            keywords = [value['#text'].lower().strip() for value in article_dict['MedlineCitation']['KeywordList']['Keyword'] if '#text' in value]
        except TypeError:
            try:
                if ';' in article_dict['MedlineCitation']['KeywordList']['Keyword']['#text']:
                    keywords = article_dict['MedlineCitation']['KeywordList']['Keyword']['#text'].split(';')
                elif ',' in article_dict['MedlineCitation']['KeywordList']['Keyword']['#text']:
                    keywords = article_dict['MedlineCitation']['KeywordList']['Keyword']['#text'].split(',')
                
                keywords = [keyword.lower().strip() for keyword in keywords]
                keywords = [re.sub(pattern,' ',keyword).strip() for keyword in keywords]
            except:
                pass
    return keywords

def extract_relevant_info(article_dict):
    pmid = article_dict['MedlineCitation']['PMID']['#text']
    doi = extract_doi(article_dict)
    title = article_dict['MedlineCitation']['Article']['ArticleTitle']
        
    date = extract_date(article_dict)
    
    journal = article_dict['MedlineCitation']['MedlineJournalInfo']
    journal['FullName']= article_dict['MedlineCitation']['Article']['Journal']['Title']
    
    authors = extract_authors(article_dict)
    
    keywords = extract_keywords(article_dict)
    abstract = extract_abstract(article_dict)
    
    sub_dict = {'pmid':pmid,'doi':doi,'date':date,'journal':journal,'authors':authors,'keywords':keywords,
               'abstract':abstract,'title':title}
    
    return sub_dict

def wrapper_download_and_turn_to_dict(string):
    print(string)
    articles_dict = download_file_and_open_as_dict(str(string))
    master_dict = {}
    for article_dict in articles_dict['PubmedArticleSet']['PubmedArticle']:
        if article_dict['MedlineCitation']['Article']['Language'] == 'eng':
            try:
                sub_dict = extract_relevant_info(article_dict)
                master_dict[sub_dict['pmid']] = sub_dict
            except Exception as e:
                print(e)
    print('loaded as dict')
    return master_dict