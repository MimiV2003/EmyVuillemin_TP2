from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QTextEdit, QPushButton, QMessageBox, QCheckBox, QLineEdit

class MessageBoard(QWidget):#definir la classe | QWidget = affiche dans lecran

    def __init__(self): #Constructeur

        super().__init__() #Initialisation | Constructeur a quelqu'un d'autre ====> De notre parent (QWidget)

        self.setWindowTitle("Outliner Organiser") #(Titre)----Parametre
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

        # C:\Users\evuillemin\Repos\EmyVuillemin_TP2\rules.json
    
    #Quande je clique, je veux que sa active la bonne fonction---------------------------------------------------------------
    def on_click(self):
        print("C'est organisé")

        self.json(self.message.text())

        if self.checkbox1.isChecked():
            self.selection()

        if self.checkbox2.isChecked():
            self.color()

        if self.checkbox3.isChecked():
            self.reorder()

    def selection(self):
        print("Selection")

    def color(self):
        print("Color")

    def reorder(self):
        print("Reorder")

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

