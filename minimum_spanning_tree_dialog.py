# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MinimumSpanningTreeDialog
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

import os

from PyQt5 import uic
from PyQt5 import QtWidgets

# This loads your .ui file so that PyQt can populate your plugin with the elements from Qt Designer
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'minimum_spanning_tree_dialog_base.ui'))


class MinimumSpanningTreeDialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(MinimumSpanningTreeDialog, self).__init__(parent)
        # Set up the user interface from Designer through FORM_CLASS.
        # After self.setupUi() you can access any designer object by doing
        # self.<objectname>, and you can use autoconnect slots - see
        # http://qt-project.org/doc/qt-4.8/designer-using-a-ui-file.html
        # #widgets-and-dialogs-with-auto-connect
        self.setupUi(self)
