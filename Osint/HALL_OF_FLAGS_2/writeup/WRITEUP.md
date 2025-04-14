# 📝 Writeup - HALL OF FLAGS 2

## 🔍 Introduction

Ce challenge consistait à identifier **la nouvelle équipe** qui avait battu la Ligue Pokémon dans le fichier de sauvegarde fourni (`pokemon_save2.sav`). La difficulté résidait dans **l’identification de l’équipe** et **la récupération de sa date de création**.

Le flag suit le format **MCTF{YYYY-MM-DD}**.

---

## 🛠️ Étapes de résolution

### 1️⃣ Trouver le bon outil

Étant donné que le challenge impliquait l’analyse d’un **fichier de sauvegarde Pokémon**, la première étape consistait à trouver le bon outil pour extraire les données. Un éditeur hexadécimal pouvait révéler des données brutes, mais un éditeur spécialisé était nécessaire pour une lecture claire.

- **PKHeX** était l’outil idéal, car il permettait d’accéder directement aux archives du **Hall of Fame**.
    

📌 **Téléchargement de PKHeX :** [https://projectpokemon.org/home/files/file/1-pkhex/](https://projectpokemon.org/home/files/file/1-pkhex/)

---

### 2️⃣ Extraire l’équipe du Hall of Fame

1. Ouvrir **PKHeX**.
    
2. Charger `pokemon_save2.sav`.
    
3. Aller dans l’onglet **Hall of Fame**.
    
4. Identifier l’équipe ayant remporté la victoire la plus récente contre la Ligue Pokémon.
    

L’équipe extraite correspondait à **une team bien connue en 3G OU sur Coup Critique** :
🔗 [Voir l’équipe ici](https://www.coupcritique.fr/entity/teams/4891?from=%2Fentity%2Fusers%2F102)
Trouvable en faisant une simple recherche des noms des pokemons sur internet

---

### 3️⃣ Rechercher l’origine de l’équipe

Une fois l’équipe identifiée, la prochaine étape était de déterminer **sa date de création**.

- En recherchant cette équipe sur **Coup Critique**, il était possible de retrouver sa date d’origine.

FLAG : `MCTF{2023-03-03}`
