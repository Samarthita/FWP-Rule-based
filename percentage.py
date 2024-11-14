import nltk
import re
import spacy
from nltk.tokenize import sent_tokenize, word_tokenize
nltk.download('punkt')

nlp = spacy.load("en_core_web_sm")

def custom_sent_tokenize(text):
    sentences = re.split(r'(?<!\d)\.(?!\d)', text)
    return [s.strip() for s in sentences if s.strip()]

synonyms = {
    'Principal': ['loan', 'lend', 'borrow', 'principal', 'rs.', 'sum'],
    'Time': ['period', 'span', 'years', 'months', 'days', 'year'],
    'Rate of Interest': ['rate', 'rate of interest', '%'],
    'Interest': ['interest', 'simple interest'],
    'Amount': ['amounts', 'total', 'sum of money amounts']
}

def find_synonym_key(word, corpus):
    for key, synonym_list in synonyms.items():
        if word.lower() in [x.lower() for x in synonym_list]:
            return key
    return None

# Extract data from the corpus
def extract_data_from_corpus(corpus):
    data = {}
    principal_match = re.search(r'(\d+(?:\.\d+)?) Rs', corpus, re.IGNORECASE)
    time = re.search(r'(\d+) (years|months|days|year)', corpus, re.IGNORECASE)
    rate_of_interest = re.search(r'(\d+(?:\.\d+)?) %', corpus, re.IGNORECASE)
    simple_interest = re.search(r'simple interest is (\d+(?:\.\d+)?)', corpus, re.IGNORECASE)

    if simple_interest:
        data['Simple Interest'] = float(simple_interest.group(1))

    if principal_match:
        data['Principal'] = float(principal_match.group(1))

    if time:
        data['Time'] = int(time.group(1))

    if rate_of_interest:
        data['Rate of Interest'] = float(rate_of_interest.group(1))

    return data

# Function to calculate simple interest
def calculate_simple_interest(principal, rate_of_interest, time):
    return (principal * rate_of_interest * time) / 100

# Function to calculate principal
def calculate_principal(simple_interest, rate_of_interest, time):
    return (simple_interest * 100) / (rate_of_interest * time)

# Function to calculate time
def calculate_time(principal, rate_of_interest, simple_interest):
    return (simple_interest * 100) / (rate_of_interest * principal)

# Function to calculate rate of interest
def calculate_rate_of_interest(principal, simple_interest, time):
    return (simple_interest * 100) / (time * principal)


corpus = input("Enter the financial corpus: ")

doc = nlp(corpus)

question_words = ['what', 'how', 'where', 'when', 'why', 'which', 'who', 'whom']
keywords = ['calculate', 'find', 'determine', 'compute', 'evaluate', 'figure out', 'derive']

sentences = custom_sent_tokenize(corpus)

def is_question(sentence):
    words = word_tokenize(sentence.lower())
    if words[0] in question_words or any(keyword in words for keyword in keywords):
        return True
    return False

question_sentences = [sentence for sentence in sentences if is_question(sentence)]

if question_sentences:
    print("Question sentence(s) found:")
    for sentence in question_sentences:
        print(sentence)
else:
    print("No question sentences found in the corpus.")

# Print the given data
data = extract_data_from_corpus(corpus)
print("Given Data:")
for key, value in data.items():
    print(f"{key}: {value} {'rs' if key=='Principal' or key=='Simple Interest' else 'years' if key=='Time' else '%'}")

# Calculate and print the results
if 'Simple Interest' in data and 'Rate of Interest' in data and 'Time' in data:
    principal = calculate_principal(data['Simple Interest'], data['Rate of Interest'], data['Time'])
    print(f"Answer = Principal: {principal} rs")

elif 'Principal' in data and 'Rate of Interest' in data and 'Time' in data:
    simple_interest = calculate_simple_interest(data['Principal'], data['Rate of Interest'], data['Time'])
    print(f"Answer = Simple Interest: {simple_interest} rs")

elif 'Principal' in data and 'Simple Interest' in data and 'Time' in data:
    rate_of_interest = calculate_rate_of_interest(data['Principal'], data['Simple Interest'], data['Time'])
    print(f"Answer = Rate of Interest: {rate_of_interest} %")

elif 'Principal' in data and 'Rate of Interest' in data and 'Simple Interest' in data:
    time = calculate_time(data['Principal'], data['Rate of Interest'], data['Simple Interest'])
    print(f"Answer = Time: {time} years")

if not any(key in data for key in ['Simple Interest', 'Principal', 'Time', 'Rate of Interest']):
    print("Insufficient data to perform calculations.")
