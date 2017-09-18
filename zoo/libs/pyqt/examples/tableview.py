from qt import QtWidgets
from zoo.libs import iconlib
from zoo.libs.pyqt.extended import tableviewplus
from zoo.libs.pyqt.models import datasources
from zoo.libs.pyqt.models import tablemodel
from zoo.libs.pyqt.widgets import dialog


class TableViewExample(dialog.Dialog):
    def __init__(self, title="Tableview example", width=600, height=800, icon="", parent=None, showOnInitialize=True):
        super(TableViewExample, self).__init__(title, width, height, icon, parent, showOnInitialize)

        self.mainLayout = QtWidgets.QVBoxLayout(self)
        self.view = tableviewplus.TableViewPlus(True, parent=self)
        self.mainLayout.addWidget(self.view)
        self.setLayout(self.mainLayout)
        self.qmodel = tablemodel.TableModel(parent=self)
        self.view.setModel(self.qmodel)
        self.rowDataSource = ExampleRowDataSource([Node("one"), Node("Two"), Node("Three")])
        self.columnDataSources = (ExampleColumnIntDataSource(), ExampleColumnEnumerationDataSource())
        self.view.registerRowDataSource(self.rowDataSource)
        self.view.registerColumnDataSources(self.columnDataSources)
        self.qmodel.reload()
        self.view.refresh()


class Node(object):
    def __init__(self, label):
        self.label = label
        self.dataField = 10
        self.icon = iconlib.icon("brick")
        self.values = ["translate", "rotate", "scale", "visibility"]
        self.currentIndex = 0


class ExampleRowDataSource(datasources.BaseDataSource):
    def __init__(self, nodes):
        super(ExampleRowDataSource, self).__init__()
        self.nodes = nodes

    def headerText(self, index):
        """see base class for doc
        """
        return "rowHeader"

    def rowCount(self):
        return len(self.nodes)

    def icon(self, index):
        if index in range(self.rowCount()):
            return self.nodes[index].icon

    def data(self, index):
        if index in xrange(self.rowCount()):
            return self.nodes[index].label

    def setData(self, index, value):
        if index in xrange(self.rowCount()):
            self.nodes[index].label = value

    def userObject(self, index):
        if index in xrange(self.rowCount()):
            return self.nodes[index]


class ExampleColumnIntDataSource(datasources.BaseDataSource):
    def headerText(self, index):
        """see base class for doc
        """
        return "column spinbox"

    def data(self, rowDataSource, index):
        node = rowDataSource.userObject(index)
        if node:
            return node.dataField

    def setData(self, rowDataSource, index, value):
        node = rowDataSource.userObject(index)
        if node:
            node.dataField = int(value)

    def isEnabled(self, rowDataSource, index):
        return True

    def isEditable(self, rowDataSource, index):
        return True

    def isSelectable(self, rowDataSource, index):
        return True


class ExampleColumnEnumerationDataSource(datasources.ColumnEnumerationDataSource):
    def __init__(self):
        super(ExampleColumnEnumerationDataSource, self).__init__()

    def headerText(self, index):
        """see base class for doc
        """
        return "column combobox"

    def enums(self, rowDataSource, index):
        node = rowDataSource.userObject(index)
        if node:
            return node.values

    def data(self, rowDataSource, index):
        node = rowDataSource.userObject(index)
        if node:
            return node.values[node.currentIndex]

    def setData(self, rowDataSource, index, value):
        node = rowDataSource.userObject(index)
        if node:
            node.currentIndex = int(value)

    def isEnabled(self, rowDataSource, index):
        return True

    def isEditable(self, rowDataSource, index):
        return True

    def isSelectable(self, rowDataSource, index):
        return True
