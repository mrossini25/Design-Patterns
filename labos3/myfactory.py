from importlib import import_module

def myfactory(moduleName):
    module = import_module(f'plugins.{moduleName}')
    return getattr(module, moduleName.capitalize())