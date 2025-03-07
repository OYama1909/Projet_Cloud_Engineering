# Projet Cloud Engineering

## Qui nous sommes

Nous sommes étudiants en B2 à l'IA Insitut by EPITA & ISG.

## De quoi il s'agit

Le projet consiste à simuler la génération de tickets de caisse. Il y aurait *n* magasins et pour chaque magasin, *k* vendeurs pour *i* caisses, avec un stock différent pour chaque magasin. On aurait le générateur de tickets de caisse. Dans un ticket de caisse, il y a le numéro du magasin, le numéro de la caisse, le numéro du vendeur, les produits, la quantité, le prix pour chaque produit et le prix final. 

Les tickets de caisse vont dans les serveurs (le générateur de tickets est relié au serveur). Grâce à Kafka, les tickets vont dans les *savers*, qui vont enregistrer un nombre de tickets par seconde dans le cloud MongoDB. En même temps que les tickets sont envoyés dans le serveur par *Kafka*, une notification de l'enregistrement des tickets est envoyée au serveur de gestion. Les caisses reliées au serveur devraient envoyer une notification s'il reste moins de 10 % en stock. 

Nous avions une période d'un mois pour réaliser ce projet.

## Composition du GitHub

Le GitHub comporte les dossiers suivants :
- *kafka* : comme son nom l'indique, ce dossier comporte des éléments relatifs à l'intégration de kafka à notre projet. En particulier, il contient les dossiers *consumer* (pour la simulation d'un lecteur de tickets de caisse) et *producer* (pour la simulation d'un générateur de tickets de caisse).

- *store* : ce dossier est censé permettre la génération d'une API REST simulant la course d'un consommateur, qui a un panier auquel il peut ajouter (ou enlever) des produits, et qu'il peut valider, générant ainsi un ticket de caisse.

## Lancement du code
Notre projet fonctionne avec Docker et il convient d'utiliser la commande suivante pour l'exécuter : docker-compose up --remove-orphans

## Difficultés rencontrées / Points à améliorer
Cependant, nous avons malheureusement rencontré des difficultés pour l'intégration de *kafka* à notre projet. En effet, le code Python ne parvenait pas à importer ce module, nous empêchant de faire fonctionner pleinement notre projet et donc d'entièrement le tester...
Par manque de temps, nous n'avons pas réalisé certaines choses qui sont décrites dans la partie "De quoi il s'agit" (par exemple, l'envoi de notification s'il reste moins de 10 % en stock).
