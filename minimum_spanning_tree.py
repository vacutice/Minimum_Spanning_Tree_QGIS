# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MinimumSpanningTree
                                 A QGIS plugin
 This plugin finds the Minimum Spanning Tree of an input polygon shp file using Kruskal's algorithm.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2019-05-24
        git sha              : $Format:%H$
        copyright            : (C) 2019 by Abdurrahman Serhan, Berk Anbaroğlu / Hacettepe University
        email                : samiselim1212@hotmail.com, banbar@hacettepe.edu.tr
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt5.QtCore import QSettings, QTranslator, qVersion, QCoreApplication, QVariant
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QFileDialog
from qgis.core import *

# Initialize Qt resources from file resources.py
from .resources import *
# Import the code for the dialog
from .minimum_spanning_tree_dialog import MinimumSpanningTreeDialog
import os.path

# Disjoint Set Class Node and Functions (MakeSet, Union and Find)
class Node:
    def __init__(self, data):
        self.data = data

    def __str__(self):
        return self.label

def MakeSet(x):
    x.parent = x
    x.rank = 0


def Union(x, y):
    xRoot = Find(x)
    yRoot = Find(y)
    if xRoot.rank > yRoot.rank:
        yRoot.parent = xRoot
    elif xRoot.rank < yRoot.rank:
        xRoot.parent = yRoot
    elif xRoot != yRoot:  # Unless x and y are already in same set, merge them
        yRoot.parent = xRoot
        xRoot.rank = xRoot.rank + 1


def Find(x):
    if x.parent == x:
        return x
    else:
        x.parent = Find(x.parent)
        return x.parent





