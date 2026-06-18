
import csv
import os

RUTA_CSV = 'paises.csv'

# ==================== ARCHIVO.PY ====================
def crear_csv_base():
    """Crea el CSV con datos base si no existe."""
    datos_iniciales = [
        ['nombre', 'poblacion', 'superficie', 'continente'],
        ['Argentina', '45376763', '2780400', 'América'],
        ['Japón', '125800000', '377975', 'Asia'],
        ['Brasil', '213993437', '8515767', 'América'],
        ['Alemania', '83149300', '357022', 'Europa'],
        ['Nigeria', '223804632', '923768', 'África'],
        ['Australia', '26177413', '7692024', 'Oceanía'],
        ['Canadá', '40097761', '9984670', 'América'],
        ['Egipto', '112716598', '1010408', 'África'],
        ['Francia', '68373833', '643801', 'Europa'],
        ['India', '1428627663', '3287263', 'Asia']
    ]
    with open(RUTA_CSV, 'w', encoding='utf-8', newline='') as archivo:
        escritor = csv.writer(archivo)
        escritor.writerows(datos_iniciales)

def cargar_paises(ruta_csv):
    """Lee el CSV y devuelve una lista de diccionarios. Valida formato."""
    paises = []
    if not os.path.exists(ruta_csv):
        print(f"No se encontró {ruta_csv}. Creando archivo base...")
        crear_csv_base()

    try:
        with open(ruta_csv, 'r', encoding='utf-8') as archivo:
            lector = csv.DictReader(archivo)
            for i, fila in enumerate(lector, start=2):
                try:
                    pais = {
                        'nombre': fila['nombre'].strip(),
                        'poblacion': int(fila['poblacion']),
                        'superficie': int(fila['superficie']),
                        'continente': fila['continente'].strip()
                    }
                    if not all(pais.values()):
                        raise ValueError("Campo vacío detectado")
                    if pais['poblacion'] <= 0 or pais['superficie'] <= 0:
                        raise ValueError("Valores deben ser > 0")
                    paises.append(pais)
                except (ValueError, KeyError) as e:
                    print(f"Advertencia: Línea {i} omitida. Motivo: {e}")
        print(f"Éxito: Se cargaron {len(paises)} países.")
    except Exception as e:
        print(f"Error crítico al leer CSV: {e}")
    return paises

