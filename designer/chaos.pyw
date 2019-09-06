#from chaos_ui import *
from num_ui import *
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from functools import partial
import os

BUTTONMAP = {
1:"hand",
2:"gurtel",
3:"schuh",
4:"waffe",
5:"brust",
6:"ring",
8:"helm",
9:"amulett"
}

def increment(name):
    button = ui.groupBox.findChild(QtWidgets.QPushButton, name)
    button.setText(str(int(button.text()) + 1))

def decrement(name):
    button = ui.groupBox.findChild(QtWidgets.QPushButton, name)
    button.setText(str(int(button.text()) - 1))

def set_amount(name, amount):
    button = ui.groupBox.findChild(QtWidgets.QPushButton, name)
    button.setText(str(int(amount)))

def get_amount(name):
    return int(ui.groupBox.findChild(QtWidgets.QPushButton, name).text())

def get_amount_str(name):
    return ui.groupBox.findChild(QtWidgets.QPushButton, name).text()

def check_status_directory():
    if not os.path.isdir("./status"):
        os.mkdir("./status")
    return

def on_close(event):
    check_status_directory()

    # https://stackoverflow.com/questions/23279125/python-pyqt4-functions-to-save-and-restore-ui-widget-values
    settings = QtCore.QSettings("cv", "chaos-recipe-tracker")
    settings.setValue("geometry", MainWindow.saveGeometry())

    # save values of fields
    for _,v in BUTTONMAP.items():
        with open(f"status/{v}", "w") as f:
            f.write(get_amount_str(v))
    with open(f"status/total_c_sold", "w") as f:
        f.write(str(int(ui.TotalNumber.value())))
    return

def on_load():
    check_status_directory()

    settings = QtCore.QSettings("cv", "chaos-recipe-tracker")
    MainWindow.restoreGeometry(settings.value("geometry"))

    # load values of fields
    for _,v in BUTTONMAP.items():
        try:
            with open(f"status/{v}", "r") as f:
                amount = f.readline().strip()
        except:
            amount = 0
        finally:
            set_amount(v, amount)
    try:
        with open(f"status/total_c_sold", "r") as f:
            amount = f.readline().strip()
    except:
        amount = 0
    finally:
        ui.TotalNumber.display(str(int(amount)))
    return

def key_event(event):
    #modifiers = QtWidgets.QApplication.keyboardModifiers()
    modifiers = event.modifiers()
    if type(event) != QtGui.QKeyEvent:
        return
    #print(f"text:{event.text()}|num:{event.key()}")
    if event.key() == 45: # - button
        sell(1)
        return
    if event.key() == 43: # + button
        sell(2)
        return
    try:
        button_name = BUTTONMAP[int(chr(event.key()))]
    except:
        return
    if modifiers & QtCore.Qt.ControlModifier:
        decrement(button_name)
        return
    increment(button_name)

def sell(c):
    if check_full_set():
        for i in [1,2,3,4,5,6,8,9]:
            button_name = BUTTONMAP[i]
            if i == 6:
                decrement(button_name)
            decrement(button_name)
        ui.TotalNumber.display(str(int(ui.TotalNumber.value()) + c))
    return

def check_full_set():
    for i in [1,2,3,4,5,6,8,9]:
        button_name = BUTTONMAP[i]
        if i == 6:
            if get_amount(button_name) < 2:
                return False
        else:
            if get_amount(button_name) < 1:
                return False
    return True

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    MainWindow.keyPressEvent = key_event
    MainWindow.closeEvent = on_close
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)

    #---
    for button in ui.groupBox.findChildren(QtWidgets.QPushButton):
        button.clicked.connect(partial(increment, button.objectName()))
    ui.sell1.clicked.connect(partial(sell, 1))
    ui.sell2.clicked.connect(partial(sell, 2))
    #---
    on_load()
    MainWindow.show()
    sys.exit(app.exec_())
