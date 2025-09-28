import torch as th
from ..base import BaseNode, InputSocket, OutputSocket, Connection
from ..expr_node import GLNode
from ..simple_registry import register_node, register_node_decorator
# import splitweaver.symbolic as sws


@register_node_decorator
class EvaluateLayoutNode(BaseNode):
    """
    Key Idea: Layout Expression -> Grid and Grid Ids
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    
    def setup_sockets(self):
        self.input_sockets = {
            "expr": InputSocket("expr", parent=self),
            "seed": InputSocket("seed", parent=self),
            "normalization_mode": InputSocket("normalization_mode", parent=self, value=0),
            "center_x": InputSocket("center_x", parent=self, value=0),
            "center_y": InputSocket("center_y", parent=self, value=0),

        }
        self.output_sockets = {
            "grid": OutputSocket("grid", parent=self),
            "grid_ids": OutputSocket("grid_ids", parent=self),
        }
    
    def __new__(cls, *args, **kwargs):
        # Create the node instance using the default constructor
        instance = super(EvaluateLayoutNode, cls).__new__(cls)

        # After setting up sockets in BaseNode, now handle connections
        for arg in args:
            if isinstance(arg, GLNode):
                Connection(input_node=arg, input_socket="expr", output_node=instance, output_socket="expr")
            else:
                raise ValueError("What to do here?")
        
        # Handle keyword arguments (for params like width, height)
        for key, value in kwargs.items():
            if isinstance(value, (GLNode)):
                Connection(input_node=value, input_socket=key, output_node=instance, output_socket="expr")
            elif isinstance(value, OutputSocket):
                node = value.parent
                Connection(input_node=node, output_socket=value.name, output_node=instance, input_socket=key)
            else:
                instance.input_sockets[key].set_value(value)

        return instance

    def setup_base(self):
        self.arg_keys = ['expr', 'grid']
        self.default_values = {}
    def inner_eval(self, sketcher=None, **kwargs):
        expr = self.inputs.get('expr', None)
        # if its a GL Node, then we don't want to evlauate it fully
        seed = self.inputs.get('seed', None)
        normalization_mode = self.inputs.get('normalization_mode', None)
        # TODO: Instead -> send different expressions to the output.
        # Or send Memoised output. 
        if normalization_mode == 2:
            center_x = self.inputs.get('center_x', None)
            center_y = self.inputs.get('center_y', None)
        #############
        if seed is not None:
            with th.random.fork_rng():
                th.manual_seed(seed)
                grid, grid_ids = grid_eval(expr.tensor(), sketcher, grid=None)
        else:
            grid, grid_ids = grid_eval(expr.tensor(), sketcher, grid=None)

        if normalization_mode == 1:
            simple_grid, _ = grid_eval(gs.CartesianGrid().tensor(), sketcher, grid=None)
            grid = voronoi_style_normalize(grid_ids, simple_grid, simple_grid)
        elif normalization_mode == 2:
            # need to get the center from somewhere
            center = (center_x, center_y)
            simple_grid, _ = grid_eval(gs.CartesianGrid().tensor(), sketcher, grid=None)
            grid = voronoi_style_normalize(grid_ids, simple_grid, simple_grid, minfit=False, rotate=True, center=center)
        ############
        grid, grid_ids = grid_eval(expr.tensor(), sketcher)

        self.register_output("grid", grid)
        self.register_output("grid_ids", grid_ids)

