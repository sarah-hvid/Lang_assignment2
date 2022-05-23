# Assignment 2 - Sentiment and NER
 
Link to GitHub of this assignment: https://github.com/sarah-hvid/Lang_assignment2

## Assignment description
The purpose of this assignment is to perform sentiment analysis and named entity recognition (NER). A CSV file should be created showing the sentiment scores and the NE's of the type: GPE (geo political entity), for each article title. A bar plot should be created of the top 20 most mentioned GPE's.\
The full assignment description is available in the ```assignment2.md``` file.

## Methods
The fake or real news CSV file is initially loaded from the ```data``` folder and split by fake or real news. The two new dataframes are then processed almost identically in a for-loop. Initially, for each row in the dataframe the text id and title is saved. The title is then used to calculate the  ```Vader``` compund sentiment score. ```Spacy``` is then used to create spacy documents. The user may specify whether to use the small or large ```spacy``` model in the commandline. The small model is the default value. The documents are used with ```Spacytextblob``` to calculate polarity and subjectivity scores. They are also used to find and save the GPE named entities. A bar plot is created of the 20 most mentioned GPE's. The color will differ depending on the input data (real or fake). The plot will be saved in the ```output``` folder, and the name will vary depending on the input data and the ```spacy``` model used. A CSV file with the same naming convention will also be saved in the ```output``` folder.

## Usage
In order to run the script, certain modules need to be installed. These can be found in the ```requirements.txt``` file. The folder structure must be the same as in this GitHub repository (ideally, clone the repository).
```bash
git clone https://github.com/sarah-hvid/Lang_assignment2.git
cd Lang_assignment2
pip install -r requirements.txt
```
The data used in the assignment is the __fake_or_real_news.csv__ file. The data is available in the shared ```CDS-LANG``` folder. The file must be placed in the ```data``` folder in order to replicate the results.\
The current working directory when running the script must be the one that contains the ```data```, ```output``` and ```src``` folder.\
\
How to run the script from the command line: 

__The news corpus script__\
Standard:
```bash
python src/news_corpus.py
```
Specified spacy model:
```bash
python src/news_corpus.py -s large
```

Examples of the outputs of the script can be found in the ```output``` folder. 

## Results
The GPE's found in the titles of the articles are different for the fake and real news. Using the small ```spacy``` model, the real news data contains most mentions of Obama (though not a GPE NE), Iran and U.S./America. The fake news contains most mentions of US/U.S./America, Russia and Syria. So while the mention of the United States is similar in both datasets, Russia and Syria is mostly mentioned in fake news. Looking at the large ```spacy``` models output, it can be seen that _Obama_ is no longer picked up as a GPE. The results are clearly more precise. The real news contains most mentions of Iran, US/America/U.S. and Iowa. For the fake news, it is Russia by far, US/U.S./America and Syria. Therefore, it appears that Russia is the best predictor of real or fake news, as the real contains 20 mentions while the fake contains 100. 

**Real news, spacy small**

<img src="/output/news_real_sm_gpe.png">

**Fake news, spacy small**

<img src="/output/news_fake_sm_gpe.png">

**Real news, spacy large**

<img src="/output/news_real_lg_gpe.png">

**Fake news, spacy large**

<img src="/output/news_fake_lg_gpe.png">

The results of the sentiment analysis are difficult to compare without further analysis.\
The CSV file created contains the following information:
 
 [**CSV file, real news, spacy large**](/output/news_real_lg.csv)
 
 | id  | title | polarity  | subjectivity | vader_compund  | GPE |
| ------------- | ------------- | ------------- | ------------- | ------------- | ------------- |
| 3608 | Kerry to go to Paris in gesture of sympathy | 0.0 | 0.0 | 0.3612 | ['Paris'] | 
| 875 | The Battle of New York: Why This Primary Matters | 0.2681818181818182 | 0.4772727272727273 | -0.3612 | [] |
| 95 | ‘Britain’s Schindler’ Dies at 106 | 0.0 | 0.0 | 0.0 | ['Britain'] |
| ...  | ...  | ...  | ... | ...  | ... |
 
