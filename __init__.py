# -*- coding: utf-8 -*-
"""
/***************************************************************************
 MinimumSpanningTree
                                 A QGIS plugin
 This plugin finds the Minimum Spanning Tree of an input polygon shp file using Kruskal's algorithm.
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2019-05-24
        copyright            : (C) 2019 by Abdurrahman Serhan, Berk Anbaroğlu / Hacettepe University 
        email                : samiselim1212@hotmail.com, banbar@hacettepe.edu.tr
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load MinimumSpanningTree class from file MinimumSpanningTree.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .minimum_spanning_tree import MinimumSpanningTree
    return MinimumSpanningTree(iface)
