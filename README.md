# DorkSearcher

**DorkSearcher** est un outil de recherche avancée qui exploite la technique de "dorking" pour interroger en profondeur les moteurs de recherche tels que Google et Bing. Que vous soyez un journaliste d'investigation, un auditeur en sécurité, ou un analyste, cet outil vous permet de découvrir des informations sensibles cachées dans des pages web publiques, ainsi que des vulnérabilités exposées par des serveurs accessibles en ligne.

## Fonctionnalités

- **Recherche Avancée ("Dorking")** : Utilise la puissance des moteurs de recherche pour explorer des recoins invisibles des services web et découvrir des informations et vulnérabilités publiques.
- **Automatisation** : Facilite et accélère les recherches complexes grâce à des requêtes automatisées.
- **Multiprocessing** : Accélère la récupération des résultats en utilisant plusieurs processus simultanés.
- **Personnalisation des Paramètres** : Contrôlez le nombre de pages à récupérer et le nombre de processus pour maximiser l'efficacité de vos recherches.

## Installation

### Téléchargement du code

Clonez le dépôt GitHub :

```bash
git clone https://github.com/IbnWalid/DorkSearcher.git
cd DorkSearcher
```

### Prérequis

```bash
  pip install -r requirements.txt
```

### Utilisations

Lancez le script avec Python :

```bash
python dorksearcher.py
```

### Étapes d'utilisation

1. **Entrez votre requête** : Entrez la requête de recherche, comme une Google Dork, pour explorer des informations spécifiques.
2. **Sélectionnez le moteur de recherche** : Choisissez entre Google ou Bing pour exécuter votre recherche.
3. **Indiquez le nombre de pages** : Définissez combien de pages de résultats vous souhaitez récupérer.
4. **Ajustez le nombre de processus** : Choisissez le nombre de processus parallèles pour optimiser la rapidité de vos recherches (par défaut : 2).

### Remerciements

Merci d'avoir utilisé DorkSearcher ! Développé par IbnWalid.