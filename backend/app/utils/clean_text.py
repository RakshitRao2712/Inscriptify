import re
def clean_text(text):
    text = text.replace('\n\n', '\n')
    text = re.sub(r'[^\x00-\x7F]+', ' ', text) #removes noisy unicode
    text = re.sub(r'\s+', ' ', text) #normalize spaces
    return text.strip()