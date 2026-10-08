from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QTextEdit, QPushButton, QMessageBox, QCheckBox, QLineEdit
from maya import cmds
import json



class MessageBoard(QWidget):#definir la classe | QWidget = affiche dans lecran

    def __init__(self): #Constructeur

        super().__init__() #Initialisation | Constructeur a quelqu'un d'autre ====> De notre parent (QWidget)

        self.setWindowTitle("Outliner Organiser") #(Titre)----Parametre
        #self.rules = {} #variable pour stocker les regles json sous forme dictionnaire
        #self.target_objects = []  #Variable pour stocker les objets cibles
        self.create_ui()#fonction defeni a l'interieur d'une class | instance
    
    def create_ui(self):

        layout = QVBoxLayout(self)
        label = QLabel("Enter JSON rule path")
        layout.addWidget(label)

        self.message = QLineEdit()
        self.message.setPlaceholderText("Entrez message...")
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


    def json(self, chemin):
        print("json rule :", chemin)

        chemin = chemin.replace('\\', '/')


        #loading le json
        try:
            with open(chemin, 'r') as fichier:
                self.rules = json.load(fichier)
            print("Loading JSON from chemin:", chemin)

        except Exception as erreur:
            QMessageBox.warning(self, "Attention", "Le JSON file est introuvable")
            return

    
    #Quande je clique, je veux que sa active la bonne fonction---------------------------------------------------------------
    def on_click(self):
        print("C'est organisé")

        self.json(self.message.text())

        selection = None
        if self.checkbox1.isChecked():
            print("Selection")
            selection = cmds.ls(selection=True, long=True)

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
            cmds.undoInfo(closeChunk=True)
        #-------------------------------------------------------------------------------------------------------------------------

    def color(self):
        print("Color")

    #Pour selectionner-------------------------------------------------------------------------------------------------------------
    def reorder(self, selection):
        print("Reorder")

        if selection is None:
            selection = cmds.ls(transforms=True, long=True)
        #Prendre les cles dans les regles du fichier JSON (Dans la boite, pour prendre les informations)
        keys = list(self.rules.keys())

        #Pour commencer, on prend une collection et on retourne une nouvelle liste triee
        #Keys sert à determiner l'ordre des elements, calcule la valeur de chaque element et utilise la valeur pour triee
        #node.split ===> decoupe chaque information alors [-1] prend le dernier element (Dans python liste[-1] ===> est le dernier)
        #Cherche l'index du premier element de keys qui correspond au debut de la derniere partie de node

        sorted_selection = sorted(selection, key=lambda node: next((i for i, p in enumerate(keys) if node.split('|')[-1].startswith(p)), len(keys)))

        for obj in reversed(sorted_selection):
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

