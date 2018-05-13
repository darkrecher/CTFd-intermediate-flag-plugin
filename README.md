# CTFd-intermediate-flag-plugin

Plugin for the Capture The Flag platform CTFd : challenge type with intermediate flags.

Created from this plugin :

https://github.com/tamuctf/CTFd-multi-question-plugin


## TODO list

 - X un seul champ dans le modal
 - X les commentaires que j'avais mis dans `__init__.py`
 - X la création permet de définir les infos des clés
 - X le choix static/regex n'est pas pris en compte, j'ai dû bugger.
 - X les award négatifs ne sont pas acceptés. Là c'est un bug.
 - X l'update permet de redéfinir les infos des clés. (Pas d'en ajouter ou d'en supprimer, car ça mettrait le bazar dans les flags en cours).
 - donner des awards à chaque flag interm. Si possible les virer à la fin pour que ça donne le score final.
 - affichage des flags déjà obtenu
 - message adapté quand on essaye de remettre un flag déjà trouvé
 - solve qui ne tient pas compte des flags négatifs
 - accès au fichier/à la page secrète quand on a le flag correspondant
 - si possible, affichage direct du flag interm obtenu
 - si possible, enabler/disabler la visibilité des flags obtenus par les autres équipes.
 - affichage des flags de toutes les équipes. Du coup, il faut changer la structure de la table "partial". Un enregistrement par (team, chal, flag_interm), avec horodatage.
 - Des tooltips un peu plus clairs.
 - Les TODO dans le code
 - doc là où on peut. Expliquer que le bouton "new flag" dans la fenêtre standard "edit flags" risque de mettre le bazar. Expliquer aussi pourquoi y'a pas de add/remove dans les flags interm.




