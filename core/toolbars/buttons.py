"""
This file is part of Giswater 3
The program is free software: you can redistribute it and/or modify it under the terms of the GNU
General Public License as published by the Free Software Foundation, either version 3 of the License,
or (at your option) any later version.
"""
# -*- coding: utf-8 -*-

# Basic
from .basic.btn_info import GwInfoButton
from .basic.btn_search import GwSearchButton
from .basic.btn_selector import GwSelectorButton

# Om
from .om.btn_mincut import GwMincutButton
from .om.btn_mincut_manager import GwMincutManagerButton

from .om.btn_flow_trace import GwFlowTraceButton
from .om.btn_flow_exit import GwFlowExitButton

from .om.btn_profile import GwProfileButton
from .om.btn_add_visit import GwAddVisitButton
from .om.btn_manage_visit import GwManageVisitButton
from .om.btn_date_selector import GwDateSelectorButton

# Edit
from .edit.btn_add_point import GwAddPointButton
from .edit.btn_add_line import GwAddLineButton
from .edit.btn_feature_replace import GwFeatureReplaceButton
from .edit.btn_arc_divide import GwArcDivideButton
from .edit.btn_arc_fusion import GwArcFusionButton
from .edit.btn_nodetype_change import GwNodeTypeChangeButton
from .edit.btn_connect_link import GwConnectLinkButton
from .edit.btn_end_feature import GwEndFeatureButton
from .edit.btn_delete_feature import GwDeleteFeatureButton
from .edit.btn_dimensioning import GwDimensioningButton
from .edit.btn_add_document import GwAddDocumentButton
from .edit.btn_edit_document import GwEditDocumentButton
from .edit.btn_add_element import GwAddElementButton
from .edit.btn_edit_element import GwEditElementButton

# Cad
from .cad.btn_aux_circle import GwAuxCircleButton
from .cad.btn_aux_point import GwAuxPointButton

# Epa
from .epa.btn_go2epa import GwGo2EpaButton
from .epa.btn_go2epa_manager import GwGo2EpaManagerButton
from .epa.btn_go2epa_selector import GwGo2EpaSelectorButton

# Plan
from .plan.btn_psector import GwPsectorButton
from .plan.btn_psector_manager import GwPsectorManagerButton
from .plan.btn_price_manager import GwPriceManagerButton

# Utilities
from .utilities.btn_toolbox import GwToolBoxButton
from .utilities.btn_config import GwConfigButton
from .utilities.btn_csv import GwCSVButton
from .utilities.btn_print import GwPrintButton
from .utilities.btn_project_check import GwProjectCheckButton

# ToC
from .toc.btn_add_child_layer import GwAddChildLayerButton
