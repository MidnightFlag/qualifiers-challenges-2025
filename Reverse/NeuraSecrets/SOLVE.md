# Etapes de solve

Ce chall étant une VM, il va donc falloir en reverse une bonne partie pour flag le challenge.
Le but de ce challenge est de trouver la clée qui déchiffre le fichier, en reversant le code on trouve une implémentation de MD5.
Lorsque le user envoie un input, un préfixe est concaténé à l'input de la façon suivante : `key_<user_input>`, il est ensuite hashé.

En poursuivant le reverse on peut dump le shellcode qui est envoyé à la VM par le serveur, il s'agit d'un tableau json qui code les prochaines instructions à executer, on peut donc trouver où se fait le check de la clé.

La clé hashée est envoyée par le serveur pour un check coté client, il faut donc recuperer ce hash et le casser avec hashcat (le mdp est dans rockyou)

Rentre la clé et le flag apparait.
