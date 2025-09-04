# global_registry.py
DAG_SYMBOL_REGISTRY = {}

def register_symbol(cls):
    DAG_SYMBOL_REGISTRY[cls.__name__] = cls
    return cls