# Form implementation generated from reading ui file 'designer/form.ui'
#
# Created by: PyQt6 UI code generator 6.3.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(512, 327)
        self.formLayout_2 = QtWidgets.QFormLayout(Dialog)
        self.formLayout_2.setObjectName("formLayout_2")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setObjectName("label_5")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_5)
        self.searchFieldComboBox = QtWidgets.QComboBox(Dialog)
        self.searchFieldComboBox.setObjectName("searchFieldComboBox")
        self.formLayout_2.setWidget(0, QtWidgets.QFormLayout.ItemRole.FieldRole, self.searchFieldComboBox)
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setObjectName("label_6")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.label_6)
        self.highlightFieldComboBox = QtWidgets.QComboBox(Dialog)
        self.highlightFieldComboBox.setObjectName("highlightFieldComboBox")
        self.formLayout_2.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.highlightFieldComboBox)
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setObjectName("groupBox")
        self.formLayout = QtWidgets.QFormLayout(self.groupBox)
        self.formLayout.setObjectName("formLayout")
        self.highlightCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.highlightCheckBox.setObjectName("highlightCheckBox")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.ItemRole.LabelRole, self.highlightCheckBox)
        self.clozeCheckbox = QtWidgets.QCheckBox(self.groupBox)
        self.clozeCheckbox.setObjectName("clozeCheckbox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.clozeCheckbox)
        self.increasingClozeCheckbox = QtWidgets.QCheckBox(self.groupBox)
        self.increasingClozeCheckbox.setObjectName("increasingClozeCheckbox")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.ItemRole.FieldRole, self.increasingClozeCheckbox)
        self.clozeHintCheckBox = QtWidgets.QCheckBox(self.groupBox)
        self.clozeHintCheckBox.setWhatsThis("")
        self.clozeHintCheckBox.setObjectName("clozeHintCheckBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.LabelRole, self.clozeHintCheckBox)
        self.clozeHintCharSpinBox = QtWidgets.QSpinBox(self.groupBox)
        self.clozeHintCharSpinBox.setWhatsThis("")
        self.clozeHintCharSpinBox.setObjectName("clozeHintCharSpinBox")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.ItemRole.FieldRole, self.clozeHintCharSpinBox)
        self.formLayout_2.setWidget(3, QtWidgets.QFormLayout.ItemRole.SpanningRole, self.groupBox)
        self.processButton = QtWidgets.QPushButton(Dialog)
        self.processButton.setObjectName("processButton")
        self.formLayout_2.setWidget(4, QtWidgets.QFormLayout.ItemRole.FieldRole, self.processButton)
        self.separatePhrasesCheckBox = QtWidgets.QCheckBox(Dialog)
        self.separatePhrasesCheckBox.setObjectName("separatePhrasesCheckBox")
        self.formLayout_2.setWidget(1, QtWidgets.QFormLayout.ItemRole.LabelRole, self.separatePhrasesCheckBox)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.searchFieldComboBox, self.highlightFieldComboBox)
        Dialog.setTabOrder(self.highlightFieldComboBox, self.processButton)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label_5.setText(_translate("Dialog", "Search field"))
        self.label_6.setText(_translate("Dialog", "Highlight/Cloze field"))
        self.groupBox.setTitle(_translate("Dialog", "Operation"))
        self.highlightCheckBox.setText(_translate("Dialog", "Highlight"))
        self.clozeCheckbox.setText(_translate("Dialog", "Cloze"))
        self.increasingClozeCheckbox.setText(_translate("Dialog", "Increasing cloze numbers"))
        self.clozeHintCheckBox.setToolTip(_translate("Dialog", "Cloze words in the cloze field"))
        self.clozeHintCheckBox.setText(_translate("Dialog", "Cloze Hint"))
        self.clozeHintCharSpinBox.setToolTip(_translate("Dialog", "The number of characters to reveal in each word"))
        self.processButton.setText(_translate("Dialog", "Process"))
        self.separatePhrasesCheckBox.setText(_translate("Dialog", "Treat * as a separator for search phrases in search field"))
