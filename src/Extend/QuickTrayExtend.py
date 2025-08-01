# -*- coding: UTF-8 -*-
"""
PROJECT_NAME Python_projects
PRODUCT_NAME PyCharm
NAME QuickTrayExtend
AUTHOR Pfolg
TIME 2025/7/17 20:28
"""
import json
import os
import sys

from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QApplication, QPushButton, QLabel, QLineEdit, QFileDialog, QMessageBox, \
    QTextEdit, QComboBox

app_folder = "app_config"
if not os.path.exists(app_folder):
    app_folder = "..\\app_config"
config_files = os.listdir(app_folder)


# 读取屏幕长宽
def get_screen_info() -> tuple:
    # 获取现有的 QApplication 实例
    _app = QApplication.instance()

    if _app is not None:
        screen = _app.primaryScreen().geometry()

        return screen.width(), screen.height()
    else:
        return 800, 600


class EWidget(QWidget):
    def __init__(self, p=None):
        super().__init__()
        self._window_name = "QuickTrayExtendMenu"
        self._string_choose = "Enter to choose"
        self._string_add = "add"
        self._string_update = "update"
        self._string_open = "open"
        self._string_sentence = "input..."
        self._string_change = "change"
        self._string_warning_empty_input = "Nothing input, add None! "
        self._string_information_add_success = "Added successfully!"
        self._string_path_not_exists = "Path not exists!"
        self._string_plshd = "Patience is key in life."
        self.picture_filter = "*.jpg *.png *.svg *.ico"
        self._string_warning_wrong_instance = "Input data type mismatch!"
        self.setParent(p)
        self.tabWidget = QtWidgets.QTabWidget(parent=self)
        self.tabs = {}

        self.init()
        self.adjustSize()

    def init(self):
        sw, sh = get_screen_info()
        _w, _h = 400, 300
        self.setGeometry(int((sw - _w) / 2), int((sh - _h) / 2), _w, _h)
        self.setMaximumSize(_w, _h)
        self.setWindowTitle(self._window_name)
        self.setWindowFlags(
            Qt.WindowType.Window |
            # Qt.WindowType.WindowMaximizeButtonHint |
            Qt.WindowType.WindowCloseButtonHint
        )

        for _ in config_files:
            a = QtWidgets.QWidget()
            self.tabWidget.addTab(a, "")
            self.tabs[_] = a
            self.tabWidget.setTabText(self.tabWidget.indexOf(a), (_.split(".")[0]))

        self.tabWidget.setGeometry(0, 0, _w, _h)
        self.control_applist()
        self.control_config()
        self.control_lines()

    def control_config(self):
        special_keys1 = ["usecount", "port"]
        special_keys2 = ["autorun"]
        special_keys3 = ["logo"]

        try:
            file = config_files[1]
            fp = app_folder + "/" + file
            tab = self.tabs[file]
            with open(fp, "r", encoding="utf-8") as file:
                org_data: dict = json.load(file)
            keys = list(org_data.keys())

            box = QComboBox(tab)
            input_box = QLineEdit(tab)
            view = QTextEdit(tab)
            btn_change = QPushButton(self._string_change, tab)
            btn_update = QPushButton(self._string_update, tab)
            btn_open = QPushButton(self._string_open, tab)

            box.addItems(keys)

            box.setGeometry(20, 20, 100, 30)
            input_box.setGeometry(160, 20, 180, 30)
            view.setGeometry(20, 120, 360, 120)

            fx, st = 120, 80
            for i in [btn_open, btn_update, btn_change]:
                i.setGeometry(fx, 60, 60, 30)
                fx += st

            def func_update():
                with open(fp, "r", encoding="utf-8") as f:
                    d = f.read()
                    view.setText(d)

            def func_change():
                key, value = box.currentText(), input_box.text()
                if value:
                    if key in special_keys1 or key in special_keys2:
                        value = eval(value)
                    if key in special_keys3:
                        if not os.path.exists(value):
                            QMessageBox.critical(
                                self,
                                "Error",
                                self._string_path_not_exists + "\n" + value
                            )

                    with open(fp, "r", encoding="utf-8") as f1:
                        d: dict = json.load(f1)
                    if isinstance(value, type(d.get(key))):
                        print(True)
                        d[key] = value
                        with open(fp, "w", encoding="utf-8") as f2:
                            json.dump(d, f2, indent=4, ensure_ascii=False)
                    else:
                        print(False)
                        QMessageBox.warning(
                            self,
                            "Warning",
                            self._string_warning_wrong_instance
                        )
                else:
                    QMessageBox.warning(
                        self,
                        "Warning",
                        self._string_warning_empty_input
                    )

            def choice_file():
                key = box.currentText()
                if key not in special_keys3:
                    return
                fd = QFileDialog()
                fd.setFileMode(QFileDialog.FileMode.ExistingFile)
                fd.setNameFilter(self.picture_filter)
                fd.setViewMode(QFileDialog.ViewMode.List)
                if fd.exec():
                    a = fd.selectedFiles()
                    input_box.setText(a[0])

            def func_on_var_change():
                key = box.currentText()
                with open(fp, "r", encoding="utf-8") as f1:
                    d: dict = json.load(f1)
                input_box.setPlaceholderText(str(type(d.get(key))))

            btn_open.clicked.connect(lambda: os.startfile(os.path.join(os.getcwd(), fp)))
            btn_update.clicked.connect(func_update)
            btn_change.clicked.connect(func_change)
            input_box.returnPressed.connect(choice_file)
            box.currentTextChanged.connect(func_on_var_change)

            func_update()
            func_on_var_change()

        except Exception as e:
            print(e)
            return

    def control_lines(self):
        try:
            file = config_files[2]
            fp = app_folder + "/" + file
            tab = self.tabs[file]

            label = QLabel(self._string_sentence, tab)
            input_edit = QLineEdit(tab)
            btn_add = QPushButton(self._string_add, tab)
            btn_update = QPushButton(self._string_update, tab)
            btn_open = QPushButton(self._string_open, tab)
            show_lines = QTextEdit(tab)

            label.setGeometry(20, 20, 60, 40)
            input_edit.setGeometry(100, 20, 240, 30)
            show_lines.setGeometry(20, 100, 360, 150)
            lx, st = 120, 80
            for i in [btn_open, btn_update, btn_add]:
                i.setGeometry(lx, 60, 60, 30)
                lx += st

            show_lines.setReadOnly(True)
            input_edit.setPlaceholderText(self._string_plshd)

            def func_update():
                try:
                    with open(fp, "r", encoding="utf-8") as f:
                        _lines = f.read()
                        show_lines.setText(_lines)
                except FileNotFoundError:
                    return

            def func_add():
                text = input_edit.text()
                if text:
                    with open(fp, "r", encoding="utf-8") as f1:
                        org: list = json.load(f1)
                    org.append(text)
                    with open(fp, "w", encoding="utf-8") as f2:
                        json.dump(org, f2, indent=4, ensure_ascii=False)
                    QMessageBox.information(
                        self,
                        "Tip",
                        self._string_information_add_success + "\n" + text,
                        QMessageBox.StandardButton.Ok
                    )
                else:
                    QMessageBox.warning(
                        self,
                        "Warning",
                        self._string_warning_empty_input
                    )

            btn_open.clicked.connect(lambda: os.startfile(os.path.join(os.getcwd(), fp)))
            btn_update.clicked.connect(func_update)
            btn_add.clicked.connect(func_add)

            func_update()

        except Exception as e:
            print(e)
            return

    @staticmethod
    def find_icon(x: QLineEdit, _filter=None):
        fd = QFileDialog()
        fd.setFileMode(QFileDialog.FileMode.ExistingFile)
        fd.setNameFilter(_filter)
        fd.setViewMode(QFileDialog.ViewMode.List)
        if fd.exec():
            a = fd.selectedFiles()
            x.setText(a[0])

    def add_item(self, _type: str, _name, _path, _icon, _data: list[dict], _file):
        if _type and _name and _path:
            t = _type.replace("，", ",").split(",")
            if not os.path.exists(_path):
                QMessageBox.critical(
                    self,
                    "Error",
                    self._string_path_not_exists + "\n" + _path

                )
                return
            if not os.path.exists(_icon):
                # QMessageBox.warning(
                #     self,
                #     "Warning",
                #     self._string_path_not_exists + "\n" + _icon
                # )
                pass
            for i in _data:
                if i.get("name") == _name:
                    _data.remove(i)
            item = {
                "type": t,
                "name": _name,
                "path": _path,
                "icon": _icon,
            }
            _data.append(item)
            with open(_file, "w", encoding="utf-8") as f:
                json.dump(_data, f, indent=4, ensure_ascii=False)
                QMessageBox.information(
                    self,
                    "Tip",
                    self._string_information_add_success + "\n" + str(item),
                    QMessageBox.StandardButton.Ok
                )
        else:
            QMessageBox.critical(
                self,
                "Warning",
                self._string_warning_empty_input
            )

    def control_applist(self):
        # ["star", "app", "link", "scripts"]
        try:
            file = config_files[0]
            fp = app_folder + "/" + file
            tab = self.tabs[file]
            with open(fp, "r", encoding="utf-8") as f:
                origin_data: list[dict] = json.load(f)
            keys = list(origin_data[0].keys())

            x, y, w, h, s, v = 20, 20, 100, 20, 100, 30
            cache = {}
            for i in keys:
                view = QLabel(tab)
                view.setText(i)
                b = QLineEdit(tab)
                view.setGeometry(x, y, w, h)
                b.setGeometry(x + s, y, w * 2, h)
                if i != keys[3]:
                    view.setText(view.text() + "*")
                if i == keys[0]:
                    b.setPlaceholderText("star, app, link, scripts")
                y += v
                cache[i] = (view, b)

            _type: QLineEdit = cache[keys[0]][1]
            _name: QLineEdit = cache[keys[1]][1]
            _icon: QLineEdit = cache[keys[3]][1]
            _icon.setPlaceholderText(self._string_choose)
            _icon.returnPressed.connect(
                lambda: self.find_icon(_icon, self.picture_filter)
            )
            _path: QLineEdit = cache[keys[2]][1]
            _path.setPlaceholderText(self._string_choose)
            _path.returnPressed.connect(
                lambda: self.find_icon(_path)
            )

            view = QTextEdit(tab)

            def update_view():
                with open(fp, "r", encoding="utf-8") as _file:
                    _data = _file.read()
                view.setText(_data)

            btn_add = QPushButton(self._string_add, tab)
            btn_add.setGeometry(300, 140, 60, 30)
            btn_add.clicked.connect(
                lambda: self.add_item(
                    _type.text(), _name.text(), _path.text(), _icon.text(), origin_data, fp
                ))

            btn_update = QPushButton(self._string_update, tab)
            btn_update.setGeometry(220, 140, 60, 30)
            btn_update.clicked.connect(update_view)

            btn_open = QPushButton(self._string_open, tab)
            btn_open.setGeometry(140, 140, 60, 30)
            btn_open.clicked.connect(lambda: os.startfile(os.path.join(os.getcwd(), fp)))

            view.setReadOnly(True)
            update_view()
            view.setGeometry(20, 180, 360, 80)
        except Exception as e:
            print(e)
            return


if __name__ == '__main__':
    print(config_files)
    app = QApplication(sys.argv)

    ew = EWidget()
    ew.show()

    sys.exit(app.exec())
