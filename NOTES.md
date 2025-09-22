# ✅ Progression - Projet Django (LITRevu)

## 🔧 Déjà fait
- [x] Création du projet Django `LITRevu`
- [x] Mise en place des apps : `authentication`, `tickets`, `reviews`, `userfollows`, `posts`
- [x] Système d’authentification avec utilisateur custom (`authentication.User`)
- [x] Création des modèles : `Ticket`, `Review`, etc.
- [x] Templates de base avec héritage (`base.html`)
- [x] Gestion des posts utilisateur (tickets + reviews)
- [x] Ajout des notifications (Bootstrap Toasts)
- [x] Confirmation et aperçu avant suppression d’une **review**
- [x] Confirmation et aperçu avant suppression d’un **ticket**
- [x] Notification lors de la suppression d’une review/ticket
- [x] Fusion de l’affichage `Review` et `Ticket` dans **Vos posts** (tri par date)
- [x] Uniformisation du format de date (12:02, 17 Septembre 2025)
- [x] Création d’un **custom filter Django** (`format_date`) pour afficher la date avec mois en toutes lettres
- [x] Corriger le chargement du custom filter (`{% load custom_filters %}`)
- [x] Vérifier que le dossier `templatetags` contient bien un `__init__.py` vide
- [x] Tester le `format_date` dans `user_posts.html` et les partials
- [x] Vérifier que toutes les notifications s’affichent bien en haut à droite
- [x] Créer une app `core` pour centraliser :  
  - les filtres custom  
  - les tags custom  
  - les JS communs (notifications, toasts, etc.)
- [x] Déplacer `custom_filters.py` dans `core/templatetags/`
- [x] Mettre en place l'autocomplétion des utilisateurs dans la page des abonnements
- [x] Ajout des |linebreaksbr (saut de ligne)
- [x] Ajouter les notifications manquantes
- [x] Correction de l'ordre d'affichage dans le flux 
- [x] Ajout de next pour rediriger vers la page précédente lors d'une suppression ou d'une modification d'un ticket ou d'une critique
- [x] Ajout de la possibilité de modifier/supprimer son ticket dans le flux [Fait grâce a read_only (True/False)]
- [x] Mise en place du système d’abonnements entre utilisateurs (suivre, se désabonner, liste abonnés/abonnements).
- [x] Modifier la gestion des critiques (si une critique est déjà présente, impossibilité d'en ajouter une nouvelle (+ notif))
- [x] Avoir la possibilité de bloquer un utilisateur (éviter qu'il puisse nous suivre, nous contacter, etc.)
- [x] Voir les tickets uniquement des personnes qu'on suit. 
- [x] Ajout d'un filtre pour avoir la possibilité de voir soit les tickets des abonnés (Mes abonnements), soit de tout le monde (Tous les posts).
- [x] Enregistrer le choix du filtre pour la session.
- [x] Voir les critiques associés aux personnes des tickets qu'on suit, même si la critique est posté par un autre utilisateur.
- [x] Ne pas pouvoir accéder a un ticket ou une review d'une personne qui ma bloqué.

## 🚧 En cours
- [ ] Améliorer le visuel du site
- [ ] Améliorer le design des cartes (`review` / `ticket`) pour plus de cohérence
- [ ] Refactoring sur les templates (éviter la répétition de code)

## 🎯 Pour demain
- [ ] Ajouter la pagination des posts
- [ ] Enlever le lien Admin


## 🚀 Pour plus tard
- [ ] Adapter le site pour respecter les WCAG
- [ ] Embellir le code avec `Flake8` ou `Black`
- [ ] Vérifier qu'aucune donnée sensible n'est exposée publiquement (secret, clé privée, informations de connexion, etc.)
- [ ] Vérifier que le code est bien documenté et qu'il respecte la PEP8 (commentaires, docstrings, etc.)
- [ ] Vérifier `requirements.txt`, `README.md`, etc.
- [ ] Rédiger un petit plan de soutenance (15 min présentation + 10 min questions)


## 💡 Pourrait avoir (si temps dispo)
- [ ] Sessions Django classiques (cookies de session)
- [ ] Créer la gestion du profil utilisateur (affichage des infos, modification, etc.)
- [ ] Afficher l’indication d’édition sur une critique ou un post et mettre à jour l’heure de dernière modification.
- [ ] Ajouter un Dark Mode


