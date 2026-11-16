#TP2 Emy Vuillemin----------------------------------------------------------------------------------------------------


from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QTextEdit, QPushButton, QMessageBox, QCheckBox, QLineEdit
from maya import cmds
import json


#-------------------------------------------------------------------------------------------------------------------------------
class MessageBoard(QWidget):#definir la classe | QWidget = affiche dans lecran

    def __init__(self): #Constructeur

        super().__init__() #Initialisation | Constructeur a quelqu'un d'autre ====> De notre parent (QWidget)

        self.setWindowTitle("Outliner Organiser") #(Titre)----Parametre
        self.create_ui()#fonction defeni a l'interieur d'une class | instance

    #------------------------------------------------------------------------------------------------------------------------
    #Le resultat de la fenetre avec les case à cocher et barre de recherche
    def create_ui(self):

        layout = QVBoxLayout(self)
        label = QLabel("Enter JSON rule path")
        layout.addWidget(label)

        self.message = QLineEdit()
        self.message.setPlaceholderText("Entrer JSON...")
        layout.addWidget(self.message)

        
        #Apparaitre les boite a cocher------------------------------------------------------------------------------------------
        self.checkbox1 = QCheckBox("Apply on selection only")
        self.checkbox2 = QCheckBox("Apply colors")
        self.checkbox3 = QCheckBox("Apply reorder")
        layout.addWidget(self.checkbox1)
        layout.addWidget(self.checkbox2)
        layout.addWidget(self.checkbox3)
        #Creation du bouton------------------------------------------------------------------------------------------------------

        button = QPushButton("Organise Outliner")
        layout.addWidget(button)
        button.clicked.connect(self.on_click)
        #----------------------------------------------------------------------------------------------------------------------

        print("create UI")

    #Verificaton que le json file est bien stocker dans les donnees dans self.rules--------------------------------------------
    def json(self, chemin):
        print("json rule :", chemin)

        chemin = chemin.replace('\\', '/') #Remplace caractere par /


        #loading le json
        try:
            with open(chemin, 'r') as fichier:
                self.rules = json.load(fichier) #stocker les donnees dans self.rules
            print("Loading JSON from chemin:", chemin)

        except Exception as erreur:
            QMessageBox.warning(self, "Attention", "Le JSON file est introuvable")#Montre un avertissement si le json file est introuvable
            return

    
    #Quande je clique, je veux que sa active la bonne fonction---------------------------------------------------------------
    #Analyse une deuxime fois
    def on_click(self):
        print("C'est organisé")

        self.json(self.message.text())#Charge le fichier JSON

        selection = None
        if self.checkbox1.isChecked(): # Verifier si la case est cocher
            print("Selection")
            selection = cmds.ls(selection=True, long=True) #Recuperer la selection maya et verifier si au moins un objet est selectioner
            #Sinon si rien de selectenionner = warning
            if not selection:
                QMessageBox.warning(self, "Attention", "Rien n'est sélectionné")
                return

        # Faire le control + z pour reculer en arriere-------------------------------------------------------------------------
        cmds.undoInfo(openChunk=True)
        try:
            if self.checkbox2.isChecked():
              self.color(selection)

            if self.checkbox3.isChecked():
                self.reorder(selection)
        finally:
            cmds.undoInfo(closeChunk=True)#Un seule etape dans la pile d'annulation
        #-------------------------------------------------------------------------------------------------------------------------

    #Couleur----------------------------------------------------------------------------------------------------------------------------------------------
    #sa marche mais sa charge vraiment longtemps quand tout est selectionner, sa peut crash le maya
    #Ce que j'ai compris, c'est pas mon python le probleme mais le maya avec le playblast qui fait crash avec la couleur
    #De plus, il faut mettre le curseur (La souris) sur la ranger pour apparaitre la couleur seulement quand on prends tout la selection
    #------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def color(self, selection=None):

        
        print("Color")


        if selection is None: #Objets a traiter
            selection = cmds.ls(selection=True, long=True)

            if not selection:
                selection = cmds.ls(type="transform", long=True) or [] #la selection de type transforme
        #Attribuer automatiquement une couleur a chaque objet selectionner
        for obj in selection:

            name = obj.split("|")[-1] # Extraire le nom de chaque objet

            for prefix, rgb in self.rules.items(): #parcours toute les regles charger de self.rules

                if name.startswith(prefix): #Verifie si le nom de l'objet commence par le prefixe actuel
                    try:
                        if cmds.attributeQuery("useOutlinerColor", node=obj, exists=True): # nom de l'attribut| verificaton objet| si sa existe
                            cmds.setAttr(obj + ".outlinerColor", rgb[0], rgb[1], rgb[2], type="double3") #RGB c'est les couleurs | setAttr = definir valeur attribut | double3 = fournie 3 nbr de type double
                            #regrouper dans attribut vectoriel ===> c'est un attribut de 3 composants (RGB)
                            cmds.setAttr(obj + ".useOutlinerColor", True)#Active
                            print(f" - Color applied: {obj} -> {prefix}: {rgb}")#Affiche message dans console, le f ===> String
                    except Exception as e:
                            print(f"Erreur sur {obj}: {e}")
                    break

    #Renitialiser les couleurs personnaliser-------------------------------------------------------------------------------------------------------------------------------------------------------------------
    def clear_colors(self):

        selection = cmds.ls(selection=True, long=True) or cmds.ls(type="transform", long=True) or [] # Recuperer les objets transforme | [] ===> utiliser une liste vide
        for obj in selection:
            try:
                if cmds.attributeQuery("useOutlinerColor", node=obj, exists=True): #Existe = execute
                    cmds.setAttr(obj + ".useOutlinerColor", False) # Desactiver la couleur
            except:
                pass
            print("Couleurs Outliner rénitialisées")
            #Desacti

    #Pour Reorganiser l'ordre des objets dans maya-------------------------------------------------------------------------------------------------------------
    def reorder(self, selection):
        print("Reorder")

        if selection is None:
            selection = cmds.ls(transforms=True, long=True) #Verifie si aucune selection n'a ete fournie
        #Prendre les cles dans les regles du fichier JSON (Dans la boite, pour prendre les informations)
        keys = list(self.rules.keys())

        #Celui la est le plus longue ligne de code
        #Attribue chaque objet selon le prefixe et creation de la liste triée
        #keys=determine ordre
        #node split=decoupe information + prend le dernier ([-1])
        #cherche index du premier element

        #Trie objet en fonction de leur nom et des prefixes defenis dans les keys | Liste ===> traite objet===>recupere derniere element ('|'[-1])===>verifie le nom===>associe===>recupere===>valeur
        sorted_selection = sorted(selection, key=lambda node: next((i for i, p in enumerate(keys) if node.split('|')[-1].startswith(p)), len(keys)))

        for obj in reversed(sorted_selection): #Appliquer le nouvel ordre /Reorganise et affiche resultat ===> parcours la liste a l'envers
            cmds.reorder(obj, front=True)
            print(f" - Reordered: {obj}")

    #--------------------------------------------------------------------------------------------------------------------------

def main():

    global widget 

    try:

        widget.close()

    except Exception:

        pass

    widget = MessageBoard()

    widget.show()

 

main()
# correction
