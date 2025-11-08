# Exercice Flask - Port Scanner Web

## Étapes de développement

### Step 1 : Page d'accueil HTML ✅
**Objectif :** Afficher une page HTML de base

- Modifier la route `/` pour renvoyer une page HTML
- Afficher simplement "Hello World" en dur
- **Documentation :** https://flask.palletsprojects.com/en/stable/quickstart/#rendering-templates

---

### Step 2 : Création du formulaire ✅
**Objectif :** Construire l'interface utilisateur

Modifier la page HTML pour ajouter :
- Un titre "Port Scanner"
- Un formulaire contenant :
  - Un champ pour l'adresse IP
  - Un champ pour le port
  - Un bouton de soumission

**Notes importantes :**
- Aucune validation n'est requise à cette étape
- Le formulaire peut accepter des valeurs invalides (ex: "abc" dans le port)
- Le formulaire ne fait rien pour l'instant

---

### Step 3 : Route POST pour recevoir les données ✅
**Objectif :** Traiter les données du formulaire

- Créer une nouvelle route `/scan` de type POST
- Nommer la fonction associée `scan_form(...)`
- La fonction doit simplement afficher (print) les données reçues

**Rappel important :** Un formulaire HTML en POST attend un retour. Terminez la route par `return redirect("/")` pour éviter les erreurs.

---

### Step 4 : Connexion formulaire → route ✅
**Objectif :** Lier le frontend au backend

- Modifier le formulaire pour qu'il envoie les données à la route `/scan`
- Vérifier dans le terminal que les données sont bien affichées (printées)

---

### Step 5 : Intégration du scanner de ports ✅
**Objectif :** Utiliser la logique de scan existante

- Modifier la route `/scan` pour appeler la fonction de scan existante (celle qui ouvre le socket, etc.)

---

### Step 6 : Page de résultats
**Objectif :** Afficher les résultats du scan

- Faire en sorte que la route `/scan` redirige vers une nouvelle page `/result`
- Afficher dans cette page les données du scan :
  - Adresse IP
  - Port
  - Résultat (ex: "opensshd 22.3")

**Exemple :** Si je scanne un service SSH, je dois voir : `IP + port + résultat (opensshd 22.3)`

---

## Fonctionnalités optionnelles

### Validation frontend
- Ajouter une validation des données côté formulaire
- Empêcher l'utilisateur de saisir :
  - Une adresse IP invalide
  - Un port invalide

### Amélioration visuelle
- Ajouter du CSS pour améliorer l'interface

---

## Ressources et bonnes pratiques

- De nombreuses ressources en ligne existent pour Flask
- N'hésitez pas à les consulter, mais évitez le copier-coller aveugle
- Comprenez le code que vous utilisez

---

## Notes importantes

⚠️ **Attention :** Ne pas oublier de sauvegarder régulièrement votre travail ! 
