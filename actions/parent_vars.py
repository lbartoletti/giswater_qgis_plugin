from ..core.actions.edit.layer_tools import GwLayerTools
from .. import global_vars


feature_id = None
snapper_manager = None
snapper = None
vertex_marker = None
rubber_polygon = None
add_layer = None
temp_layers_added = None
rubber_point = None
user_current_layer = None
list_update = None

# parent_manage.py
plan_om = None
ids = None
list_ids = None
layers = None
remove_ids = None
lazy_widget = None
lazy_init_function = None
geom_type = None

def init_global_vars():
	global add_layer
	add_layer = GwLayerTools()