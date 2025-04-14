# 📝 Writeup - HALL OF FLAGS

## 🔍 Introduction

Ce challenge consistait à retrouver **la première équipe** ayant battu la Ligue Pokémon dans une sauvegarde de **Pokémon Émeraude** (`pokemon_save.sav`). La difficulté résidait dans l’accès aux données, nécessitant l’utilisation du bon outil pour explorer la sauvegarde.

Le flag suit le format **MCTF{flag}**.

---

## 🛠️ Étapes de résolution

### 1️⃣ Trouver le bon outil

En analysant le challenge, il était clair que les données du **Hall of Fame** devaient être extraites de la sauvegarde.

- Un éditeur de texte ou un éditeur hexadécimal comme **HxD** permettait d’examiner le fichier `.sav`, mais sans structuration claire des données.
    
- Des outils plus spécialisés dans l’édition de sauvegardes Pokémon étaient nécessaires.
    
- **PKHeX** s’est avéré être l’outil idéal, car il permet d’afficher directement les équipes enregistrées dans le **Hall of Fame**.
    

📌 **Téléchargement de PKHeX :** https://projectpokemon.org/home/files/file/1-pkhex/

---

### 2️⃣ Ouvrir la sauvegarde avec PKHeX

1. Lancer **PKHeX**.
    
2. Charger le fichier `pokemon_save.sav`.
    
3. Aller dans l’onglet **SAV**.
    
4. Aller dans l'onglet **Panthéon**
    
5. Repérer la **première équipe** enregistrée après la victoire contre la Ligue.
    

GGWP

Flag: `MCTF{WELL-d0NE-Y0U-F0UND-HALL-0FAME}`
