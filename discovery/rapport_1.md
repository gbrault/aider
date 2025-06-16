# Rapport sur l'architecture et les fonctionnalités d'Aider

Ce document détaille l'architecture logicielle d'Aider, ses principaux cas d'utilisation et les commandes essentielles pour interagir avec l'outil.

## Architecture

L'architecture d'Aider est modulaire et conçue pour être flexible et extensible. Les composants clés sont :

1.  **L'Orchestrateur (`Coder`)** : Le cœur de l'application réside dans la classe `Coder` (`aider/coders/base_coder.py`). Elle gère le cycle de vie d'une conversation : préparation des prompts, envoi des requêtes au LLM, traitement des réponses, et application des modifications aux fichiers. C'est le chef d'orchestre qui coordonne tous les autres modules.

2.  **Système de "Coders"** : Aider utilise un système de "Coders" spécialisés pour gérer différents formats de modification de code. Chaque `Coder` (par ex. `EditBlockCoder`, `UnifiedDiffCoder`) est responsable de la manière dont les changements sont demandés au LLM et de la façon dont la réponse du LLM est parsée pour être appliquée au code. Cette abstraction permet de s'adapter facilement aux capacités de différents modèles. La sélection du `Coder` se fait via le paramètre `edit-format`.

3.  **Gestion du Contexte (`RepoMap`)** : Le module `aider/repomap.py` est l'une des fonctionnalités les plus avancées. Il construit une "carte" du dépôt de code pour fournir au LLM un contexte pertinent sans surcharger le prompt. Pour ce faire, il utilise :
    *   **Tree-sitter** pour parser le code source et en extraire les définitions et références de symboles (fonctions, classes, etc.).
    *   Un algorithme de **PageRank** (via `networkx`) pour classer les symboles et les fichiers les plus importants par rapport à la conversation en cours.
    Cela permet à Aider de raisonner sur des bases de code volumineuses de manière efficace.

4.  **Interface Utilisateur (`io.py`)** : Le module `aider/io.py` gère toutes les interactions avec l'utilisateur dans le terminal. Il s'appuie sur `prompt-toolkit` pour offrir une expérience riche avec auto-complétion, historique des commandes, coloration syntaxique et gestion des modes d'édition (normal/multi-lignes).

5.  **Gestion des Commandes (`commands.py`)** : Toutes les commandes utilisateur commençant par `/` sont gérées par le module `aider/commands.py`. Il fournit un système simple pour ajouter de nouvelles commandes et gérer leurs logiques spécifiques (par ex. `/add`, `/run`, `/commit`).

6.  **Abstraction des Modèles (`models.py`)** : Aider s'intègre avec de multiples fournisseurs de LLM grâce à la bibliothèque `litellm`. Le module `aider/models.py` abstrait les spécificités de chaque modèle (comptage de tokens, paramètres d'appel, etc.), ce qui rend le reste du code agnostique au modèle utilisé.

## Cas d'utilisation principaux

Aider est conçu pour assister les développeurs dans diverses tâches :

1.  **Édition de code** : Le cas d'usage le plus courant. L'utilisateur ajoute des fichiers au chat et demande à l'IA d'implémenter une nouvelle fonctionnalité, de corriger un bug ou de modifier le code existant.

2.  **Refactoring** : En ajoutant plusieurs fichiers au chat, l'utilisateur peut demander des opérations de refactoring complexes, comme renommer une fonction à travers tout le projet ou extraire une logique dans une nouvelle classe.

3.  **Débogage** : L'utilisateur peut coller une trace d'erreur ou le résultat d'un test échoué, et demander à Aider de trouver la cause du problème et de le corriger. Les commandes `/run` et `/test` sont particulièrement utiles pour ce scénario.

4.  **Compréhension de code** : En fournissant des fichiers en contexte, l'utilisateur peut poser des questions sur le fonctionnement d'une partie du code, et Aider utilisera sa connaissance des fichiers pour répondre.

5.  **Génération de commits** : Aider peut automatiquement générer et appliquer des commits Git pour les modifications qu'il effectue, avec des messages de commit pertinents basés sur la conversation.

## Commandes utiles

Voici une liste des commandes les plus courantes pour interagir avec Aider :

*   `/add <fichiers...>` : Ajoute un ou plusieurs fichiers au contexte du chat.
*   `/drop <fichiers...>` : Retire un ou plusieurs fichiers du chat.
*   `/ls` : Affiche la liste des fichiers actuellement dans le chat.
*   `/run <commande shell>` : Exécute une commande shell et injecte sa sortie dans la conversation.
*   `/test <commande test>` : Exécute une commande de test. Si elle échoue, la sortie est automatiquement fournie à l'IA pour correction.
*   `/commit` : Effectue un commit Git avec les modifications en attente.
*   `/diff` : Affiche les modifications non commitées sur les fichiers du chat.
*   `/undo` : Annule le dernier commit effectué par Aider.
*   `/clear` : Réinitialise l'historique de la conversation.
*   `/tokens` : Affiche le nombre de tokens utilisés par le contexte actuel.
*   `/model <nom_du_modèle>` : Permet de changer de modèle de langage à la volée.
*   `/web <url>` : Ajoute le contenu d'une page web au chat.
