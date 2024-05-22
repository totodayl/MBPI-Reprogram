import psycopg2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal

from PyQt5.QtWidgets import *






class ClickableLabel(QtWidgets.QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, event):
        self.clicked.emit()

class Ui_LoginWindow(object):
    def setupUi(self, LoginWindow):
        LoginWindow.setObjectName("LoginWindow")
        LoginWindow.resize(800, 600)
        self.login_window = QtWidgets.QWidget(LoginWindow)
        self.login_window.setStyleSheet("""background-color : qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, 
        stop:0 rgba(176, 0, 0, 255), stop:0.738636 rgba(255, 113, 250, 255))""")
        self.login_window.setObjectName("MainWindow")
        self.username = QtWidgets.QLineEdit(self.login_window)
        self.username.setGeometry(QtCore.QRect(310, 140, 171, 31))
        self.username.setAutoFillBackground(False)
        self.username.setStyleSheet("background-color: rgb(255, 255, 255); border-radius: 5px")
        self.username.setObjectName("username")
        self.username.setText("postgres")
        self.password = QtWidgets.QLineEdit(self.login_window)
        self.password.setGeometry(QtCore.QRect(310, 230, 171, 31))
        self.password.setAutoFillBackground(False)
        self.password.setStyleSheet("background-color: rgb(255, 255, 255); border-radius: 5px")
        self.password.setObjectName("password")
        self.password.setEchoMode(QtWidgets.QLineEdit.Password) # Make the input hidden
        self.password.setText("mbpi")
        self.login_btn = QtWidgets.QPushButton(self.login_window)
        self.login_btn.setGeometry(QtCore.QRect(360, 340, 75, 23))
        self.login_btn.setStyleSheet("\n"
                                     "color: rgb(0, 0, 0);\n"
                                     "background-color: rgb(255, 255, 255); \n"
                                     "border-radius: 10px;")
        self.login_btn.setObjectName("Login")
        self.login_btn.clicked.connect(self.login)
        LoginWindow.setCentralWidget(self.login_window)



        self.retranslateUi(LoginWindow)
        QtCore.QMetaObject.connectSlotsByName(LoginWindow)

    def retranslateUi(self, LoginWindow):
        _translate = QtCore.QCoreApplication.translate
        LoginWindow.setWindowTitle(_translate("LoginWindow", "MBPI"))
        self.login_btn.setText(_translate("LoginWindow", "Login"))

    def login(self):
        username = self.username.text()
        pass1 = self.password.text()
        self.username.deleteLater()
        self.password.deleteLater()
        self.login_btn.deleteLater()

        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            dbname='postgres',
            user='postgres',
            password='postgres'
        )
        self.cursor = conn.cursor()

        self.launch_main()

    # This is the main window after login screen
    def launch_main(self):

        LoginWindow.move(0,0)
        LoginWindow.setFixedSize(1200,750)
        self.login_window.setStyleSheet("background-color: rgb(60,60,60);")
        self.main_widget = QtWidgets.QWidget(self.login_window)
        self.main_widget.setStyleSheet("""
        background-color: white;
        border-top-left-radius: 30px;
        border-bottom-left-radius: 30px;
        """)
        self.main_widget.setGeometry(QtCore.QRect(210, 0, 991, 751))
        self.main_widget.show()

        self.production_btn = QtWidgets.QPushButton(self.login_window)
        self.production_btn.setGeometry(30,200,180,40)
        self.production_btn.setCursor(Qt.PointingHandCursor)
        self.production_btn.setStyleSheet("border-top-left-radius: 10px; border-bottom-left-radius: 10px; background-color: rgb(125,125,125);")
        self.production_btn.clicked.connect(self.production)
        self.production_btn.show()

        self.production_lbl = QtWidgets.QLabel(self.production_btn)
        self.production_lbl.setText("Production")
        self.production_lbl.setGeometry(50,5,100,30)
        self.production_lbl.setFont(QtGui.QFont("Arial", 13))
        self.production_lbl.setStyleSheet("color: blue;")
        self.production_lbl.setCursor(Qt.PointingHandCursor)
        self.production_lbl.show()

        self.production_icon = ClickableLabel(self.production_btn)
        self.production_icon.setGeometry(10,3,30,30)
        self.production_icon.setPixmap(QtGui.QIcon('setting.png').pixmap(30, 30))  # Set icon
        self.production_icon.setScaledContents(True)  # Scale icon to fit the label
        self.production_icon.setCursor(Qt.PointingHandCursor)
        self.production_icon.show()


    def production(self):

        def show_form():
            selected = self.production_table.selectedItems()
            selected = [i.text() for i in selected]

            # Unpack all the items for convenience
            company, product_code, quantity_ordered, product_output = selected[1:5]
            formula, resin, t_start, t_end, total_time = selected[5:10]
            _operator, supervisor, materials, lot_number, feed_rate = selected[10:15]
            rpm, screen_size, screw_config, output_percent, loss = selected[15:20]
            loss_percent, purge_start, purge_end, purge_duration, remarks = selected[20:25]
            temperature = selected[25]


            # Clear all the widget first
            self.production_table.deleteLater()
            self.view_btn.deleteLater()
            self.add_btn.deleteLater()
            self.update_btn.deleteLater()

            font = QtGui.QFont("Arial", 15)

            self.ordered_company = QtWidgets.QLabel(self.main_widget)
            self.ordered_company.setGeometry(20,30,950,30)
            self.ordered_company.setFont(QtGui.QFont("Arial", 30))
            self.ordered_company.setText(company)
            self.ordered_company.setAlignment(Qt.AlignCenter)
            self.ordered_company.show()

            # Product Code Label
            self.code_label = QtWidgets.QLabel(self.main_widget)
            self.code_label.setText("Product Code:")
            self.code_label.setFont(font)
            self.code_label.setGeometry(50,100,150,30)
            self.code_label.setStyleSheet("background-color: red;")
            self.code_label.show()

            # Quantity Order Label
            self.order_label = QtWidgets.QLabel(self.main_widget)
            self.order_label.setText("Quantity Order:")
            self.order_label.setFont(font)
            self.order_label.setGeometry(50, 150, 150, 30)
            self.order_label.setStyleSheet("background-color: red;")
            self.order_label.show()

            self.output_label = QtWidgets.QLabel(self.main_widget)
            self.output_label.setText("Output:")
            self.output_label.setFont(font)
            self.output_label.setGeometry(50, 200, 150, 30)
            self.output_label.setStyleSheet("background-color: red;")
            self.output_label.show()

            self.formula_label = QtWidgets.QLabel(self.main_widget)
            self.formula_label.setText("Formula ID:")
            self.formula_label.setFont(font)
            self.formula_label.setGeometry(50, 250, 150, 30)
            self.formula_label.setStyleSheet("background-color: red;")
            self.formula_label.show()

            self.resin_label = QtWidgets.QLabel(self.main_widget)
            self.resin_label.setText("Resin:")
            self.resin_label.setFont(font)
            self.resin_label.setGeometry(50, 300, 150, 30)
            self.resin_label.setStyleSheet("background-color: red;")
            self.resin_label.show()

            self.lot_label = QtWidgets.QLabel(self.main_widget)
            self.lot_label.setText("LOT Number:")
            self.lot_label.setFont(font)
            self.lot_label.setGeometry(350, 100, 150, 30)
            self.lot_label.setStyleSheet("background-color: red;")
            self.lot_label.show()

            self.feedrate_label = QtWidgets.QLabel(self.main_widget)
            self.feedrate_label.setText("Feed Rate:")
            self.feedrate_label.setFont(font)
            self.feedrate_label.setGeometry(350, 150, 150, 30)
            self.feedrate_label.setStyleSheet("background-color: red;")
            self.feedrate_label.show()

            self.rpm_label = QtWidgets.QLabel(self.main_widget)
            self.rpm_label.setText("RPM:")
            self.rpm_label.setFont(font)
            self.rpm_label.setGeometry(350, 200, 150, 30)
            self.rpm_label.setStyleSheet("background-color: red;")
            self.rpm_label.show()

            self.screen_size_label = QtWidgets.QLabel(self.main_widget)
            self.screen_size_label.setText("Screen Size:")
            self.screen_size_label.setFont(font)
            self.screen_size_label.setGeometry(350, 250, 150, 30)
            self.screen_size_label.setStyleSheet("background-color: red;")
            self.screen_size_label.show()

            self.screwconfig_label = QtWidgets.QLabel(self.main_widget)
            self.screwconfig_label.setText("Screw Config:")
            self.screwconfig_label.setFont(font)
            self.screwconfig_label.setGeometry(350, 300, 150, 30)
            self.screwconfig_label.setStyleSheet("background-color: red;")
            self.screwconfig_label.show()

            self.code_label = QtWidgets.QLabel(self.main_widget)
            self.code_label.setText("Product Code:")
            self.code_label.setFont(font)
            self.code_label.setGeometry(50, 100, 150, 30)
            self.code_label.setStyleSheet("background-color: red;")
            self.code_label.show()

            self.output_percentage_lbl = QtWidgets.QLabel(self.main_widget)
            self.output_percentage_lbl.setText("Output %:")
            self.output_percentage_lbl.setFont(font)
            self.output_percentage_lbl.setGeometry(50, 100, 150, 30)
            self.output_percentage_lbl.setStyleSheet("background-color: red;")
            self.output_percentage_lbl.show()

            self.loss_label = QtWidgets.QLabel(self.main_widget)
            self.loss_label.setText("Loss:")
            self.loss_label.setFont(QtGui.QFont("Arial", 20))
            self.loss_label.setGeometry(50, 100, 150, 30)
            self.loss_label.setStyleSheet("background-color: red;")
            self.loss_label.show()

            self.loss_percent_label = QtWidgets.QLabel(self.main_widget)
            self.loss_percent_label.setText("Loss %:")
            self.loss_percent_label.setFont(QtGui.QFont("Arial", 20))
            self.loss_percent_label.setGeometry(50, 100, 150, 30)
            self.loss_percent_label.setStyleSheet("background-color: red;")
            self.loss_percent_label.show()

            self.purge_start_label = QtWidgets.QLabel(self.main_widget)
            self.purge_start_label.setText("Purge Start:")
            self.purge_start_label.setFont(QtGui.QFont("Arial", 20))
            self.purge_start_label.setGeometry(50, 100, 150, 30)
            self.purge_start_label.setStyleSheet("background-color: red;")
            self.purge_start_label.show()

            self.purge_end_label = QtWidgets.QLabel(self.main_widget)
            self.purge_end_label.setText("Purge End:")
            self.purge_end_label.setFont(QtGui.QFont("Arial", 20))
            self.purge_end_label.setGeometry(50, 100, 150, 30)
            self.purge_end_label.setStyleSheet("background-color: red;")
            self.purge_end_label.show()

            self.purge_duration_label = QtWidgets.QLabel(self.main_widget)
            self.purge_duration_label.setText("Purge Duration:")
            self.purge_duration_label.setFont(QtGui.QFont("Arial", 20))
            self.purge_duration_label.setGeometry(50, 100, 150, 30)
            self.purge_duration_label.setStyleSheet("background-color: red;")
            self.purge_duration_label.show()




        def add_entry():
            pass

        def update_entry():
            pass

        self.production_table = QtWidgets.QTableWidget(self.main_widget)
        self.production_table.setGeometry(QtCore.QRect(20, 30, 900, 375))

        try:
            self.cursor.execute("SELECT * FROM extruder;")
            result = self.cursor.fetchall()
        except Exception as e:
            print(e)

        self.cursor.execute(
            "SELECT column_name FROM information_schema.columns WHERE table_name = 'extruder';")
        column_names = self.cursor.fetchall()

        self.production_table.setColumnCount(len(column_names))
        self.production_table.setRowCount(len(result))

        # Populate table with data
        for i in range(len(result)):
            for j in range(len(column_names)):
                item = QtWidgets.QTableWidgetItem(str(result[i][j]))  # Convert to string
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make the cells unable to be edited
                self.production_table.setItem(i, j, item)

        self.production_table.setHorizontalHeaderLabels([col[0].upper() for col in column_names])  # Set column names

        self.view_btn = QtWidgets.QPushButton(self.main_widget)
        self.view_btn.setGeometry(100, 500, 100, 30)
        self.view_btn.setText("View")
        self.view_btn.setStyleSheet("background-color : red;")
        self.view_btn.clicked.connect(show_form)
        self.view_btn.show()

        self.add_btn = QtWidgets.QPushButton(self.main_widget)
        self.add_btn.setGeometry(250, 500, 100, 30)
        self.add_btn.setText("Add Entry")
        self.add_btn.setStyleSheet("background-color : red;")
        self.add_btn.clicked.connect(show_form)
        self.add_btn.show()

        self.update_btn = QtWidgets.QPushButton(self.main_widget)
        self.update_btn.setGeometry(400, 500, 100, 30)
        self.update_btn.setText("Update")
        self.update_btn.setStyleSheet("background-color : red;")
        self.update_btn.clicked.connect(update_entry)
        self.update_btn.show()

        # Set selection mode to select entire rows and disable single item selection
        self.production_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.production_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.production_table.show()






if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    LoginWindow = QtWidgets.QMainWindow()
    ui = Ui_LoginWindow()
    ui.setupUi(LoginWindow)
    LoginWindow.show()
    sys.exit(app.exec_())