"""
A script that performs sentiment and NER analysis on the Fake/Real news dataset.
"""

# Data analysis tools
import os, argparse
import pandas as pd
import collections
from collections import Counter
import itertools
from tqdm import tqdm

# NLP tools
import spacy
from spacytextblob.spacytextblob import SpacyTextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
analyzer = SentimentIntensityAnalyzer()

# visualisations
import matplotlib.pyplot as plt


def parse_args():
    '''
    Function that specifies the available commandline arguments.
    '''
    # Initialise argparse
    ap = argparse.ArgumentParser()
    
    # command line parameters
    ap.add_argument("-s", "--spacy", required = False, help = "Write 'small' or 'large' as input for the corresponding spacy model size")
        
    args = vars(ap.parse_args())
    return args


def load_data(): # maybe allow file input
    '''
    Function that loads the fake or real news dataset and splits it to separate dataframes. Returns a list of the two dataframes. 
    '''
    filepath = os.path.join("data", 'fake_or_real_news.csv')
    df = pd.read_csv(filepath)
    
    # exploiting the accidental index column as a text id column
    df.rename(columns={'Unnamed: 0': 'id'}, inplace=True) 

    # Creating the two data sets, filtering by fake and real
    df_real = df[df.label == 'REAL']
    df_fake = df[df.label == 'FAKE']
    
    df_list = [df_real, df_fake]
    
    return df_list


def vader_sent(df):
    '''
    Function that calculates the Vader compound sentiment score for each row of the title column. Also grabs the id and text data for later use. 
    
    df: A dataframe containing id and title column.
    '''
    # Initiating empty lists
    id_list = []
    title_list = []
    vader_list = []
    
    # Iterrating over each row of the dataframe
    for index, row in df.iterrows(): 
        id_list.append(row['id'])
        title_list.append(row['title'])

        headline = row['title']
        dict_of_scores = analyzer.polarity_scores(headline) # Getting the vader sentiment scores
        vader_list.append(dict_of_scores)
        
    # Initiating empty vader list
    comp_list = []
    
    #looping through each dictionary
    for vader_dict in vader_list: 
        # getting the values of the dict if the key is compound
        for key, value in vader_dict.items():
            if key == 'compound':
                comp_list.append(value)
                
    return id_list, title_list, comp_list


def spacy_doc(df):
    '''
    Function that loads the nlp model specified and creates a list of spacy documents.
    
    df: dataframe containing title column with text. 
    '''
    # parse argument
    args = parse_args()
    spacy_model = args['spacy']
    
    if spacy_model == None:
        nlp = spacy.load("en_core_web_sm")
        nlp.add_pipe('spacytextblob')
        
    elif spacy_model == 'small':
        nlp = spacy.load("en_core_web_sm")
        nlp.add_pipe('spacytextblob')
        
    elif spacy_model == 'large':
        nlp = spacy.load("en_core_web_lg")
        nlp.add_pipe('spacytextblob')

    # create spacy documents
    docs = tqdm(list(nlp.pipe(df.title)))
              
    return docs
    
    
def spacy_sent(docs):
    '''
    Function that calculates the Spacy polarity and subjectivity scores for each document.
    
    docs: a list of spacy documents. 
    '''
    # Initiating empty lists
    polarity_score = []
    subjectivity_score = []


    # Looping through each doc
    for doc in docs:
        # getting the textblob sentiment scores
        pol_scores = doc._.blob.polarity
        polarity_score.append(pol_scores)

        sub_scores = doc._.blob.subjectivity
        subjectivity_score.append(sub_scores)
    
    return polarity_score, subjectivity_score

def spacy_ner(docs):
    '''
    Function that finds named entities of the GPE type in a list of spacy documents. 
    
    docs: a list of spacy documents.
    '''
    gpe_result = []
    
    # Looping through each doc
    for doc in docs:

        # Initiating an empty list per doc for the NE's
        gpe_in_list = []

        # Keeping the entities if they are locations
        for token in doc.ents:
            if token.label_ == 'GPE':
                gpe_in_list.append(token.text)

        gpe_result.append(gpe_in_list) # appending the inner list to the outer list
        
    return gpe_result


