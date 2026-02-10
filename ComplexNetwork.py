import os
from pypdf import PdfReader
from collections import Counter
import string
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import csv
import time
import sqlite3
import networkx as nx
import math
from pyvis.network import Network
import webbrowser
from multiprocessing import Pool

# Setup SQL Database
conn = sqlite3.connect('ESreferences.db')
cursor = conn.cursor()

# Store all the pdf's in an array
folder_path = r"D:\Epstein Files\PDF's"
pdfFiles = []
for root, dirs, files in os.walk(folder_path):
    for file in files:
        if file.endswith('.pdf'):
            pdfFiles.append(os.path.join(root, file))
    
# Get all keywords to search for
keys = {}
with open('word_categories.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)  # Skip header
    for row in reader:
        keys[row[0]] = row[1]


def timeElapsed(startTime, pdfIndex):
            # Get Time
        elapsed = time.time() - startTime
        avg_time = elapsed / pdfIndex
        remaining = avg_time * (len(pdfFiles) - pdfIndex)
        
        return remaining

def process_pdf(pdf):
    results = []
    surrResults = []
    reader = PdfReader(pdf)
    for page in reader.pages:
        text = page.extract_text()
        text_lower = text.lower()
        
        fileNumIndex = text.find('EFTA0')
        fileNum = text[fileNumIndex:fileNumIndex+12]

        for key in keys:
            if key.lower() in text_lower:
                textIndex = text_lower.find(key)
                surrText = text[textIndex-25:textIndex+25]
                results.append((fileNum, keys[key]))
                surrResults.append((fileNum, surrText))

    return results, surrResults

def searhForKeywords(): # Searches though every pdf for the keywords and stored by document
    # Clear the table
    cursor.execute('DROP TABLE IF EXISTS ESreferences')
    cursor.execute('DROP TABLE IF EXISTS ESsurrounding')

    # Create the table if it doesn't exist (Format: fileNum, category)
    cursor.execute('''CREATE TABLE IF NOT EXISTS ESreferences
                    (fileNumber TEXT, category TEXT)''')
    conn.commit()

        # Create the table if it doesn't exist (Format: fileNum, category)
    cursor.execute('''CREATE TABLE IF NOT EXISTS ESsurrounding
                    (fileNumber TEXT, surroundingText TEXT)''')
    conn.commit()

    startTime = time.time()
    refRows = []
    surrRows = []
    with Pool() as pool:
        for pdfIndex, (refResult, surrResult) in enumerate(pool.imap_unordered(process_pdf, pdfFiles), 1):
            remaining = timeElapsed(startTime, pdfIndex)
            print(f"Processing file {pdfIndex}/{len(pdfFiles)} | {round(pdfIndex/len(pdfFiles)*100, 2)}% | ETA: {round(remaining/60, 1)} min")
            refRows.extend(refResult)
            surrRows.extend(surrResult)
    cursor.executemany('''INSERT INTO ESreferences (fileNumber, category) VALUES (?, ?)''', refRows)
    cursor.executemany('''INSERT INTO ESsurrounding (fileNumber, surroundingText) VALUES (?, ?)''', surrRows)
    conn.commit()

    print("Exported Data to ESreferences.db")

def pyVisGraph(G):
    # PyVis for HTML graph
    net = Network(height='750px', width='100%', bgcolor='#222222', font_color='white')

    for node in G.nodes(): # Loop through g.nodes and add nodes to netx graph
        count = G.nodes[node].get('count', 1)
        net.add_node(node, label=str(node), size=math.log(count) * 2, 
                     font={'size': 100, 'color': 'white'},
                     color={'background': 'rgba(31, 72, 126, 1)',
                            'border': 'rgba(31, 72, 126, 1)',
                            'border': 'rgba(31, 72, 126, 1)',
                            'highlight': {'background': 'rgba(128, 32, 26, 1)', 'border': 'rgba(251, 54, 64, 1)'}})

    for u, v in G.edges(): # Loop through g.edges and add edges to netx graph
        weight = G[u][v]['weight']
        net.add_edge(u, v, value=weight * 10,
                     color={'color': 'rgba(36, 123, 160, 0.3)', 'highlight': 'rgba(251, 54, 64, 1)'})

    net.toggle_physics(False)
    net.toggle_drag_nodes(False)

    # Calculate positions with NetworkX and apply them to pyvis nodes
    pos = nx.spring_layout(G, k=10, scale=1000)

    # Set pos of each node
    for node, (x, y) in pos.items():
        net.get_node(node)['x'] = x
        net.get_node(node)['y'] = y

    # Display graph and print nodes
    print(f"Nodes: {G.number_of_nodes()}")
    print(f"Edges: {G.number_of_edges()}")
    net.save_graph('graph.html')
    webbrowser.open('graph.html')

def generateGraph():
    G = nx.Graph()
    sizes = []

    # Get each category from the database
    cursor.execute('SELECT category, COUNT(*) FROM ESreferences GROUP BY category')
    results = cursor.fetchall()

    for category, count in results:
        G.add_node(category, count=count)
        sizes.append(count)
    
    # Get each file from the database
    cursor.execute('''
    SELECT r1.category, r2.category, COUNT(*)
    FROM ESreferences r1
    JOIN ESreferences r2 ON r1.fileNumber = r2.fileNumber
    WHERE r1.category < r2.category
    GROUP BY r1.category, r2.category
    ''')
    results = cursor.fetchall()

    for c1, c2, count in results:
        G.add_edge(c1, c2, weight=count)
        

    print(f"Number of nodes: {G.number_of_nodes()}")
    weights = [math.log(G[u][v]['weight'] + 1) for u, v in G.edges()]
    pos = nx.spring_layout(G, k=10, iterations=50)
    nx.draw(G, 
            pos=pos, 
            with_labels=True, 
            node_size=sizes, 
            node_color='lightgreen',
            font_size=20,
            edge_color='lightblue',
            width=weights)
    
    pyVisGraph(G)
    #plt.show()

#generateGraph()

if __name__ == '__main__':
    input = input("Do you want to regenerate the database (will take a long time): Y/N \n")
    if (input.lower() == 'y'):
        searhForKeywords()
    else:
        generateGraph()
