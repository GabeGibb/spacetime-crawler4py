import re
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin, urldefrag, urlunparse

#GLOBALS
visited = set()
unique_pages = 0

longest_page_url = ''
longest_page_length = 0

stopWords = ["a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren", "t", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can", "cannot", "could", "couldn", "did", "didn", "do", "does", "doesn", "doing", "don", "down", "during", "each", "few", "for", "from", "further", "had", "hadn", "has", "hasn", "have", "haven", "having", "he", "d", "ll", "s", "her", "here", "hers", "herself", "him", "himself", "his", "how", "i", "m", "ve", "if", "in", "into", "is", "isn", "it", "its", "itself", "let", "me", "more", "most", "mustn", "my", "myself", "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan", "she", "should", "shouldn", "so", "some", "such", "than", "that", "the", "their", "theirs", "them", "themselves", "then", "there", "these", "they", "re", "ve", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "wasn", "we", "were", "weren", "what", "when", "where", "which", "while", "who", "whom", "why", "with", "won", "would", "wouldn", "you", "your", "yours", "yourself", "yourselves"]
subdomains = {}

def scraper(url, resp):
    try:
        links = extract_next_links(url, resp)
        return [link for link in links if is_valid(link)]
    except Exception as e:
        print(e)
        return []

def extract_next_links(url, resp):
    '''
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    return list()
    '''
    # GLOBALS
    global visited
    global unique_pages

    global longest_page_url
    global longest_page_length 

    global subdomains

    # TODO: We may not want to do this (need to remove colon/fragmentation)
    # THIS ALSO WILL NOT TRACK REDIRECTS NEED TO CHANGE
    if resp.status != 200: #if error
        print('ERROR:', resp.status)
        visited.add(url_without_query(url))
        return []
    
    # TODO: Tokenize url by / and if there are duplicates in url, url is bad return []
    # EXAMPLE: https://www.ics.uci.edu/alumni/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/stayconnected/index.php
    # http://www.cert.ics.uci.edu/seminar/Nanda/seminar/Nanda/EMWS09/EMWS09/seminar/Nanda/seminar/Nanda/seminar/Nanda/EMWS09/seminar/Nanda/seminar/Nanda/seminar/Nanda/EMWS09/seminar/Nanda/seminar/Nanda/EMWS09/EMWS09/seminar/Nanda/seminar/Nanda/seminar/Nanda/seminar/Nanda/EMWS09/seminar/Nanda/EMWS09/seminar/Nanda/EMWS09/seminar/Nanda/seminar/Nanda/seminar/Nanda/seminar/Nanda/EMWS09/seminar/Nanda/seminar/Nanda/seminar/Nanda/seminar/Nanda/seminar/Nanda/seminar/Nanda/EMWS09/seminar/Nanda/EMWS09/seminar/Nanda/seminar/Nanda/seminar/Nanda/EMWS09/EMWS09/seminar/Nanda/seminar/Nanda/seminar/Nanda/seminar/Nanda/seminar/Nanda/seminar/Nanda/EMWS09/seminar/Nanda/EMWS09/seminar/Nanda/seminar/Nanda/EMWS09/asdf

    # TODO: Use some sort of hashing of html to get similarity score of pages, if score is too high, return []

    # Get html content, defragment, get absolute path, and add it links List if they are valid
    links = get_links(url, resp)
    # WE NOW HAVE VALID / DEFRAGMENTED LINKS

    # Filter query params to add to visited, and return links that when shortened are not in visited
    goodLinks = filter_query_params(links)
    # WE NOW HAVE ADDED LINKS WITHOUT FRAGMENTS/QUERY PARAMS TO VISITED AND RETURNED UNIQUE LINKS

    # PAGE GOOD, add to pages
    unique_pages += 1

    # KELLY TASKS!!!!!!!!!!
    # TODO: Get page length (in length of words) and compare to longest page, if longer, update longest page count and url (BEATUFIUL SOUP)
    if len(resp.raw_response.content) > longest_page_length:
        longest_page_length = len(resp.raw_response.content)
        longest_page_url = resp.url
    # TODO: Store common words using some sort of dict object (increment count if word is already in dict or set to 1 if new)
    common_words = {}
    if resp.raw_response.content: #if content exists:
        soup = BeautifulSoup(resp.raw_response.content, 'html.parser') #parsed HTML content
        for script in soup(["script", "style"]): #removes script and style tags from html doc
            script.extract()
        text = soup.get_text()
        words = text.split()


        for word in words:
            if word.isalpha() and word.lower() not in stopWords: #if word is not a stop word and is an english word
                common_words[word] = common_words.get(word, 0) + 1 #increment count if word is already in dict or set to 1 if new
        
    # TODO: Keep track of subdomains in  ics.uci.edu. 
    # NOTE: Again use a dict object to store subdomains and increment count if subdomain is already in dict or set to 1 if new (store all of them)
    
    

    return goodLinks


def url_without_query(url): # REMOVE QUERY PARAMETERS
    parsed_url = urlparse(url)
    url_without_query = urlunparse(parsed_url._replace(query="", fragment="")) 
    return url_without_query


def get_links(url, resp):
    links = []
    soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
    for anchor in soup.find_all('a', href=True):
        href = anchor['href'] # get url
        href, _ = urldefrag(href) # deframentation
        href = urljoin(resp.url, href) # getting absolute path
        if is_valid(href) and href != url and href != resp.url: # If valid or not in page
            links.append(href)


def filter_query_params(links):
    global visited
    goodLinks = []
    for link in links:
        tempLink = url_without_query(link)
        if tempLink not in visited:
            visited.add(tempLink)
            goodLinks.append(link)

    return goodLinks
def is_valid(url):
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        if not re.match(r"(.*\.ics\.uci\.edu|.*\.cs\.uci\.edu|.*\.informatics\.uci\.edu|.*\.stat\.uci\.edu)$", parsed.hostname.lower()):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print("TypeError for ", parsed)
        raise