def guardar_paises(ruta_csv, paises):
    """Guarda la lista de países en el CSV."""
    try:
        with open(ruta_csv, 'w', encoding='utf-8', newline='') as archivo:
            campos = ['nombre', 'poblacion', 'superficie', 'continente']
            escritor = csv.DictWriter(archivo, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(paises)
        return True
    except Exception as e:
        print(f"Error al guardar: {e}")
        return False

# ==================== PAISES.PY ====================
def mostrar_tabla(paises):
    """Muestra países en formato tabla. Usado por varias funciones."""
    if not paises:
        print("No hay datos para mostrar.")
        return
    print(f"\n{'Nombre':<20} {'Población':>15} {'Superficie':>15} {'Continente':<15}")
    print("-" * 70)
    for p in paises:
        print(f"{p['nombre']:<20} {p['poblacion']:>15,} {p['superficie']:>15,} {p['continente']:<15}")

def agregar_pais(paises):
    """Solicita datos y agrega un país. No permite campos vacíos ni duplicados."""
    print("\n--- AGREGAR PAÍS ---")
    try:
        nombre = input("Nombre: ").strip()
        poblacion = input("Población: ").strip()
        superficie = input("Superficie km²: ").strip()
        continente = input("Continente: ").strip()

        if not nombre or not poblacion or not superficie or not continente:
            print("Error: Ningún campo puede estar vacío.")
            return False

        pais = {
            'nombre': nombre,
            'poblacion': int(poblacion),
            'superficie': int(superficie),
            'continente': continente
        }

        if pais['poblacion'] <= 0 or pais['superficie'] <= 0:
            print("Error: Población y superficie deben ser mayores a 0.")
            return False

        if any(p['nombre'].lower() == nombre.lower() for p in paises):
            print("Error: Ya existe un país con ese nombre.")
            return False

        paises.append(pais)
        print(f"Éxito: {nombre} agregado correctamente.")
        return True
    except ValueError:
        print("Error: Población y superficie deben ser números enteros.")
        return False

def actualizar_pais(paises):
    """Actualiza población y superficie de un país existente."""
    nombre = input("\nNombre del país a actualizar: ").strip()
    for pais in paises:
        if pais['nombre'].lower() == nombre.lower():
            try:
                nueva_pob = input(f"Nueva población [{pais['poblacion']}]: ").strip()
                nueva_sup = input(f"Nueva superficie [{pais['superficie']}]: ").strip()

                if nueva_pob:
                    pais['poblacion'] = int(nueva_pob)
                if nueva_sup:
                    pais['superficie'] = int(nueva_sup)

                if pais['poblacion'] <= 0 or pais['superficie'] <= 0:
                    print("Error: Los valores deben ser mayores a 0.")
                    return False

                print("Éxito: Datos actualizados.")
                return True
            except ValueError:
                print("Error: Debe ingresar números enteros.")
                return False
    print("Error: País no encontrado.")
    return False

def buscar_pais(paises):
    """Busca por coincidencia parcial o exacta. Case insensitive."""
    busqueda = input("\nIngrese nombre a buscar: ").strip().lower()
    if not busqueda:
        print("Error: Debe ingresar un texto para buscar.")
        return

    resultados = [p for p in paises if busqueda in p['nombre'].lower()]

    if resultados:
        print(f"\nSe encontraron {len(resultados)} países:")
        mostrar_tabla(resultados)
    else:
        print("Error: No se encontraron coincidencias.")

def filtrar_paises(paises):
    """Filtra por continente, rango de población o superficie."""
    print("\n--- FILTRAR ---")
    print("1. Por continente")
    print("2. Por rango de población")
    print("3. Por rango de superficie")
    op = input("Opción: ")

    filtrados = []
    try:
        if op == '1':
            cont = input("Continente: ").strip().lower()
            filtrados = [p for p in paises if p['continente'].lower() == cont]
        elif op == '2':
            min_p = int(input("Población mínima: "))
            max_p = int(input("Población máxima: "))
            if min_p > max_p:
                print("Error: El mínimo no puede ser mayor al máximo.")
                return
            filtrados = [p for p in paises if min_p <= p['poblacion'] <= max_p]
        elif op == '3':
            min_s = int(input("Superficie mínima: "))
            max_s = int(input("Superficie máxima: "))
            if min_s > max_s:
                print("Error: El mínimo no puede ser mayor al máximo.")
                return
            filtrados = [p for p in paises if min_s <= p['superficie'] <= max_s]
        else:
            print("Error: Opción inválida.")
            return
    except ValueError:
        print("Error: Ingrese números válidos.")
        return

    if filtrados:
        print(f"\nSe encontraron {len(filtrados)} países:")
        mostrar_tabla(filtrados)
    else:
        print("Error: Sin resultados para ese filtro.")

def ordenar_paises(paises):
    """Ordena por nombre, población o superficie asc/desc."""
    if not paises:
        print("Error: No hay países para ordenar.")
        return

    print("\n--- ORDENAR ---")
    print("1. Nombre")
    print("2. Población")
    print("3. Superficie")
    criterio = input("Criterio: ")
    orden = input("Orden A-Ascendente / D-Descendente: ").upper()

    key_map = {'1': 'nombre', '2': 'poblacion', '3': 'superficie'}
    if criterio not in key_map:
        print("Error: Criterio inválido.")
        return

    reverse = orden == 'D'
    paises_ordenados = sorted(paises, key=lambda x: x[key_map[criterio]], reverse=reverse)
    mostrar_tabla(paises_ordenados)

def mostrar_estadisticas(paises):
    """Muestra estadísticas: max/min, promedios, cantidad por continente."""
    if not paises:
        print("Error: No hay países cargados.")
        return

    print("\n--- ESTADÍSTICAS ---")
    pais_max_pob = max(paises, key=lambda x: x['poblacion'])
    pais_min_pob = min(paises, key=lambda x: x['poblacion'])
    prom_pob = sum(p['poblacion'] for p in paises) / len(paises)
    prom_sup = sum(p['superficie'] for p in paises) / len(paises)

    por_continente = {}
    for p in paises:
        por_continente[p['continente']] = por_continente.get(p['continente'], 0) + 1

    print(f"Mayor población: {pais_max_pob['nombre']} con {pais_max_pob['poblacion']:,}")
    print(f"Menor población: {pais_min_pob['nombre']} con {pais_min_pob['poblacion']:,}")
    print(f"Promedio población: {prom_pob:,.0f}")
    print(f"Promedio superficie: {prom_sup:,.0f} km²")
    print("\nPaíses por continente:")
    for cont, cant in sorted(por_continente.items()):
        print(f" {cont}: {cant}")

# ==================== MAIN ====================
def menu():
    paises = cargar_paises(RUTA_CSV)

    while True:
        print("\n==== GESTOR DE PAÍSES ====")
        print("1. Agregar país")
        print("2. Actualizar país")
        print("3. Buscar país")
        print("4. Filtrar países")
        print("5. Ordenar países")
        print("6. Mostrar estadísticas")
        print("7. Ver todos los países")
        print("8. Guardar y salir")

        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            if agregar_pais(paises):
                guardar_paises(RUTA_CSV, paises)
        elif opcion == '2':
            if actualizar_pais(paises):
                guardar_paises(RUTA_CSV, paises)
        elif opcion == '3':
            buscar_pais(paises)
        elif opcion == '4':
            filtrar_paises(paises)
        elif opcion == '5':
            ordenar_paises(paises)
        elif opcion == '6':
            mostrar_estadisticas(paises)
        elif opcion == '7':
            mostrar_tabla(paises)
        elif opcion == '8':
            guardar_paises(RUTA_CSV, paises)
            print("Datos guardados. ¡Hasta luego!")
            break
        else:
            print("Error: Opción inválida.")

if __name__ == "__main__":
    menu()
