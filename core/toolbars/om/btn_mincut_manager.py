"""
This file is part of Giswater 3
The program is free software: you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation, either version 3 of the License,
or (at your option) any later version.
"""
# -*- coding: utf-8 -*-
from ..parent_action import GwParentAction
from ...actions.om.mincut import GwMincut


class GwMincutManagerButton(GwParentAction):

    def __init__(self, icon_path, text, toolbar, action_group):
        super().__init__(icon_path, text, toolbar, action_group)
        self.mincut = GwMincut()


    def clicked_event(self):
        self.mincut.mg_mincut_management()