class MinimumSpanningTree:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        self.inFile = ''
        self.inFiles = ''
        self.activelayer = "" # set my active layer to null at the
        """Constructor.
        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface
        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'mst_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # this line for add the GUI and use its tools it ex: combobox, button,... is general named as self.dlg
        # in is takr the name of class and after it we write Dialog()
        self.dlg = MinimumSpanningTreeDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&Minimum Spanning Tree')

        self.toolbar = self.iface.addToolBar(u'Minimum Spanning Tree')
        self.toolbar.setObjectName(u'Minimum Spanning Tree')


    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('MinimumSpanningTree', message)


    def add_action(
        self,
        icon_path,
        text,
        callback,
        enabled_flag=True,
        add_to_menu=True,
        add_to_toolbar=True,
        status_tip=None,
        whats_this=None,
        parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            # Adds plugin icon to Plugins toolbar
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToVectorMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/minimum_spanning_tree/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'Minimum Spanning Tree'),
            callback=self.run,
            parent=self.iface.mainWindow())

        self.dlg.open_shpe_files.clicked.connect(self.openShpFile)


    # this methods will open file browser and load data to QGIS
    def openShpFile(self):  # vectors data
        if self.inFile is not None and self.dlg.entryshpfile.text() == '':  # if our file dose not none
            self.inFile = str(QFileDialog.getOpenFileName(caption="open shapefile"
                                                          , filter="shapefiles (*.shp)")[0])
            self.inFiles = self.inFile
            # we add vector data to my QGIS
            # self.iface is to connecting our plugin to QGIS and make change on qgis gui
            self.iface.addVectorLayer(self.inFile, str.split(os.path.basename(self.inFile), ".")[0], "ogr")
            # give the name of my layer to not loop when ever i need it
            self.my_layer = str.split(os.path.basename(self.inFile), ".") [0]
            self.setUsingLayer(self.my_layer)  # set my layer name.

            self.setVectorsToEntry(self.inFile)# this for show the file path in the edit line in plugin's gui
        elif self.dlg.entryshpfile.text() != '' :
            inFile = self.dlg.entryshpfile.text()
            self.iface.addVectorLayer(inFile, str.split(os.path.basename(inFile), ".")[0], "ogr")
            # give the name of my layer to not loop when ever i need it
            self.my_layer = str.split(os.path.basename(inFile), ".")[0]
            self.setUsingLayer(self.my_layer)  # set my layer name.
            self.setVectorsToEntry(inFile)  # this for show the file path in the edit line in plugin's gui

    # this function is for show what ever is choose by the user for shp file
    # so the user will see the file path that choose
    def setVectorsToEntry(self, text):
        self.dlg.entryshpfile.setText(text)

    # set my layer to make change on it. to do not loop all vector data more then one time
    def setUsingLayer(self, name):
        layers = [layer for layer in QgsProject.instance().mapLayers().values()]
        for layer in layers:
            # if the name of my added layer is equal to layer name set my layer.
            if layer.type() == QgsMapLayer.VectorLayer and layer.name() == name:
                self.activelayer = layer
                break

    # this part of the code it to draw line between centers in shape file
    def draw_line(self):
        self.all_edge_list = []
        layer = self.activelayer
        epsg = layer.crs().postgisSrid()
        iter = layer.getFeatures()  # get all the features in my shape file
        # new layer name and the data type of it data and where I would save it. so I save it on y ram
        uri = "LineString?crs=epsg:" + str(epsg) + "&field=id:integer""&index=yes"
        v_layer = QgsVectorLayer(uri, "line", "memory")
        pr = v_layer.dataProvider()  # make change on the new layers
        v_layer.startEditing()
        # the 3. part is for data type so if i live it as empty it will return the type that given in process
        # 4. the field length
        myField = QgsField("id", QVariant.Int, '', 0, 2)  # Note here the field type!
        dp = v_layer.dataProvider()
        dp.addAttributes([myField])
        myField2 = QgsField("neighbors_from", QVariant.Int, '', 1, 2)  # Note here the field type!
        dp.addAttributes([myField2])
        myField3 = QgsField("neighbors_to", QVariant.Int, '', 2, 2)  # Note here the field type!
        dp.addAttributes([myField3])
        myField3 = QgsField("cost", QVariant.Int, '', 3, 2)  # Note here the field type!
        dp.addAttributes([myField3])
        v_layer.updateFields()
        i = 0
        for feature in iter: # loop our features
            for feature1 in layer.getFeatures(): # loop the feature with them self again
                if feature.id() == feature1.id():  # to not take the same polygon
                    continue
                # if the geometry of two features are intersects take the first one as start point and the second
                # one as end point and draw line between them
                elif feature1.geometry().intersects(feature.geometry()) is True:
                    start = QgsPoint(feature.geometry().centroid().asPoint()[0],
                                     feature.geometry().centroid().asPoint()[1]) # X,Y of the point of the center
                    end = QgsPoint(feature1.geometry().centroid().asPoint()[0],
                                   feature1.geometry().centroid().asPoint()[1])
                    # add the geometry to the feature,
                    # create a new memory layer
                    # create a new feature
                    seg = QgsFeature()
                    seg.setGeometry(QgsGeometry.fromPolyline([start, end]))
                    # add the geometry to the layer
                    seg.setAttributes([i, feature1.id(), feature.id(),seg.geometry().length()])
                    pr.addFeatures([seg])
                    # update extent of the layer (not necessary)
                    v_layer.updateExtents()
                    v_layer.updateFeature(seg)
                    v_layer.commitChanges()
                    newEdge = [i, [feature1.id(),feature.id()], int(seg.geometry().length())]

                    self.all_edge_list.append(newEdge)
                    i += 1
        QgsProject.instance().addMapLayer(v_layer)

    # find the MST of our edges.
    def kruskal(self):
        # Initialize the list of vertices
        l_edges = []
        for polyID in range(len(self.all_points)):
            n1 = Node(polyID)
            l_edges.append(n1)

        edgesListSorted = sorted(self.all_edge_list, key=lambda l: l[2])
        self.all_edge_list = edgesListSorted
        del edgesListSorted

        # MakeSet for each of the vertex
        [MakeSet(node) for node in l_edges]

        # Resulting edge list - MST
        self.MST = [[]]
        total_cost = 0

        for edges in range(len(self.all_edge_list)):
            # Find the representative set of the edge
            root1 = Find(l_edges[self.all_edge_list[edges][1][0]])
            root2 = Find(l_edges[self.all_edge_list[edges][1][1]])
            # If both representative nodes are the same, then we form a cycle
            if(root1.data == root2.data):
                continue
            else:
                self.MST.append( [self.all_edge_list[edges][0], self.all_edge_list[edges][1]] )
                total_cost += self.all_edge_list[edges][2]
                Union(root1, root2)

        self.MST.pop(0)
        print("Cost: ", total_cost) # show total cost of our MST if needed

    # this part is for add the center of polygon in our shp file.
    def add_point(self):
        self.all_points = []
        layer = self.activelayer
        epsg = layer.crs().postgisSrid()
        # determine the layer project and the type of data
        uri = "Point?crs=epsg:" + str(epsg) + "&field=id:integer""&index=yes"
        mem_layer = QgsVectorLayer(uri,
                                   'point',
                                   'memory')
        prov = mem_layer.dataProvider()
        i = 0
        for f in layer.getFeatures():
            self.all_points.append(i)
            feat = QgsFeature()
            # get the geometry and get the center of them as point (x,y)
            pt = f.geometry().centroid().asPoint()
            feat.setAttributes([i])  # we can add the features that we want to attribute table
            feat.setGeometry(QgsGeometry.fromPointXY(pt)) # the geometry that we will add to new row in shape file
            prov.addFeatures([feat]) # add one ore row to my shape file
            i += 1
        QgsProject.instance().addMapLayer(mem_layer) # we add the layer to my qgsi and show it

# draw MST by using kruskal
    def draw_MST(self):
        # comment part is for add the prıject type of new added layer.
        epsg = self.activelayer.crs().postgisSrid()
        # new layer name and the data type of it data and where I would save it. so I save it on y ram
        uri = "LineString?crs=epsg:" + str(epsg) + "&field=id:integer""&index=yes"
        v_layer = QgsVectorLayer(uri, "MST", "memory")
        self.setUsingLayer('line')
        layer = self.activelayer
        pr = v_layer.dataProvider()  # make change on the new layers
        v_layer.startEditing()
        myField = QgsField("id", QVariant.Int, '', 0, 2)
        dp = v_layer.dataProvider()
        dp.addAttributes([myField])
        myField1 = QgsField("cost", QVariant.Int, '', 1, 2)
        dp = v_layer.dataProvider()
        dp.addAttributes([myField1])
        for edge in self.MST:
            for feature in layer.getFeatures():  # loop our features
                if feature[0] == edge[0]:  # to not take the same polygon
                    seg = QgsFeature()
                    seg.setGeometry(feature.geometry())
                    seg.setAttributes([feature.id(), feature.geometry().length()])
                    pr.addFeatures([seg])
                    v_layer.updateExtents()
                    v_layer.updateFeature(seg)
                    v_layer.commitChanges()

        QgsProject.instance().addMapLayer(v_layer)





    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginVectorMenu(
                self.tr(u'&Minimum Spanning Tree'),
                action)
            self.iface.removeToolBarIcon(action)



    def run(self):
        """Run method that performs all the real work"""
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            if self.dlg.entryshpfile.text() != '' and self.inFiles == '':
                self.inFiles =  self.dlg.entryshpfile.text()
                self.openShpFile()
            self.add_point()  # get all the centers of polygons
            self.draw_line()  # draw lien between then neighbor polygon
            self.kruskal()    # solve edges to find MST by using Kurskal
            self.draw_MST()   # draw MST.