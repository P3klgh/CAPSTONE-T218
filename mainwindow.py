import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMenuBar, QFileDialog, QMessageBox
from PyQt6.QtGui import QAction  
import qtawesome as qta
from pages.welcome_page import WelcomePage
from styles_loader import load_stylesheets

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Train Simulator')
        self.setGeometry(300, 300, 800, 600)

        self.welcome_page = WelcomePage(self)
        self.setCentralWidget(self.welcome_page)

        self.create_menu_bar()
        self.apply_stylesheet()

    def create_menu_bar(self):
       
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu('File')
        
        new_project_action = QAction(qta.icon('fa.file', color='white'), 'Create a new project', self)
        new_project_action.triggered.connect(self.new_project)
        file_menu.addAction(new_project_action)
        
        open_project_action = QAction(qta.icon('fa.folder-open', color='white'), 'Open an existing project', self)
        open_project_action.triggered.connect(self.open_project)
        file_menu.addAction(open_project_action)
      
       # Separator
        menuSeparator = menu_bar.addMenu('|')
        menuSeparator.setObjectName('separator')
        menuSeparator.setEnabled(False)
      
        save_action = QAction(qta.icon('fa.save', color='white'), 'Save', self)
        save_action.triggered.connect(self.save_project)
        file_menu.addAction(save_action)

        save_as_action = QAction(qta.icon('fa.upload', color='white'), 'Save as', self)
        save_as_action.triggered.connect(self.save_as_project)
        file_menu.addAction(save_as_action)

        exit_action = QAction(qta.icon('fa.times', color='white'), 'Exit', self)
        exit_action.triggered.connect(self.close)  
        file_menu.addAction(exit_action)

        tools_menu = menu_bar.addMenu('Tools')

        settings_action = QAction(qta.icon('fa.cog', color='white'), 'Settings', self)
        settings_action.triggered.connect(self.open_settings)
        tools_menu.addAction(settings_action)

        # Separator
        menuSeparator = menu_bar.addMenu('|')
        menuSeparator.setObjectName('separator')
        menuSeparator.setEnabled(False)
    
        help_menu = menu_bar.addMenu('Help')

        about_action = QAction(qta.icon('fa.info-circle', color='white'), 'About Simul', self)
        about_action.triggered.connect(self.about_simul)
        help_menu.addAction(about_action)

        user_manual_action = QAction(qta.icon('fa.book', color='white'), 'Open User Manual', self)
        user_manual_action.triggered.connect(self.open_user_manual)
        help_menu.addAction(user_manual_action)
   
    def apply_stylesheet(self):
        stylesheet = load_stylesheets()  
        self.setStyleSheet(stylesheet)

    def new_project(self):
        self.welcome_page = WelcomePage(self)
        self.setCentralWidget(self.welcome_page)

    def open_project(self):
        file_name, _ = QFileDialog.getOpenFileName(self, 'Open Project', '', 'Project Files (*.json *.xml);;All Files (*)')
        if file_name:
            print(f"Opening Project: {file_name}")
            # add logic to open the project file.

    def save_project(self):
        print("save clicked")
        # will add the logic 

    def save_as_project(self):
        file_name, _ = QFileDialog.getSaveFileName(self, 'Save Project As', '', 'Project Files (*.json *.xml);;All Files (*)')
        if file_name:
            print(f"Saving Project As: {file_name}")
            # add the logic of saving the project file depends on project name simulation file....

    def open_settings(self):
        # add logic to go to setting page
        print("Settings clicked")
        
    def about_simul(self):
         # add logic to go to simul intro page
        print("about_simul clicked")

    def open_user_manual(self):
         # add logic to go to user_manual page
        print("user_manual clicked")

    def update_window_title(self, name):
        self.setWindowTitle(name)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    welcome_page = WelcomePage(window)
    window.show()
    sys.exit(app.exec())

    