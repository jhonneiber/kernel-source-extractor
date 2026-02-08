#Decompile.py
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor
from java.io import File

# 1. Configurar el Descompilador
program = currentProgram
decomp = DecompInterface()
decomp.openProgram(program)
monitor = ConsoleTaskMonitor()

# 2. Definir dónde guardar el resultado
output_dir = "output_code"
# Asegurarse de que el directorio existe (se hace en el YAML, pero por seguridad)
import os
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

output_file_path = output_dir + "/kernel_dump.c"
f = open(output_file_path, "w")

print("--- INICIANDO DESCOMPILACIÓN MASIVA ---")
print("Este proceso puede tardar mucho dependiendo del tamaño del kernel...")

# 3. Iterar sobre todas las funciones encontradas
function_manager = program.getFunctionManager()
functions = function_manager.getFunctions(True) # True = forward direction

count = 0
for func in functions:
    # Opcional: Filtrar solo funciones que contengan "ili78" para ir al grano
    # if "ili78" not in func.getName():
    #     continue
    
    try:
        # Descompilar la función actual
        res = decomp.decompileFunction(func, 0, monitor)
        decompiled_code = res.getDecompiledFunction().getC()
        
        # Escribir en el archivo
        f.write("\n// Address: " + func.getEntryPoint().toString() + "\n")
        f.write("// Function: " + func.getName() + "\n")
        f.write(decompiled_code)
        f.write("\n---------------------------------------------------\n")
        
        count += 1
        if count % 100 == 0:
            print("Descompiladas: " + str(count) + " funciones.")
            
    except Exception as e:
        f.write("\n// Error descompilando " + func.getName() + "\n")
        print("Error en: " + func.getName())

f.close()
print("--- FIN ---")
print("Total funciones exportadas: " + str(count))
