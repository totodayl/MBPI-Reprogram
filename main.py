import datetime
import json
import psycopg2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt, pyqtSignal
import re
from PyQt5.QtWidgets import *
from datetime import time
import datetime as dt






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
        self.production_lbl.setGeometry(50, 5, 100, 30)
        self.production_lbl.setFont(QtGui.QFont("Arial", 13))
        self.production_lbl.setStyleSheet("color: blue;")
        self.production_lbl.setCursor(Qt.PointingHandCursor)
        self.production_lbl.show()

        self.production_icon = ClickableLabel(self.production_btn)
        self.production_icon.setGeometry(10, 3, 30, 30)
        self.production_icon.setPixmap(QtGui.QIcon('setting.png').pixmap(30, 30))  # Set icon
        self.production_icon.setScaledContents(True)  # Scale icon to fit the label
        self.production_icon.setCursor(Qt.PointingHandCursor)
        self.production_icon.show()

    def production(self):

        # Delete If there are existing Widgets
        try:
            self.info_widget.deleteLater()
            self.temp_table.deleteLater()
            self.time_table.deleteLater()
            self.material_table.deleteLater()
        except Exception as e:
            print(e)

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
            machine = selected[26]

            # Convert stringo of json to JSON
            materials = materials.replace("'", '"')
            materials = json.loads(materials)

            # Regular expression pattern to match time values
            time_pattern = r'datetime\.time\((\d+), (\d+)\)'

            # Extract time values using regular expression
            matches = re.findall(time_pattern, t_start)

            # Convert matched values to time objects and create a list
            t_start = [time(int(match[0]), int(match[1])) for match in matches]
            matches = re.findall(time_pattern, t_end)
            t_end = [time(int(match[0]), int(match[1])) for match in matches]

            # Converts String To List
            temperature = temperature.replace("[","").replace("]","")
            temperature = temperature.split(",")



            # Clear all the widget first
            self.production_table.deleteLater()
            self.view_btn.deleteLater()
            self.add_btn.deleteLater()
            self.update_btn.deleteLater()

            self.info_widget = QtWidgets.QWidget(self.main_widget)
            self.info_widget.setGeometry(20, 20, 951, 450)
            self.info_widget.setStyleSheet("border-radius: 30px; background-color: rgb(0,109,189);")
            self.info_widget.show()

            font = QtGui.QFont("Arial", 14) # Set Font for Labels

            self.ordered_company = QtWidgets.QLabel(self.info_widget)
            self.ordered_company.setGeometry(20,30,950,30)
            self.ordered_company.setFont(QtGui.QFont("Arial", 30))
            self.ordered_company.setStyleSheet("background-color: rgb(0,109,184);")
            self.ordered_company.setText(company)
            self.ordered_company.setAlignment(Qt.AlignCenter)
            self.ordered_company.show()

            # Extruder Label
            self.machine_label = QtWidgets.QLabel(self.info_widget)
            self.machine_label.setText("Extruder:")
            self.machine_label.setFont(font)
            self.machine_label.setGeometry(50, 80, 80, 30)
            self.machine_label.setStyleSheet("background-color: red;")
            self.machine_label.show()

            # Show Extruder Value
            self.extruder_val = QtWidgets.QLabel(self.info_widget)
            self.extruder_val.setGeometry(200,80,120,30)
            self.extruder_val.setText(machine)
            self.extruder_val.setFont(font)
            self.extruder_val.show()

            # Product Code Label
            self.code_label = QtWidgets.QLabel(self.info_widget)
            self.code_label.setText("Product Code:")
            self.code_label.setFont(font)
            self.code_label.setGeometry(50,125,130,30)
            self.code_label.setStyleSheet("background-color: red;")
            self.code_label.show()

            # Show Product Code Value
            self.product_code_val = QtWidgets.QLabel(self.info_widget)
            self.product_code_val.setGeometry(200,125,150,30)
            self.product_code_val.setText(product_code)
            self.product_code_val.setFont(font)
            self.product_code_val.show()

            # Quantity Order Label
            self.order_label = QtWidgets.QLabel(self.info_widget)
            self.order_label.setText("Quantity Order:")
            self.order_label.setFont(font)
            self.order_label.setGeometry(50, 170, 130, 30)
            self.order_label.setStyleSheet("background-color: red;")
            self.order_label.show()

            # Show Order Value
            self.order_val = QtWidgets.QLabel(self.info_widget)
            self.order_val.setGeometry(200, 170, 150, 30)
            self.order_val.setText(quantity_ordered)
            self.order_val.setFont(font)
            self.order_val.show()

            self.output_label = QtWidgets.QLabel(self.info_widget)
            self.output_label.setText("Output:")
            self.output_label.setFont(font)
            self.output_label.setGeometry(50, 215, 60, 30)
            self.output_label.setStyleSheet("background-color: red;")
            self.output_label.show()

            # Show Output Value
            self.output_val = QtWidgets.QLabel(self.info_widget)
            self.output_val.setGeometry(200, 215, 150, 30)
            self.output_val.setText(product_output)
            self.output_val.setFont(font)
            self.output_val.show()

            self.formula_label = QtWidgets.QLabel(self.info_widget)
            self.formula_label.setText("Formula ID:")
            self.formula_label.setFont(font)
            self.formula_label.setGeometry(50, 260, 100, 30)
            self.formula_label.setStyleSheet("background-color: red;")
            self.formula_label.show()

            # Show Formula ID Value
            self.formulaID_val = QtWidgets.QLabel(self.info_widget)
            self.formulaID_val.setGeometry(200, 260, 150, 30)
            self.formulaID_val.setText(formula)
            self.formulaID_val.setFont(font)
            self.formulaID_val.show()

            self.resin_label = QtWidgets.QLabel(self.info_widget)
            self.resin_label.setText("Resin:")
            self.resin_label.setFont(font)
            self.resin_label.setGeometry(50, 305, 60, 30)
            self.resin_label.setStyleSheet("background-color: red;")
            self.resin_label.show()

            # Show Resin Value
            self.resin_val = QtWidgets.QLabel(self.info_widget)
            self.resin_val.setGeometry(200, 305, 100, 30)
            self.resin_val.setText(resin)
            self.resin_val.setFont(font)
            self.resin_val.show()

            # Lot Label
            self.lot_label = QtWidgets.QLabel(self.info_widget)
            self.lot_label.setText("LOT Number:")
            self.lot_label.setFont(font)
            self.lot_label.setGeometry(350, 80, 120, 30)
            self.lot_label.setStyleSheet("background-color: red;")
            self.lot_label.show()

            # Show Lot Number Value
            self.lotNum_val = QtWidgets.QLabel(self.info_widget)
            self.lotNum_val.setGeometry(490, 80, 150, 30)
            self.lotNum_val.setText(resin)
            self.lotNum_val.setFont(font)
            self.lotNum_val.show()

            self.feedrate_label = QtWidgets.QLabel(self.info_widget)
            self.feedrate_label.setText("Feed Rate:")
            self.feedrate_label.setFont(font)
            self.feedrate_label.setGeometry(350, 125, 120, 30)
            self.feedrate_label.setStyleSheet("background-color: red;")
            self.feedrate_label.show()

            # Show Feed Rate Value
            self.feedrate_val = QtWidgets.QLabel(self.info_widget)
            self.feedrate_val.setGeometry(490, 125, 150, 30)
            self.feedrate_val.setText(resin)
            self.feedrate_val.setFont(font)
            self.feedrate_val.show()

            # RPM label
            self.rpm_label = QtWidgets.QLabel(self.info_widget)
            self.rpm_label.setText("RPM:")
            self.rpm_label.setFont(font)
            self.rpm_label.setGeometry(350, 170, 120, 30)
            self.rpm_label.setStyleSheet("background-color: red;")
            self.rpm_label.show()

            # Show RPM Value
            self.rpm_val = QtWidgets.QLabel(self.info_widget)
            self.rpm_val.setGeometry(490, 170, 150, 30)
            self.rpm_val.setText(resin)
            self.rpm_val.setFont(font)
            self.rpm_val.show()

            # Screen Size Label
            self.screen_size_label = QtWidgets.QLabel(self.info_widget)
            self.screen_size_label.setText("Screen Size:")
            self.screen_size_label.setFont(font)
            self.screen_size_label.setGeometry(350, 215, 120, 30)
            self.screen_size_label.setStyleSheet("background-color: red;")
            self.screen_size_label.show()

            # Show Screen Size Value
            self.screenSize_val = QtWidgets.QLabel(self.info_widget)
            self.screenSize_val.setGeometry(490, 215, 150, 30)
            self.screenSize_val.setText(resin)
            self.screenSize_val.setFont(font)
            self.screenSize_val.show()

            self.screwconfig_label = QtWidgets.QLabel(self.info_widget)
            self.screwconfig_label.setText("Screw Config:")
            self.screwconfig_label.setFont(font)
            self.screwconfig_label.setGeometry(350, 260, 130, 30)
            self.screwconfig_label.setStyleSheet("background-color: red;")
            self.screwconfig_label.show()

            # Show Screw Config Value
            self.screwConf_val = QtWidgets.QLabel(self.info_widget)
            self.screwConf_val.setGeometry(490, 260, 150, 30)
            self.screwConf_val.setText(resin)
            self.screwConf_val.setFont(font)
            self.screwConf_val.show()

            # Output % Label
            self.output_percentage_lbl = QtWidgets.QLabel(self.info_widget)
            self.output_percentage_lbl.setText("Output %:")
            self.output_percentage_lbl.setFont(font)
            self.output_percentage_lbl.setGeometry(650, 80, 140, 30)
            self.output_percentage_lbl.setStyleSheet("background-color: red;")
            self.output_percentage_lbl.show()

            # Show Output Percentage Value
            self.outputPercent_val = QtWidgets.QLabel(self.info_widget)
            self.outputPercent_val.setGeometry(800, 80, 150, 30)
            self.outputPercent_val.setText(resin)
            self.outputPercent_val.setFont(font)
            self.outputPercent_val.show()

            # Loss Label
            self.loss_label = QtWidgets.QLabel(self.info_widget)
            self.loss_label.setText("Loss:")
            self.loss_label.setFont(QtGui.QFont(font))
            self.loss_label.setGeometry(650, 125, 140, 30)
            self.loss_label.setStyleSheet("background-color: red;")
            self.loss_label.show()

            # Show Loss Value
            self.loss_val = QtWidgets.QLabel(self.info_widget)
            self.loss_val.setGeometry(800, 125, 150, 30)
            self.loss_val.setText(resin)
            self.loss_val.setFont(font)
            self.loss_val.show()

            # loss percentage Label
            self.loss_percent_label = QtWidgets.QLabel(self.info_widget)
            self.loss_percent_label.setText("Loss %:")
            self.loss_percent_label.setFont(font)
            self.loss_percent_label.setGeometry(650, 170, 140, 30)
            self.loss_percent_label.setStyleSheet("background-color: red;")
            self.loss_percent_label.show()

            # Show Loss Percentage Value
            self.lossPercent_val = QtWidgets.QLabel(self.info_widget)
            self.lossPercent_val.setGeometry(800, 170, 150, 30)
            self.lossPercent_val.setText(resin)
            self.lossPercent_val.setFont(font)
            self.lossPercent_val.show()

            # Purge Start Label
            self.purge_start_label = QtWidgets.QLabel(self.info_widget)
            self.purge_start_label.setText("Purge Start:")
            self.purge_start_label.setFont(font)
            self.purge_start_label.setGeometry(650, 215, 140, 30)
            self.purge_start_label.setStyleSheet("background-color: red;")
            self.purge_start_label.show()

            # Show Purge Start Value
            self.purgeStart_val = QtWidgets.QLabel(self.info_widget)
            self.purgeStart_val.setGeometry(800, 215, 150, 30)
            self.purgeStart_val.setText(resin)
            self.purgeStart_val.setFont(font)
            self.purgeStart_val.show()

            # Purge End Label
            self.purge_end_label = QtWidgets.QLabel(self.info_widget)
            self.purge_end_label.setText("Purge End:")
            self.purge_end_label.setFont(font)
            self.purge_end_label.setGeometry(650, 260, 140, 30)
            self.purge_end_label.setStyleSheet("background-color: red;")
            self.purge_end_label.show()

            # Show Purge End Value
            self.purgeEnd_val = QtWidgets.QLabel(self.info_widget)
            self.purgeEnd_val.setGeometry(800, 260, 150, 30)
            self.purgeEnd_val.setText(resin)
            self.purgeEnd_val.setFont(font)
            self.purgeEnd_val.show()

            # Purge Duration Label
            self.purge_duration_label = QtWidgets.QLabel(self.info_widget)
            self.purge_duration_label.setText("Purge Duration:")
            self.purge_duration_label.setFont(font)
            self.purge_duration_label.setGeometry(650, 305, 140, 30)
            self.purge_duration_label.setStyleSheet("background-color: red;")
            self.purge_duration_label.show()

            # Show Resin Value
            self.purgeDuration_val = QtWidgets.QLabel(self.info_widget)
            self.purgeDuration_val.setGeometry(800, 305, 150, 30)
            self.purgeDuration_val.setText(resin)
            self.purgeDuration_val.setFont(font)
            self.purgeDuration_val.show()

            try:
                # Create 3 tables for Time, Materials and Temperature
                self.time_table = QtWidgets.QTableWidget(self.main_widget)
                self.time_table.setGeometry(0, 490, 330, 250)
                self.time_table.setColumnCount(3)
                self.time_table.setRowCount(len(t_start) + 2)
                self.time_rows = len(t_start)
                self.time_cols = 3
                self.time_table.setHorizontalHeaderLabels(["Time Start", "Time End", "Time Diff"])
                total_timediff = datetime.timedelta()
                for i in range(self.time_rows):
                    for j in range(self.time_cols):
                        if j == 0:
                            item = QtWidgets.QTableWidgetItem(t_start[i].strftime('%H:%M:%S'))  # Convert to string
                            item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make the cells unable to be edited
                            self.time_table.setItem(i, j, item)
                        elif j == 1:
                            item = QtWidgets.QTableWidgetItem(t_end[i].strftime('%H:%M:%S'))  # Convert to string
                            item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # Make the cells unable to be edited
                            self.time_table.setItem(i, j, item)
                        else:

                            datetime1 = dt.datetime.combine(dt.datetime.today(), t_start[i])
                            datetime2 = dt.datetime.combine(dt.datetime.today(), t_end[i])
                            t_diff = datetime2 - datetime1
                            # Convert timedelta to a string representation (e.g., "X days, HH:MM:SS")
                            total_timediff = total_timediff + t_diff
                            t_diff_str = str(t_diff)
                            item = QtWidgets.QTableWidgetItem(t_diff_str)
                            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                            self.time_table.setItem(i, j, item)

                # Convert it to Hours and Minutes only
                total_hours = total_timediff.days * 24 + total_timediff.seconds // 3600
                total_minutes = (total_timediff.seconds % 3600) // 60

                self.time_table.setItem(self.time_rows + 1, 1, QtWidgets.QTableWidgetItem("Total"))
                self.time_table.setItem(self.time_rows + 1, 2, QtWidgets.QTableWidgetItem(str(total_hours)+":"+str(total_minutes)))
                self.time_table.show()

                # Material Table
                self.material_table = QtWidgets.QTableWidget(self.main_widget)
                self.material_table.setRowCount(len(materials))
                self.material_table.setColumnCount(3)
                self.material_table.setGeometry(360,490,300,250)
                self.material_table.setStyleSheet("gridline-color: rgb(255, 0, 0);")
                self.material_table.setHorizontalHeaderLabels(["Materials", "Quantity(Kg)",""])
                self.material_table.horizontalHeader().setStyleSheet("QHeaderView::section { border: 1px solid red; }")
                self.material_table.verticalHeader().setVisible(False)

                for key in list(materials.keys()):
                    key_item = QtWidgets.QTableWidgetItem(str(key))
                    value_item = QtWidgets.QTableWidgetItem(str(materials[key]))
                    key_item.setFlags(key_item.flags() & ~Qt.ItemIsEditable)  # Make the cells unable to be edited
                    value_item.setFlags(value_item.flags() & ~Qt.ItemIsEditable)  # Make the cells unable to be edited
                    self.material_table.setItem(list(materials.keys()).index(key), 0, key_item)
                    self.material_table.setItem(list(materials.keys()).index(key), 1, value_item)

                self.material_table.show()

                # Temperature Table
                self.temp_table = QtWidgets.QTableWidget(self.main_widget)
                self.temp_table.setGeometry(760,490,230,250)
                self.temp_table.setRowCount(12)
                self.temp_table.setColumnCount(2)
                self.temp_table.setHorizontalHeaderLabels(["Zone", "Temperature"])
                self.temp_table.setStyleSheet("gridline-color: red;")
                self.temp_table.horizontalHeader().setStyleSheet("QHeaderView::section { border: 1px solid red; }")
                self.temp_table.verticalHeader().setVisible(False)

                # Populate the First Column
                for i in range(13):
                    item = QtWidgets.QTableWidgetItem("Z" + str(i+1))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.temp_table.setItem(i,0, item)


                # Populate the 2nd Column
                for i in range(len(temperature)):
                    item = QtWidgets.QTableWidgetItem(str(temperature[i]))
                    item.setFlags(item.flags() & ~Qt.ItemIsEditable)
                    self.temp_table.setItem(i, 1, item)

                self.temp_table.show()

            except Exception as e:
                print(e)

        def add_entry():

            self.entry_widget = QtWidgets.QWidget()
            self.entry_widget.setGeometry(300, 100, 600, 600)
            self.entry_widget.setStyleSheet("background-color : rgb(0,109,189);")
            self.entry_widget.show()

            # Create two new widget for the VBOX Layout
            self.leftInput_side = QtWidgets.QWidget(self.entry_widget)
            self.leftInput_side.setGeometry(0, 0, 300, 400)
            self.leftInput_side.show()

            self.right_side = QtWidgets.QWidget(self.entry_widget)
            self.right_side.setGeometry(300, 0, 300, 400)
            self.right_side.show()

            # Create Vertical Box Layout
            self.left_vbox = QtWidgets.QFormLayout(self.leftInput_side)
            self.left_vbox.setSpacing(20)
            self.right_vbox = QtWidgets.QFormLayout(self.right_side)
            self.right_vbox.setSpacing(20)

            font = QtGui.QFont("Berlin Sans FB", 14)


            customer_label = QtWidgets.QLabel()
            customer_label.setText("Customer")
            customer_label.setFont(font)

            productCode_label = QtWidgets.QLabel()
            productCode_label.setText("Product Code")
            productCode_label.setFont(font)

            productOutput_label = QtWidgets.QLabel()
            productOutput_label.setText("Output (kg)")
            productOutput_label.setFont(font)

            formulaID_label = QtWidgets.QLabel()
            formulaID_label.setText("Formula ID")
            formulaID_label.setFont(font)

            lotnumber_label = QtWidgets.QLabel()
            lotnumber_label.setText("Lot Number")
            lotnumber_label.setFont(font)

            orderedQuantity_label = QtWidgets.QLabel()
            orderedQuantity_label.setText("Ordered Qty")
            orderedQuantity_label.setFont(font)

            feedrate_label = QtWidgets.QLabel()
            feedrate_label.setText("Feed Rate")
            feedrate_label.setFont(font)

            rpm_label = QtWidgets.QLabel()
            rpm_label.setText("RPM")
            rpm_label.setFont(font)

            screenSize_label = QtWidgets.QLabel()
            screenSize_label.setText("Screen Size")
            screenSize_label.setFont(font)

            screwConf_label = QtWidgets.QLabel()
            screwConf_label.setText("Screw Config")
            screwConf_label.setFont(font)

            loss_label = QtWidgets.QLabel()
            loss_label.setText("Loss Label")
            loss_label.setFont(font)

            purgeStart_label = QtWidgets.QLabel()
            purgeStart_label.setText("Purge Start")
            purgeStart_label.setFont(font)

            purgeEnd_label = QtWidgets.QLabel()
            purgeEnd_label.setText("Purge End")
            purgeEnd_label.setFont(font)

            remarks_label = QtWidgets.QLabel()

            operator_label = QtWidgets.QLabel()
            operator_label.setText("Operator")
            operator_label.setFont(font)

            supervisor_label = QtWidgets.QLabel()
            supervisor_label.setText("Supervisor")
            supervisor_label.setFont(font)

            # QLineEdit Boxes
            customer_input = QtWidgets.QLineEdit()
            customer_input.setFixedHeight(25)
            orderedQuantity = QtWidgets.QLineEdit()
            orderedQuantity.setFixedHeight(25)
            productCode = QtWidgets.QLineEdit()
            productCode.setFixedHeight(25)
            product_output = QtWidgets.QLineEdit()
            product_output.setFixedHeight(25)
            formulaID = QtWidgets.QLineEdit()
            formulaID.setFixedHeight(25)
            lot_number = QtWidgets.QLineEdit()
            lot_number.setFixedHeight(25)
            feedRate = QtWidgets.QLineEdit()
            feedRate.setFixedHeight(25)
            rpm = QtWidgets.QLineEdit()
            rpm.setFixedHeight(25)
            screenSize = QtWidgets.QLineEdit()
            screenSize.setFixedHeight(25)
            screwConf = QtWidgets.QLineEdit()
            screwConf.setFixedHeight(25)
            loss = QtWidgets.QLineEdit()
            loss.setFixedHeight(25)
            purgeStart = QtWidgets.QLineEdit()
            purgeStart.setFixedHeight(25)
            purgeEnd = QtWidgets.QLineEdit()
            purgeEnd.setFixedHeight(25)
            remarks = QtWidgets.QTextEdit()
            operator = QtWidgets.QLineEdit()
            operator.setFixedHeight(25)
            supervisor = QtWidgets.QLineEdit()
            supervisor.setFixedHeight(25)

            # Left Side of Vertical Box
            self.left_vbox.addRow(customer_label,customer_input)
            self.left_vbox.addRow(productCode_label,productCode)
            self.left_vbox.addRow(productOutput_label, product_output)
            self.left_vbox.addRow(formulaID_label,formulaID)
            self.left_vbox.addRow(lotnumber_label, lot_number)
            self.left_vbox.addRow(orderedQuantity_label, orderedQuantity)
            self.left_vbox.addRow(loss_label, loss)



            # Add widgets to the right Form Box
            self.right_vbox.addRow(feedrate_label,feedRate)
            self.right_vbox.addRow(rpm_label, rpm)
            self.right_vbox.addRow(screenSize_label, screenSize)
            self.right_vbox.addRow(screwConf_label, screwConf)
            self.right_vbox.addRow(purgeStart_label, purgeStart)
            self.right_vbox.addRow(purgeEnd_label, purgeEnd)
            self.right_vbox.addRow(operator_label, operator)
            self.right_vbox.addRow(supervisor_label, supervisor)











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
        self.add_btn.clicked.connect(add_entry)
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