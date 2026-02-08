# Decompile.py - Versión Optimizada para GitHub Actions
from ghidra.app.decompiler import DecompInterface
from ghidra.util.task import ConsoleTaskMonitor
from java.io import File
import os

# --- CONFIGURACIÓN ---
# Palabras clave para filtrar. 
# Si la función contiene alguna de estas, se guarda. 
# Esto es VITAL para no superar el límite de 6 horas de GitHub.
KEYWORDS = ["ili78", "lcm", "dsi", "panel", "display", "mtk_disp", "videolfb"]

OUTPUT_DIR = "output_code"
OUTPUT_FILE = "kernel_drivers_dump.c"

# ---------------------

print("--- INICIANDO SCRIPT DE GIDRA OPTIMIZADO ---")

# 1. Preparar Entorno
program = currentProgram
decomp = DecompInterface()
decomp.openProgram(program)
monitor = ConsoleTaskMonitor()

if not os.path.exists(OUTPUT_DIR):
    os.makedirs(OUTPUT_DIR)

full_path = OUTPUT_DIR + "/" + OUTPUT_FILE
f = open(full_path, "w")

# Escribir cabecera
f.write("/* \n")
f.write(" * DUMP DEL KERNEL - MODULOS DE PANTALLA \n")
f.write(" * Generado automaticamente por Ghidra Headless \n")
f.write(" */\n\n")

# 2. Obtener funciones
function_manager = program.getFunctionManager()
# Iterar en orden de memoria para mantener cierta coherencia
functions = function_manager.getFunctions(True) 

print("Analizando funciones en busca de drivers de pantalla...")

count_total = 0
count_saved = 0

for func in functions:
    count_total += 1
    func_name = func.getName()
    
    # 3. FILTRO: ¿Es esta función relevante?
    # Convertimos a minúsculas para comparar
    name_lower = func_name.lower()
    
    is_interesting = False
    for k in KEYWORDS:
        if k in name_lower:
            is_interesting = True
            break
    
    # Si no tiene las palabras clave, saltamos a la siguiente (Ahorra MUCHO tiempo)
    if not is_interesting:
        continue

    # 4. Descompilar
    try:
        # Timeout de 5 segundos por función para que no se cuelgue
        res = decomp.decompileFunction(func, 5, monitor)
        
        if not res.decompileCompleted():
            f.write("\n// Error: No se pudo completar descompilacion de " + func_name + "\n")
            continue
            
        decompiled_func = res.getDecompiledFunction()
        if decompiled_func is None:
            continue
            
        c_code = decompiled_func.getC()
        
        if c_code:
            f.write("\n// =======================================================\n")
            f.write("// Function: " + func_name + "\n")
            f.write("// Address:  " + func.getEntryPoint().toString() + "\n")
            f.write("// =======================================================\n")
            f.write(c_code)
            f.write("\n")
            
            count_saved += 1
            print("[GUARDADO] " + func_name)
            
    except Exception as e:
        print("Excepcion procesando " + func_name)

    # Reporte de progreso cada 10,000 funciones analizadas (no guardadas)
    if count_total % 10000 == 0:
        print("Escaneadas: " + str(count_total) + " | Guardadas: " + str(count_saved))

f.close()
print("--- FIN DEL PROCESO ---")
print("Total funciones analizadas: " + str(count_total))
print("Total funciones de pantalla guardadas: " + str(count_saved))
print("Archivo guardado en: " + full_path)
