import ast
import marshal
import os
import sys
import imp
import struct
import time
from types import ModuleType

from . import lexer


def parse(text):
    psr = lexer.prep()
    sequence = psr.parse(text)
    mod = ast.Module(sequence)
    ast.fix_missing_locations(mod)
    return mod


def execute(mod):
    return exec(compile(mod, "<ast>", "exec"))


def eval(text):
    return execute(parse(text))


def load_hio(module_path):
    ext = module_path.split(".")[-1]
    filename = os.path.basename(module_path)
    module = filename[-len(ext):]
    with open(module_path, 'r') as rf:
        text = rf.read()
    mtree = parse(text)
    mod = ModuleType(module)
    mod.__file__ = module_path
    compiled = compile(mtree, filename, "exec")
    exec(compiled, mod.__dict__, mod.__dict__)
    sys.modules[module] = mod
    return mod


def compile_hio(module_path, d):
    ext = module_path.split(".")[-1]
    filename = os.path.basename(module_path)
    module = filename[:-len(ext) - 1]
    with open(module_path, 'r') as rf:
        text = rf.read()

    mtree = parse(text)
    compiled = compile(mtree, filename, "exec")

    with open(f"{module}.pyc", 'wb') as cf:
        cf.write(imp.util.MAGIC_NUMBER)
        cf.write(hex(int(time.time()))[2:].encode())
        marshal.dump(compiled, cf)