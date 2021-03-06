"""
This file is part of Giswater 3
The program is free software: you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation, either version 3 of the License,
or (at your option) any later version.
"""
# -*- coding: utf-8 -*-
from qgis.core import QgsMapToPixel
from qgis.gui import QgsVertexMarker
from qgis.PyQt.QtCore import Qt
from qgis.PyQt.QtGui import QDoubleValidator

from functools import partial

from lib import qt_tools
from .... import global_vars
from ..parent_maptool import GwParentMapTool
from ....ui_manager import AuxPoint
from ...utils.giswater_tools import close_dialog, get_parser_value, load_settings, open_dialog, set_parser_value
from ....lib.qgis_tools import get_event_point, snap_to_current_layer, snap_to_background_layers, add_marker, \
    get_snapping_options, get_snapped_point


class GwAuxPointButton(GwParentMapTool):
    """ Button 72: Add point """

    def __init__(self, icon_path, text, toolbar, action_group):
        """ Class constructor """

        super().__init__(icon_path, text, toolbar, action_group)
        self.vertex_marker.setIconType(QgsVertexMarker.ICON_CROSS)
        self.cancel_point = False
        self.layer_points = None
        self.point_1 = None
        self.point_2 = None
        self.snap_to_selected_layer = False


    def init_create_point_form(self, point_1=None, point_2=None):

        # Create the dialog and signals
        self.dlg_create_point = AuxPoint()
        load_settings(self.dlg_create_point)

        validator = QDoubleValidator(-99999.99, 99999.999, 3)
        validator.setNotation(QDoubleValidator().StandardNotation)
        self.dlg_create_point.dist_x.setValidator(validator)
        validator = QDoubleValidator(-99999.99, 99999.999, 3)
        validator.setNotation(QDoubleValidator().StandardNotation)
        self.dlg_create_point.dist_y.setValidator(validator)
        self.dlg_create_point.dist_x.setFocus()
        self.dlg_create_point.btn_accept.clicked.connect(partial(self.get_values, point_1, point_2))
        self.dlg_create_point.btn_cancel.clicked.connect(self.cancel)

        if get_parser_value('cadtools', f"{self.dlg_create_point.rb_left.objectName()}") == 'True':
            self.dlg_create_point.rb_left.setChecked(True)
        else:
            self.dlg_create_point.rb_right.setChecked(True)

        open_dialog(self.dlg_create_point, dlg_name='auxpoint', maximize_button=False)


    def get_values(self, point_1, point_2):
        set_parser_value('cadtools', f"{self.dlg_create_point.rb_left.objectName()}",
                         f"{self.dlg_create_point.rb_left.isChecked()}")

        self.dist_x = self.dlg_create_point.dist_x.text()
        if not self.dist_x:
            self.dist_x = 0
        self.dist_y = self.dlg_create_point.dist_y.text()
        if not self.dist_y:
            self.dist_y = 0

        self.delete_prev = qt_tools.isChecked(self.dlg_create_point, self.dlg_create_point.chk_delete_prev)
        if self.layer_points:
            self.layer_points.startEditing()
            close_dialog(self.dlg_create_point)
            if self.dlg_create_point.rb_left.isChecked():
                self.direction = 1
            else:
                self.direction = 2

            sql = f"SELECT ST_GeomFromText('POINT({point_1[0]} {point_1[1]})', {self.srid})"
            row = self.controller.get_row(sql)
            point_1 = row[0]
            sql = f"SELECT ST_GeomFromText('POINT({point_2[0]} {point_2[1]})', {self.srid})"
            row = self.controller.get_row(sql)
            point_2 = row[0]

            sql = (f"SELECT gw_fct_cad_add_relative_point "
                   f"('{point_1}', '{point_2}', {self.dist_x}, "
                   f"{self.dist_y}, {self.direction}, {self.delete_prev})")
            self.controller.execute_sql(sql)
            self.layer_points.commitChanges()
            self.layer_points.dataProvider().forceReload()
            self.layer_points.triggerRepaint()

        else:
            self.iface.actionPan().trigger()
            self.cancel_point = False
            return


    def cancel(self):

        set_parser_value('cadtools', f"{self.dlg_create_point.rb_left.objectName()}",
                         f"{self.dlg_create_point.rb_left.isChecked()}")

        close_dialog(self.dlg_create_point)
        self.iface.setActiveLayer(self.current_layer)
        if self.layer_points:
            if self.layer_points.isEditable():
                self.layer_points.commitChanges()
        self.cancel_point = True
        self.cancel_map_tool()


    """ QgsMapTools inherited event functions """

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_Escape:
            self.cancel_map_tool()
            self.iface.setActiveLayer(self.current_layer)
            return


    def canvasMoveEvent(self, event):

        # Hide highlight and get coordinates
        self.vertex_marker.hide()
        event_point = get_event_point(event)

        # Snapping
        if self.snap_to_selected_layer:
            result = snap_to_current_layer(event_point)
        else:
            result = snap_to_background_layers(event_point)

        if result.isValid():
            # Get the point and add marker on it
            add_marker(result, self.vertex_marker)


    def canvasReleaseEvent(self, event):

        if event.button() == Qt.LeftButton:

            # Get coordinates
            x = event.pos().x()
            y = event.pos().y()
            event_point = get_event_point(event)

            # Create point with snap reference
            result = snap_to_background_layers(event_point)
            point = None
            if result.isValid():
                point = get_snapped_point(result)

            # Create point with mouse cursor reference
            if point is None:
                point = QgsMapToPixel.toMapCoordinates(self.canvas.getCoordinateTransform(), x, y)

            if self.point_1 is None:
                self.point_1 = point
            else:
                self.point_2 = point

            if self.point_1 is not None and self.point_2 is not None:
                self.init_create_point_form(self.point_1, self.point_2)

        elif event.button() == Qt.RightButton:
            self.cancel_map_tool()
            self.iface.setActiveLayer(self.current_layer)

        if self.layer_points:
            self.layer_points.commitChanges()


    def activate(self):

        self.snap_to_selected_layer = False
        # Get SRID
        self.srid = global_vars.srid

        # Check button
        self.action.setChecked(True)

        # Change cursor
        self.canvas.setCursor(self.cursor)

        # Show help message when action is activated
        if self.show_help:
            message = "Click two points over canvas and draw a line"
            self.controller.show_info(message)

        # Store user snapping configuration
        self.previous_snapping = get_snapping_options()

        # Get current layer
        self.current_layer = self.iface.activeLayer()

        self.layer_points = self.controller.get_layer_by_tablename('v_edit_cad_auxpoint')
        if self.layer_points is None:
            self.controller.show_warning("Layer not found", parameter='v_edit_cad_auxpoint')
            self.cancel_map_tool()
            self.iface.setActiveLayer(self.current_layer)
            return

        # Check for default base layer
        self.vdefault_layer = None
        row = self.controller.get_config('edit_cadtools_baselayer_vdefault')
        if row:
            self.snap_to_selected_layer = True
            self.vdefault_layer = self.controller.get_layer_by_tablename(row[0], True)
            if self.vdefault_layer:
                self.iface.setActiveLayer(self.vdefault_layer)

        if self.vdefault_layer is None:
            self.vdefault_layer = self.iface.activeLayer()


    def deactivate(self):

        self.point_1 = None
        self.point_2 = None

        # Call parent method
        super().deactivate()
        self.iface.setActiveLayer(self.current_layer)

