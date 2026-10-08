# EmyVuillemin_TP2
TP2

Développer un outil Python avec PySide6 permettant d'organiser les éléments de l'Outliner de Maya. L'outil devra lire un fichier de configuration au format JSON afin d'appliquer automatiquement des couleurs et de réorganiser les éléments selon des règles définies. L'objectif est de mettre en pratique les notions fondamentales de programmation Python dans un contexte inspiré des outils utilisés en production de jeux vidéo et d'effets visuels.
Consignes
●
Développer un outil Python qui permet d'appliquer une couleur à certains éléments de l'Outliner en fonction de leur nom. Les codes de couleur doivent être définis dans un fichier JSON. L’application des couleurs doit se faire conditionnellement à une case à cocher présente dans l’interface.
●
Permettre de réorganiser en ordre croissant de nom les éléments de l'outliner. Seuls les éléments listés dans le fichier de configuration doivent être réorganisés. La réorganisation doit se faire conditionnellement à une case à cocher présente dans l’interface.
●
Permettre d'appliquer les opérations soit sur la sélection active, soit sur tous les objets de la scène, selon l'état d'une case à cocher.
●
Supporter CTRL+Z pour revenir en arrière
●
Utiliser Github pour versionner et stocker le projet.


C:\Users\evuillemin\Repos\EmyVuillemin_TP2\rules.json

 #Pour le long code----------Pour chaque node, prends ce qui se trouve apres le dernier. Cherche dans keys quel prefixe correspond au debut de cette partie
 Utilise la position de ce prefixe dans keys comme valeur de tri. Si aucun prefixe ne correspond, mets le node a la fin. Ensuite, parcours toute la liste triee a l'envers.