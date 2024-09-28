import os
import requests
import urllib.parse
from functools import partial
from multiprocessing import Pool
from bs4 import BeautifulSoup as bsoup

GREEN, RED = '\033[1;32m', '\033[91m'

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def google_search(requetes, page):
    base_url = 'https://www.google.com/search'
    headers  = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0' }
    params   = { 'q': requetes, 'start': page * 10 }
    resp = requests.get(base_url, params=params, headers=headers)
    soup = bsoup(resp.text, 'html.parser')
    links = soup.findAll("div", { "class" : "yuRUbf" })
    resultat = []
    for link in links:
        resultat.append(link.find('a').get('href'))
    return resultat

def bing_search(requetes, page):
    base_url = 'https://www.bing.com/search'
    headers  = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0' }
    params   = { 'q': requetes, 'first': page * 10 + 1 }
    resp = requests.get(base_url, params=params, headers=headers)
    soup = bsoup(resp.text, 'html.parser')
    links  = soup.findAll('cite')
    resultat = []
    for link in links:
        resultat.append(link.text)
    return resultat

def search_result(q, engine, pages, resultat):
    print('═' * 80)
    print(f'Recherche pour: {q} sur {pages} page(s) de {engine}')
    print('═' * 80)
    print()
    
    max_len_url = max(len(r) for range in resultat for r in range)
    
    counter = 0
    for range in resultat:
        for r in range:
            if sql_checker(r) == True:
                result_text = RED + "[!] Vulnérabilités SQL détecté [!]"
            else:
                result_text = RED + "[!] Aucune vulnérabilité SQL détecté [!]"
            
            # Affichage aligné avec l'URL ajustée à la longueur maximale
            print(GREEN + '[+] ' + r.ljust(max_len_url) + ' | ' + result_text)
            counter += 1

    print()
    print(GREEN + '═' * 80)
    print(f"Nombre d'url trouvées : {counter}")
    print('═' * 80)

def sql_checker(url):
    parsed_url = urllib.parse.urlparse(url)
    query_params = urllib.parse.parse_qs(parsed_url.query)

    if not query_params:
        print("Aucun paramètre trouvé dans l'URL.")
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
        sql_errors = ["you have an error in your sql syntax", 
                      "mysql_fetch_array()", 
                      "unclosed quotation mark", 
                      "quoted string not properly terminated", 
                      "near syntax error"]
        for error in sql_errors:
            if error.lower() in response.text.lower():
                return True
    except requests.RequestException:
        print(f"Erreur lors de la requête vers {new_url}")
    return False

def main():
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
    engine = input('[?] Choisissez le moteur de recherche (Google/Bing): ')

    if engine.lower() == 'google':
        target = partial(google_search, requetes)
    elif engine.lower() == 'bing':
        target = partial(bing_search, requetes)
    else:
        print("[-] Entrer invalide ... t'as rien pigé ....")
        exit()
    
    pages = int(input('[?] Choisissez le nombre de pages : '))
    if pages == "":
        pages = 1

    try:
        with Pool(4) as p:
            resultat = p.map(target, range(int(pages)))

        search_result(requetes, engine, pages, resultat)

    except KeyboardInterrupt:
        print(RED + "\n[!] Interruption détectée. Fermeture du programme...")
    finally:
        if 'p' in locals():
            p.terminate() 
            p.join()

if __name__ == '__main__':
   while True:
        try:
            main()
        except KeyboardInterrupt:
            print("\nMerci d'avoir utilisé mon outil !")
            break
        except TimeoutError:
            print(GREEN + '\n[-] Trop de requêtes, réessayez ultérieurement....')

        # Demander à l'utilisateur s'il souhaite refaire une recherche ou quitter
        choix = input(GREEN + "\n[?] Voulez-vous refaire une requête ? (o/n): ").lower()
        if choix != 'o':
            print(GREEN +"\n[!] Fermeture du programme. À bientôt !")
            break