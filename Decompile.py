# Script para Ghidra
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor
import os

def run():
    program = getCurrentProgram()
    ifc = DecompInterface()
    ifc.openProgram(program)
    
    output_dir = "output_code"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Recorrer todas las funciones y guardarlas como archivos .c
    function = getFirstFunction()
    while function is not None:
        res = ifc.decompileFunction(function, 0, ConsoleTaskMonitor())
        with open(os.path.join(output_dir, function.getName() + ".c"), "w") as f:
            f.write(res.getDecompiledFunction().getC())
        function = getFunctionAfter(function)

run()