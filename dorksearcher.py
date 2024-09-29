import os
import requests
import urllib.parse
import logging
from functools import partial
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup as bsoup

# Constants for colored output
GREEN, RED = '\033[1;32m', '\033[91m'

# Constants for search engines
GOOGLE = 'google'
BING = 'bing'

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def search_engine_request(base_url, headers, params):
    """Perform a search engine request and return parsed links."""
    try:
        resp = requests.get(base_url, params=params, headers=headers)
        resp.raise_for_status()
        soup = bsoup(resp.text, 'html.parser')
        return soup
    except requests.RequestException as e:
        logging.error(f"Request failed: {e}")
        return None

def google_search(requetes, page):
    """Perform a Google search and return a list of result URLs."""
    base_url = 'https://www.google.com/search'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0'}
    params = {'q': requetes, 'start': page * 10}
    soup = search_engine_request(base_url, headers, params)
    if soup:
        return [link.find('a').get('href') for link in soup.findAll("div", {"class": "yuRUbf"})]
    return []

def bing_search(requetes, page):
    """Perform a Bing search and return a list of result URLs."""
    base_url = 'https://www.bing.com/search'
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0'}
    params = {'q': requetes, 'first': page * 10 + 1}
    soup = search_engine_request(base_url, headers, params)
    if soup:
        return [link.text for link in soup.findAll('cite')]
    return []

def search_result(q, engine, pages, resultat):
    """Display search results and check for SQL vulnerabilities."""
    logging.info(f"Recherche pour: {q} sur {pages} page(s) de {engine}")
    
    max_len_url = max(len(r) for range in resultat for r in range)
    counter = 0
    for range in resultat:
        for r in range:
            result_text = RED + "[!] Vulnérabilités SQL détecté [!]" if sql_checker(r) else RED + "[!] Aucune vulnérabilité SQL détecté [!]"
            logging.info(f"[+] {r.ljust(max_len_url)} | {result_text}")
            counter += 1

    logging.info(f"Nombre d'url trouvées : {counter}")

def sql_checker(url):
    """Check if a URL is vulnerable to SQL injection."""
    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed_url.query)

    if not query_params:
        logging.warning("Aucun paramètre trouvé dans l'URL.")
        return False
    
    for param in query_params:
        query_params[param] = [value + "'" for value in query_params[param]]
    
    new_query = urllib.parse.urlencode(query_params, doseq=True)
    new_url = urllib.parse.urlunparse((
        parsed_url.scheme,
        parsed_url.netloc,
        parsed_url.path,
        parsed_url.params,
        new_query,
        parsed_url.fragment
    ))

    try:
        response = requests.get(new_url)
        response.raise_for_status()
        sql_errors = ["you have an error in your sql syntax", 
                      "mysql_fetch_array()", 
                      "unclosed quotation mark", 
                      "quoted string not properly terminated", 
                      "near syntax error"]
        return any(error.lower() in response.text.lower() for error in sql_errors)
    except requests.RequestException as e:
        logging.error(f"Erreur lors de la requête vers {new_url}: {e}")
    return False

def get_user_input(prompt, valid_options=None):
    """Get validated user input."""
    while True:
        user_input = input(prompt).strip().lower()
        if valid_options and user_input not in valid_options:
            logging.warning("Entrée invalide. Veuillez réessayer.")
        else:
            return user_input

def main():
    """Main function to execute the search and vulnerability check."""
    clear()
    h4xor_banner = ''' 

 ▓█████▄  ▒█████   ██▀███   ██ ▄█▀      ██████  ▓█████ ▄▄▄      ██▀███    ▄████▄   ██░ ██  ▓█████ ██▀███  
 ▒██▀ ██▌▒██▒  ██▒▓██ ▒ ██▒ ██▄█▒     ▒██    ▒  ▓█   ▀▒████▄   ▓██ ▒ ██▒ ▒██▀ ▀█ ▒▓██░ ██  ▓█   ▀▓██ ▒ ██▒
 ░██   █▌▒██░  ██▒▓██ ░▄█ ▒▓███▄░     ░ ▓██▄    ▒███  ▒██  ▀█▄ ▓██ ░▄█ ▒ ▒▓█    ▄░▒██▀▀██  ▒███  ▓██ ░▄█ ▒
▒░▓█▄   ▌▒██   ██░▒██▀▀█▄  ▓██ █▄       ▒   ██▒ ▒▓█  ▄░██▄▄▄▄██▒██▀▀█▄  ▒▒▓▓▄ ▄██ ░▓█ ░██  ▒▓█  ▄▒██▀▀█▄  
░░▒████▓ ░ ████▓▒░░██▓ ▒██▒▒██▒ █▄    ▒██████▒▒▒░▒████▒▓█   ▓██░██▓ ▒██▒░▒ ▓███▀  ░▓█▒░██▓▒░▒████░██▓ ▒██▒
░ ▒▒▓  ▒ ░ ▒░▒░▒░ ░ ▒▓ ░▒▓░▒ ▒▒ ▓▒    ▒ ▒▓▒ ▒ ░░░░ ▒░ ░▒▒   ▓▒█░ ▒▓ ░▒▓░░░ ░▒ ▒    ▒ ░░▒░▒░░░ ▒░ ░ ▒▓ ░▒▓░
  ░ ▒  ▒   ░ ▒ ▒░   ░▒ ░ ▒ ░ ░▒ ▒░    ░ ░▒  ░ ░░ ░ ░  ░ ░   ▒▒   ░▒ ░ ▒    ░  ▒    ▒ ░▒░ ░░ ░ ░    ░▒ ░ ▒ 
  ░ ░  ░ ░ ░ ░ ▒    ░░   ░ ░ ░░ ░     ░  ░  ░      ░    ░   ▒    ░░   ░  ░         ░  ░░ ░    ░    ░░   ░ 
    ░        ░ ░     ░     ░  ░             ░  ░   ░        ░     ░      ░ ░       ░  ░  ░░   ░     ░     
                                                                                                          
    Made By: IbnWalid'211 

'''
    
    print(GREEN + h4xor_banner)

    requetes = input('[?] Entrez votre rêquete : ')
    engine = get_user_input('[?] Choisissez le moteur de recherche (Google/Bing): ', valid_options=[GOOGLE, BING])

    target = partial(google_search, requetes) if engine == GOOGLE else partial(bing_search, requetes)
    
    pages = input('[?] Choisissez le nombre de pages : ')
    pages = int(pages) if pages.isdigit() else 1

    try:
        with ThreadPoolExecutor(max_workers=4) as executor:
            resultat = list(executor.map(target, range(pages)))

        search_result(requetes, engine, pages, resultat)

    except KeyboardInterrupt:
        logging.error("Interruption détectée. Fermeture du programme...")

if __name__ == '__main__':
    while True:
        try:
            main()
        except KeyboardInterrupt:
            logging.info("Merci d'avoir utilisé mon outil !")
            break
        except TimeoutError:
            logging.warning('Trop de requêtes, réessayez ultérieurement....')

        # Ask the user if they want to perform another search or exit
        choix = get_user_input("\n[?] Voulez-vous refaire une requête ? (o/n): ", valid_options=['o', 'n'])
        if choix != 'o':
            logging.info("Fermeture du programme. À bientôt !")
            break

