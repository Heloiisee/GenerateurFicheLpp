# GenerateurFicheLpp

Ce projet est une application web développée avec **Flask** permettant de créer des fiches d'exercices dynamiques avec sections personnalisées, images, tableaux, et consignes, et de les exporter en **PDF** avec ou sans **barème d’évaluation**.

---

## 🚀 Fonctionnalités

- 🧩 Création multi-sections avec titre, consignes, questions, tableaux CSV
- 🔐 Connexion sécurisée avec authentification unique (1 utilisatrice autorisée)
- 📊 Insertion de tableaux via import CSV brut
- 🧑‍🏫 Option d'évaluation avec critères et barème personnalisable
- 📄 Export **PDF** (avec WeasyPrint) et aperçu HTML en un clic
- 🖌️ Plusieurs modèles visuels (classique, moderne, évaluation)
- 👁️ Aperçu HTML avant génération
- ♻️ Suppression automatique des fichiers temporaires (images, PDF)
- 🌱 Écoconception : poids optimisé, ressources minimales, usage mémoire leger

---

## 🧰 Technologies utilisées

- **Python 3.11**
- **Flask** – pour l’application web
- **WeasyPrint** – pour la génération de PDF
- **Dotenv** – pour gérer les variables sensibles
- **HTML/CSS minimalistes** – pour l’interface

---
## 📦 Installation

### 1. Cloner le dépôt

```bash
git https://github.com/Heloiisee/GenerateurFicheLpp.git
cd GenerateurFicheLpp

python -m venv .venv
source .venv/bin/activate  # Sur Windows : .venv\Scripts\activate

pip install -r requirements.txt

```

Si requirements.txt n'existe pas, crée-le avec :

```bash
Flask
WeasyPrint

```

# 👨‍💻 Auteur
Projet développé par Heloiisee