def count_lists(gpe_result):
    '''
    Function that unnests a list of lists and counts the occurences of the elements in them. The top 20 values are kept. The element name and number of occurences are returned as two lists. 
    
    gpe_result: a list of lists.
    '''
    # Flattening the list of the locations, and creating an unnested version of the list
    gpe_flat = itertools.chain(*gpe_result)
    gpe_flat = list(gpe_flat)

    # Counting the elements of the gpe list
    gpe_count = collections.Counter(gpe_flat) 

    # sorting the count dictionary by value and keeping the top 20
    gpe_dict = dict(sorted(gpe_count.items(), reverse = True, key=lambda item: item[1])[0:20])
    
    # creating lists of the locations and values from the count dictionary
    locations = list(gpe_dict.keys())
    values = list(gpe_dict.values())
    
    return locations, values


def plot_gpe(locations, values, df_type):
    '''
    Function that creates a barplot with varying color depending on the input data. The plot is saved in the output folder. The name is determined by input parameters.
    
    locations: list of gpe's.
    values: list of the counts of each location.
    df_type: numeric variable specified in the main function, dependent on the input data. 
    '''
    # parse argument
    args = parse_args()
    spacy_model = args['spacy']

    if spacy_model == 'large':
        spacy_model = 'lg'
    else:
        spacy_model = 'sm'

    # modify plot by input dataset
    if df_type == 1:
        df_name = 'real'
        color = 'maroon'
    elif df_type == 2:
        df_name = 'fake'
        color = 'blue'
    
    # initiating the figure and its size
    fig = plt.figure(figsize = (16, 8))

    # creating the bar plot
    plt.bar(locations, values, color = color, width = 0.6)

    # specifying labels and sizes
    plt.xlabel("Locations", fontsize = 15)
    plt.ylabel("Number of mentions", fontsize = 15)
    plt.title(f"Top 20 locations in {df_name} news data", fontsize = 20)

    # saving the plot
    plt.savefig(f'output/news_{df_name}_{spacy_model}_gpe.png')
    
    return


def create_csv(id_list, title_list, polarity_score, subjectivity_score, comp_list, gpe_result, df_type):
    '''
    Function that takes the 6 lists of results and creates a dataframe. The dataframe is saved in the output folder. The name of the file depends on the input data. 
    
    id_list: a list containing the text id 
    title_list: a list containing the titles, text 
    polarity_score: a list containing the spacy polarity score 
    subjectivity_score: a list containing the spacy subjectivity score 
    comp_list: a list containing the vader compounded sentiment scores 
    gpe_result: a list containing the spacy GPE's
    df_type: a numeric value specified in the main function
    '''
    # parse argument
    args = parse_args()
    spacy_model = args['spacy']
    
    if spacy_model == 'large':
        spacy_model = 'lg'
    else:
        spacy_model = 'sm'
        
    if df_type == 1:
        df_name = 'real'
    elif df_type == 2:
        df_name = 'fake'
        
    df = pd.DataFrame(list(zip(id_list, title_list, polarity_score,
                               subjectivity_score, comp_list, gpe_result)),
               columns =['id', 'title', 'polarity', 'subjectivity', 'vader_compund', 'GPE'])
    
    df.to_csv(f"output/news_{df_name}_{spacy_model}.csv", index = False)
        
    return


def main():
   '''
   The process of the entire script.
   '''
    # loading dataframes
    df_list = load_data()
    
    # looping through the two dataframes, and ensuring the output of the functions is on the correct split
    for df in df_list:
        if (df['label'] == 'REAL').any() == True:
            df_type = 1
        elif (df['label'] == 'FAKE').any() == True:
            df_type = 2
        
        # getting the vader sentiment score
        id_list, title_list, comp_list = vader_sent(df)

        # getting the spacy sentiment score and the NE's
        print('[INFO] Fitting Spacy ...')
        docs = spacy_doc(df)
        polarity_score, subjectivity_score = spacy_sent(docs)
        gpe_result = spacy_ner(docs)
        print('[INFO] Spacy done')
        
        # plotting the GPE's
        locations, values = count_lists(gpe_result)
        plot_gpe(locations, values, df_type)
        
        # creating a CSV of all results
        create_csv(id_list, title_list, polarity_score, subjectivity_score, comp_list, gpe_result, df_type)
        print(f'[INFO] Output success: dataframe {df_type}')
        
    print('[INFO] Script succes.')
        
    return


if __name__ == '__main__':
    main()