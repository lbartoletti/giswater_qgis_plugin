"""
This file is part of Giswater 3
The program is free software: you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation, either version 3 of the License,
or (at your option) any later version.
"""
# -*- coding: utf-8 -*-
from qgis.PyQt.QtCore import QDate
from qgis.PyQt.QtWidgets import QDateEdit, QPushButton

from datetime import datetime
from functools import partial

from lib import qt_tools
from ..parent_action import GwParentAction
from ...utils.giswater_tools import close_dialog, load_settings, open_dialog
from ....ui_manager import SelectorDate
from ....actions.parent_functs import refresh_map_canvas


class GwDateSelectorButton(GwParentAction):

    def __init__(self, icon_path, text, toolbar, action_group):
        super().__init__(icon_path, text, toolbar, action_group)


    def clicked_event(self):

        self.dlg_selector_date = SelectorDate()
        load_settings(self.dlg_selector_date)
        self.widget_date_from = self.dlg_selector_date.findChild(QDateEdit, "date_from")
        self.widget_date_to = self.dlg_selector_date.findChild(QDateEdit, "date_to")
        self.dlg_selector_date.findChild(QPushButton, "btn_accept").clicked.connect(self.update_dates_into_db)
        self.dlg_selector_date.btn_close.clicked.connect(partial(close_dialog, self.dlg_selector_date))
        self.dlg_selector_date.rejected.connect(partial(close_dialog, self.dlg_selector_date))
        self.widget_date_from.dateChanged.connect(partial(self.update_date_to))
        self.widget_date_to.dateChanged.connect(partial(self.update_date_from))

        self.get_default_dates()
        qt_tools.setCalendarDate(self.dlg_selector_date, self.widget_date_from, self.from_date)
        qt_tools.setCalendarDate(self.dlg_selector_date, self.widget_date_to, self.to_date)
        open_dialog(self.dlg_selector_date, dlg_name="selector_date")


    def update_dates_into_db(self):
        """ Insert or update dates into data base """

        # Set project user
        self.current_user = self.controller.get_project_user()

        from_date = self.widget_date_from.date().toString('yyyy-MM-dd')
        to_date = self.widget_date_to.date().toString('yyyy-MM-dd')
        sql = (f"SELECT * FROM selector_date"
               f" WHERE cur_user = '{self.current_user}'")
        row = self.controller.get_row(sql)
        if not row:
            sql = (f"INSERT INTO selector_date"
                   f" (from_date, to_date, context, cur_user)"
                   f" VALUES('{from_date}', '{to_date}', 'om_visit', '{self.current_user}')")
        else:
            sql = (f"UPDATE selector_date"
                   f" SET (from_date, to_date) = ('{from_date}', '{to_date}')"
                   f" WHERE cur_user = '{self.current_user}'")

        self.controller.execute_sql(sql)

        close_dialog(self.dlg_selector_date)
        refresh_map_canvas()


    def update_date_to(self):
        """ If 'date from' is upper than 'date to' set 'date to' 1 day more than 'date from' """

        from_date = self.widget_date_from.date().toString('yyyy-MM-dd')
        to_date = self.widget_date_to.date().toString('yyyy-MM-dd')
        if from_date >= to_date:
            to_date = self.widget_date_from.date().addDays(1).toString('yyyy-MM-dd')
            qt_tools.setCalendarDate(self.dlg_selector_date, self.widget_date_to,
                                     datetime.strptime(to_date, '%Y-%m-%d'))


    def update_date_from(self):
        """ If 'date to' is lower than 'date from' set 'date from' 1 day less than 'date to' """

        from_date = self.widget_date_from.date().toString('yyyy-MM-dd')
        to_date = self.widget_date_to.date().toString('yyyy-MM-dd')
        if to_date <= from_date:
            from_date = self.widget_date_to.date().addDays(-1).toString('yyyy-MM-dd')
            qt_tools.setCalendarDate(self.dlg_selector_date, self.widget_date_from,
                                     datetime.strptime(from_date, '%Y-%m-%d'))


    def get_default_dates(self):
        """ Load the dates from the DB for the current_user and set vars (self.from_date, self.to_date) """

        # Set project user
        self.current_user = self.controller.get_project_user()

        sql = (f"SELECT from_date, to_date FROM selector_date"
               f" WHERE cur_user = '{self.current_user}'")
        row = self.controller.get_row(sql)
        try:
            if row:
                self.from_date = QDate(row[0])
                self.to_date = QDate(row[1])
            else:
                self.from_date = QDate.currentDate()
                self.to_date = QDate.currentDate().addDays(1)
        except:
            self.from_date = QDate.currentDate()
            self.to_date = QDate.currentDate().addDays(1)

