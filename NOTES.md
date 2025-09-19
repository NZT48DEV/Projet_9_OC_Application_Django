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

## 🚧 En cours

- [ ] Ajouter les notifications manquantes
- [ ] Mise en place du système d’abonnements entre utilisateurs (suivre, se désabonner, liste abonnés/abonnements).
- [ ] Revoir la gestion des messages flash pour homogénéiser (success, error, warning, info)
- [ ] Améliorer le design des cartes (`review` / `ticket`) pour plus de cohérence
- [ ] Refactoring sur les templates (éviter la répétition de code)

## 🎯 Pour demain
- [ ] Améliorer le visuel du site
- [ ] Ajouter la pagination des posts


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
