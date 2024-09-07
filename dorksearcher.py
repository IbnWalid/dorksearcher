#############################
#   Code of DorkSearcher    #
#   Main dev : IbnWalid     #
#############################
import os
import requests
from functools import partial
from multiprocessing import Pool
from bs4 import BeautifulSoup as bsoup

GREEN, RED = '\033[1;32m', '\033[91m'

# 🚪 <-- J'ai caché la backdoor ici ahhaha ?

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


def search_result(q, engine, pages, processes, resultat):
    print('═' * 70)
    print(f'Recherche pour: {q} sur {pages} page(s) de {engine} avec {processes} processes')
    print('═' * 70)
    print()
    counter = 0
    for range in resultat:
        for r in range:
            print('[+] ' + r)
            counter += 1
    print()
    print('═' * 70)
    print(f"Nombre d'url trouvées : {counter}")
    print('═' * 70)

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

    processes = int(input('[?] Choisissez le nombre de processes : '))
    if processes == "":
        processes = 2
    

    with Pool(int(processes)) as p:
        resultat = p.map(target, range(int(pages)))

    search_result(requetes, engine, pages, processes, resultat)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nMerci d'avoir utiliser mon tool !")
        exit()
    except TimeoutError:
        print(RED + '\n[-] Trop de rêquetes, réessayer ultérieurement....')
        exit()