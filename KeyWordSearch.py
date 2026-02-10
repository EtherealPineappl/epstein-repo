import os
from pypdf import PdfReader
from collections import Counter
import string
import nltk
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import csv
import time

# Downloads the stopwords to filter out useless words
nltk.download('stopwords')
from nltk.corpus import stopwords
stopWords = set(stopwords.words('english'))

#This dictionary contains every word and the count of each
key = {}
with open('word_categories.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    for row in reader:
        key[row[0]] = row[1]

allKeys = []
allWords = []

# Store all the pdf's in an array
folder_path = r"D:\Epstein Files\Python\source"
pdfFiles = []
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith('.pdf'):
            pdfFiles.append(os.path.join(root, file))

#Loop through all pdf's in the directory
i = 0
start_time = time.time()
for pdf in pdfFiles: 
    i += 1

    # Get Time
    elapsed = time.time() - start_time
    avg_time = elapsed / i
    remaining = avg_time * (len(pdfFiles) - i)

    # Display Progress
    print(f"Processing {pdf} | File {i}/{len(pdfFiles)} | {round(i/len(pdfFiles)*100, 2)}% | ETA: {round(remaining/60, 1)} min")


    # Open the pdf
    pdfPath = os.path.join(folder_path, pdf)
    reader = PdfReader(pdfPath)

    # Loop through each page
    for page in reader.pages:
        text = page.extract_text()

        # Split the text into individual words and loop through each.
        for word in text.split():
            cleanedWord = word.strip(string.punctuation) # Clean punc. off of the words

            if cleanedWord not in stopWords and cleanedWord.title() in key:
                allKeys.append(key[cleanedWord.title()])
            
            if cleanedWord not in stopWords and not cleanedWord.isnumeric():
                allWords.append(cleanedWord.title())

# Counter for each word
keyCount = Counter(allKeys)
wordCount = Counter(allWords)

# Export top 50000 to CSV
top_50000 = wordCount.most_common(2000)

with open('top_50000_words.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['Category', 'Count'])
    for category, count in top_50000:
        writer.writerow([category, count])

print("Exported top 2000 to top_50000_words.csv")

# ============================================================================
# GRAPH
# ============================================================================

wordcloud = WordCloud(width=800, height=500).generate_from_frequencies(keyCount)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()
