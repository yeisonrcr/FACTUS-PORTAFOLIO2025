
import os
import django
import sqlite3

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'servidor.settings')
django.setup()
from repuestos.models import ModeloAnio

from repuestos.models import Marca, Modelo, Categoria, AnioAuto, ModeloAnio, Repuesto

def agregar_marcar_modelos():
    # Diccionario con marcas y modelos
    marcas_y_modelos = {
        "Mazda": ["Mazda3", "CX-5", "MX-5 Miata", "CX-9", "Mazda6"],
        "Subaru": ["Impreza", "Outback", "Forester", "Crosstrek", "Legacy"],
        "Kia": ["Soul", "Sportage", "Telluride", "Sorento", "Seltos"],
        "Hyundai": ["Elantra", "Santa Fe", "Tucson", "Sonata", "Palisade"],
        "Jeep": ["Wrangler", "Grand Cherokee", "Compass", "Cherokee", "Renegade"],
        "Volvo": ["XC90", "XC60", "S60", "V90", "C40 Recharge"],
        "Lexus": ["RX", "NX", "ES", "GX", "LX"],
        "Volkswagen": ["Golf", "Passat", "Jetta", "Atlas", "Tiguan"],
        "Tesla": ["Model S", "Model 3", "Model X", "Model Y", "Cybertruck"],
        "Dodge": ["Charger", "Challenger", "Durango", "Hornet", "Journey"],
        "Porsche": ["911", "Cayenne", "Macan", "Panamera", "Taycan"],
        "Ferrari": ["488 GTB", "Roma", "Portofino", "SF90 Stradale", "296 GTB"],
        "Lamborghini": ["Huracán", "Aventador", "Urus", "Revuelto", "Sian"],
        "Bugatti": ["Chiron", "Veyron", "Divo", "Bolide", "Centodieci"],
        "Cadillac": ["Escalade", "XT5", "CT5", "Lyriq", "XT4"],
        "Jaguar": ["F-Type", "XE", "XF", "E-PACE", "I-PACE"],
        "Land Rover": ["Range Rover", "Discovery", "Defender", "Velar", "Evoque"],
        "Mitsubishi": ["Outlander", "Eclipse Cross", "Lancer", "Pajero", "ASX"],
        "Peugeot": ["208", "308", "508", "2008", "3008"],
        "Renault": ["Clio", "Captur", "Megane", "Kadjar", "Scenic"],
        "Toyota": ["Corolla", "Camry", "RAV4", "Hilux", "Land Cruiser"],
        "Honda": ["Civic", "Accord", "CR-V", "Pilot", "Odyssey"],
        "Nissan": ["Altima", "Sentra", "Maxima", "Rogue", "Frontier"],
        "Aston Martin": ["DB11", "Vantage", "DBX"],
        "McLaren": ["720S", "Artura", "GT"],
        "Pagani": ["Zonda", "Huayra"],
        "Chevrolet": ["Silverado", "Malibu", "Camaro"],
        "Ford": ["F-150", "Mustang", "Explorer"],
        "BMW": ["3 Series", "X5", "i8"],
        "Mercedes-Benz": ["C-Class", "GLE", "AMG GT"]
    }

    nuevos = {
    "Seat": ["Ibiza", "Leon", "Arona", "Ateca", "Tarraco"],
    "Skoda": ["Fabia", "Octavia", "Kodiaq", "Kamiq", "Superb"],
    "Opel": ["Astra", "Corsa", "Insignia", "Crossland X", "Grandland X"],
    "Saab": ["9-3", "9-5", "900", "9-4X", "9000"],
    "Citroën": ["C3", "C4", "C5 Aircross", "Berlingo", "C1"],
    "Daihatsu": ["Terios", "Sirion", "Materia", "Copen", "Cuore"],
    "Isuzu": ["D-Max", "MU-X", "Trooper", "Rodeo", "Hombre"],
    "Pontiac": ["G6", "Grand Prix", "Firebird", "Vibe", "Solstice"],
    "Saturn": ["Aura", "Sky", "Vue", "Ion", "Outlook"],
    "Hummer": ["H1", "H2", "H3", "HX Concept", "EV Pickup"],
    "Rover": ["75", "45", "200", "400", "600"],
    "MG": ["MG6", "MG3", "ZS", "HS", "MG5"],
    "Geely": ["Emgrand", "Azkarra", "Coolray", "Panda", "Tugella"],
    "Chery": ["Tiggo 8", "Arrizo 5", "Tiggo 7", "Tiggo 2", "Tiggo 5"],
    "Great Wall": ["Haval H6", "Haval F7", "Haval H2", "Steed", "Wingle"],
    "BYD": ["Tang", "Song", "Han", "Qin", "Yuan"],
    "Tata": ["Nano", "Harrier", "Safari", "Hexa", "Nexon"],
    "Mahindra": ["Scorpio", "XUV500", "Thar", "Bolero", "TUV300"],
    "Lancia": ["Ypsilon", "Delta", "Thema", "Fulvia", "Stratos"]
}

    # Iterar por las marcas y agregar modelos
    for nombre_marca, modelos in nuevos.items():
        try:
            marca = Marca.objects.get(nombre=nombre_marca)
            for modelo_nombre in modelos:
                Modelo.objects.create(nombre=modelo_nombre, marca=marca)
                print(f"Modelo '{modelo_nombre}' agregado a la marca '{nombre_marca}'.")
        except Marca.DoesNotExist:
            print(f"La marca '{nombre_marca}' no existe en la base de datos.")

def agregar_categorias():
    categorias = [
        {"nombre": "Filtros de aire", "descripcion": "Filtros para el sistema de admisión de aire del motor."},
        {"nombre": "Filtros de aceite", "descripcion": "Filtros para mantener el aceite del motor limpio."},
        {"nombre": "Filtros de combustible", "descripcion": "Filtros para eliminar impurezas del combustible."},
        {"nombre": "Iluminación", "descripcion": "Faros, luces traseras, intermitentes y bombillas."},
        {"nombre": "Parabrisas", "descripcion": "Vidrios delanteros, traseros y limpiaparabrisas."},
        {"nombre": "Espejos retrovisores", "descripcion": "Espejos exteriores e interiores de automóviles."},
        {"nombre": "Dirección", "descripcion": "Componentes del sistema de dirección, como cajas y barras."},
        {"nombre": "Cables de encendido", "descripcion": "Cables para el sistema de encendido del motor."},
        {"nombre": "Tornillería", "descripcion": "Tuercas, tornillos y pernos para diversas aplicaciones."},
        {"nombre": "Aceites y lubricantes", "descripcion": "Aceites para motor, transmisión y otros lubricantes."},
        {"nombre": "Amortiguadores", "descripcion": "Componentes para absorber impactos y mejorar la estabilidad."},
        {"nombre": "Muelles", "descripcion": "Muelles para la suspensión y otros sistemas."},
        {"nombre": "Rodamientos", "descripcion": "Rodamientos de ruedas y otros sistemas."},
        {"nombre": "Bujías", "descripcion": "Componentes para encender la mezcla de aire-combustible."},
        {"nombre": "Cadenas de distribución", "descripcion": "Cadenas para sincronizar el movimiento del motor."},
        {"nombre": "Poleas", "descripcion": "Poleas para correas del motor y otros sistemas."},
        {"nombre": "Termostatos", "descripcion": "Controladores de temperatura del motor."},
        {"nombre": "Radiadores", "descripcion": "Sistemas de enfriamiento para el motor."},
        {"nombre": "Condensadores", "descripcion": "Parte del sistema de aire acondicionado."},
        {"nombre": "Compresores", "descripcion": "Compresores de aire acondicionado y otros sistemas."},
        {"nombre": "Fusibles", "descripcion": "Elementos de protección en sistemas eléctricos."},
        {"nombre": "Relés", "descripcion": "Interruptores eléctricos automáticos."},
        {"nombre": "Sensores", "descripcion": "Sensores de velocidad, temperatura y presión."},
        {"nombre": "Bobinas de encendido", "descripcion": "Componentes eléctricos para encender el motor."},
        {"nombre": "Cilindros maestros", "descripcion": "Cilindros para el sistema de frenos o embrague."},
        {"nombre": "Tambores de freno", "descripcion": "Componentes del sistema de frenos de tambor."},
        {"nombre": "Pastillas de freno", "descripcion": "Elementos de fricción para discos de freno."},
        {"nombre": "Discos de freno", "descripcion": "Discos utilizados en sistemas de frenado."},
        {"nombre": "Cables de freno", "descripcion": "Cables utilizados en frenos de mano."},
        {"nombre": "Parachoques", "descripcion": "Defensas delanteras y traseras para absorber impactos."},
        {"nombre": "Paneles de puerta", "descripcion": "Paneles interiores de las puertas del vehículo."},
        {"nombre": "Tapicería", "descripcion": "Materiales de revestimiento interior del automóvil."},
        {"nombre": "Cinturones de seguridad", "descripcion": "Sistemas de seguridad para los pasajeros."},
        {"nombre": "Volantes", "descripcion": "Volantes para el sistema de dirección."},
        {"nombre": "Tableros", "descripcion": "Consolas y paneles de instrumentos del vehículo."},
        {"nombre": "Airbags", "descripcion": "Sistemas de bolsas de aire para seguridad."},
        {"nombre": "Alternadores", "descripcion": "Generadores de energía eléctrica en el vehículo."},
        {"nombre": "Starters", "descripcion": "Motores de arranque para el encendido del vehículo."},
        {"nombre": "Claxon", "descripcion": "Sistemas de bocinas y alertas sonoras."},
        {"nombre": "Calefactores", "descripcion": "Sistemas de calefacción para el interior del vehículo."},
        {"nombre": "Defensas", "descripcion": "Protectores delanteros y traseros del vehículo."},
        {"nombre": "Tiradores de puertas", "descripcion": "Manijas exteriores e interiores de puertas."},
        {"nombre": "Bisagras", "descripcion": "Bisagras para puertas, capós y cofres."},
        {"nombre": "Cubreasientos", "descripcion": "Fundas y cubiertas para asientos de automóviles."},
        {"nombre": "Enganches", "descripcion": "Enganches para remolques y cargas."},
        {"nombre": "Portaequipajes", "descripcion": "Sistemas para transportar equipaje en el techo."},
        {"nombre": "Barras estabilizadoras", "descripcion": "Barras para mejorar la estabilidad del vehículo."},
        {"nombre": "Guardafangos", "descripcion": "Protectores para evitar salpicaduras de ruedas."},
        {"nombre": "Catalizadores", "descripcion": "Elementos para reducir emisiones contaminantes."},
        {"nombre": "Mofles", "descripcion": "Silenciadores para el sistema de escape."},
        {"nombre": "Cadenas para neumáticos", "descripcion": "Cadenas para mejorar la tracción en nieve o hielo."},
        {"nombre": "Llaves de ruedas", "descripcion": "Herramientas para desmontar ruedas."},
        {"nombre": "Cables de remolque", "descripcion": "Cables y cuerdas para remolcar vehículos."},
        {"nombre": "Tapacubos", "descripcion": "Cubiertas decorativas para ruedas."},
        {"nombre": "Llaves inteligentes", "descripcion": "Llaves electrónicas para vehículos modernos."},
        {"nombre": "Control remoto", "descripcion": "Controles para apertura y cierre de puertas."}
    ]

    nuevas = [
    {"nombre": "Componentes de inyección", "descripcion": "Partes del sistema de inyección de combustible."},
    {"nombre": "Turbocompresores", "descripcion": "Dispositivos que aumentan la potencia del motor."},
    {"nombre": "Embragues", "descripcion": "Componentes para el sistema de transmisión."},
    {"nombre": "Cadenas de tiempo", "descripcion": "Cadenas para sincronización del motor."},
    {"nombre": "Pistones", "descripcion": "Componentes que se mueven dentro de los cilindros del motor."},
    {"nombre": "Bielas", "descripcion": "Piezas que conectan los pistones al cigüeñal."},
    {"nombre": "Cigüeñales", "descripcion": "Eje central del motor."},
    {"nombre": "Toberas de combustible", "descripcion": "Boquillas que atomizan el combustible en la cámara de combustión."},
    {"nombre": "Sistemas de escape", "descripcion": "Tuberías y componentes para la salida de gases del motor."},
    {"nombre": "Radiadores de aceite", "descripcion": "Enfriadores para el aceite del motor."},
    {"nombre": "Mangueras del radiador", "descripcion": "Conductos flexibles para el sistema de enfriamiento."},
    {"nombre": "Tensores de correa", "descripcion": "Mecanismos que mantienen la tensión de las correas del motor."},
    {"nombre": "Sensores de flujo de masa de aire", "descripcion": "Sensores que miden la cantidad de aire que entra al motor."},
    {"nombre": "Módulos de control del cuerpo", "descripcion": "Unidades de control para diversos sistemas del vehículo."},
    {"nombre": "Bombas de combustible", "descripcion": "Dispositivos que suministran combustible al motor."},
    {"nombre": "Bombas de freno", "descripcion": "Componentes que generan presión en el sistema de frenos."},
    {"nombre": "Cilindros de rueda", "descripcion": "Componentes de los frenos de tambor."},
    {"nombre": "Kits de reparación de frenos", "descripcion": "Conjuntos para el mantenimiento y reparación del sistema de frenos."},
    {"nombre": "Bombas de dirección asistida", "descripcion": "Dispositivos que facilitan la dirección del vehículo."},
    {"nombre": "Enfriadores de transmisión", "descripcion": "Dispositivos que enfrían el fluido de la transmisión."},
    {"nombre": "Arboles de levas", "descripcion": "Ejes que controlan la apertura y cierre de las válvulas del motor."},
    {"nombre": "Balancines", "descripcion": "Componentes que transmiten el movimiento del árbol de levas a las válvulas."},
    {"nombre": "Válvulas", "descripcion": "Componentes que controlan el flujo de aire y combustible en el motor."},
    {"nombre": "Resortes de válvula", "descripcion": "Muelles que cierran las válvulas del motor."},
    {"nombre": "Cadenas de distribución", "descripcion": "Cadenas que sincronizan el movimiento del cigüeñal y el árbol de levas."},
    {"nombre": "Conductos de admisión", "descripcion": "Tuberías que llevan aire al motor."},
    {"nombre": "Filtros de partículas", "descripcion": "Dispositivos que reducen las emisiones contaminantes."},
    {"nombre": "Compresores de aire acondicionado", "descripcion": "Dispositivos que comprimen el refrigerante del sistema de aire acondicionado."},
    {"nombre": "Radiadores de calefacción", "descripcion": "Dispositivos que calientan el aire en el interior del vehículo."},
    {"nombre": "Sensores de temperatura", "descripcion": "Sensores que miden la temperatura del motor y otros sistemas."},
    {"nombre": "Sensores de presión de aceite", "descripcion": "Sensores que miden la presión del aceite en el motor."},
    {"nombre": "Plumas limpiaparabrisas", "descripcion": "Componentes que limpian el parabrisas."},
    {"nombre": "Interruptores de luces", "descripcion": "Componentes que controlan el encendido y apagado de las luces del vehículo."},
    {"nombre": "Baterías", "descripcion": "Fuente de energía eléctrica para el vehículo."},
    {"nombre": "Cables de batería", "descripcion": "Conductores eléctricos que conectan la batería a los sistemas del vehículo."}
]

    for categoria_data in nuevas:
        Categoria.objects.create(
            nombre=categoria_data["nombre"],
            descripcion=categoria_data["descripcion"]
        )
        print(f"Categoría '{categoria_data['nombre']}' agregada correctamente.")

def agregar_modelos_anios():
    # Datos de ejemplo: modelos y años asociados
    modelos_anios = [
        {"modelo_nombre": "Corolla", "marca_nombre": "Toyota", "anios": [2015, 2016, 2017]},
        {"modelo_nombre": "Civic", "marca_nombre": "Honda", "anios": [2018, 2019, 2020]},
        {"modelo_nombre": "Altima", "marca_nombre": "Nissan", "anios": [2017, 2018, 2019]},
        {"modelo_nombre": "3 Series", "marca_nombre": "BMW", "anios": [2020, 2021, 2022]},
        {"modelo_nombre": "F-150", "marca_nombre": "Ford", "anios": [2015, 2016, 2018]},
        {"modelo_nombre": "Camaro", "marca_nombre": "Chevrolet", "anios": [2016, 2017, 2018]},
        {"modelo_nombre": "Wrangler", "marca_nombre": "Jeep", "anios": [2019, 2020, 2021]},
        {"modelo_nombre": "Model S", "marca_nombre": "Tesla", "anios": [2018, 2019, 2020]},
        {"modelo_nombre": "CX-5", "marca_nombre": "Mazda", "anios": [2017, 2018, 2020]},
        {"modelo_nombre": "Passat", "marca_nombre": "Volkswagen", "anios": [2015, 2016, 2017]},
    ]
    
    mode =[
    {"modelo_nombre": "Yaris", "marca_nombre": "Toyota", "anios": [2017, 2018, 2019]},
    {"modelo_nombre": "Accord", "marca_nombre": "Honda", "anios": [2015, 2016, 2017]},
    {"modelo_nombre": "Sentra", "marca_nombre": "Nissan", "anios": [2018, 2019, 2020]},
    {"modelo_nombre": "X5", "marca_nombre": "BMW", "anios": [2020, 2021, 2022]},
    {"modelo_nombre": "Mustang", "marca_nombre": "Ford", "anios": [2015, 2016, 2018]},
    {"modelo_nombre": "Impala", "marca_nombre": "Chevrolet", "anios": [2016, 2017, 2018]},
    {"modelo_nombre": "Cherokee", "marca_nombre": "Jeep", "anios": [2019, 2020, 2021]},
    {"modelo_nombre": "Model X", "marca_nombre": "Tesla", "anios": [2018, 2019, 2020]},
    {"modelo_nombre": "Mazda6", "marca_nombre": "Mazda", "anios": [2017, 2018, 2020]},
    {"modelo_nombre": "Tiguan", "marca_nombre": "Volkswagen", "anios": [2015, 2016, 2017]},
    {"modelo_nombre": "Sienna", "marca_nombre": "Toyota", "anios": [2015, 2016, 2017]},
    {"modelo_nombre": "Pilot", "marca_nombre": "Honda", "anios": [2018, 2019, 2020]},
    {"modelo_nombre": "Rogue", "marca_nombre": "Nissan", "anios": [2017, 2018, 2019]},
    {"modelo_nombre": "X3", "marca_nombre": "BMW", "anios": [2020, 2021, 2022]},
    {"modelo_nombre": "Explorer", "marca_nombre": "Ford", "anios": [2015, 2016, 2018]},
    {"modelo_nombre": "Malibu", "marca_nombre": "Chevrolet", "anios": [2016, 2017, 2018]},
    {"modelo_nombre": "Compass", "marca_nombre": "Jeep", "anios": [2019, 2020, 2021]},
    {"modelo_nombre": "Model 3", "marca_nombre": "Tesla", "anios": [2018, 2019, 2020]},
    {"modelo_nombre": "Mazda3", "marca_nombre": "Mazda", "anios": [2017, 2018, 2020]},
    {"modelo_nombre": "Jetta", "marca_nombre": "Volkswagen", "anios": [2015, 2016, 2017]}
]
    
    


    for item in mode:
        # Obtener el modelo correspondiente
        try:
            modelo = Modelo.objects.get(nombre=item["modelo_nombre"], marca__nombre=item["marca_nombre"])
        except Modelo.DoesNotExist:
            print(f"El modelo '{item['modelo_nombre']}' de la marca '{item['marca_nombre']}' no existe en la base de datos.")
            continue

        # Crear/obtener los años correspondientes
        anios_objs = []
        for anio in item["anios"]:
            anio_obj, created = AnioAuto.objects.get_or_create(anio=anio)
            anios_objs.append(anio_obj)

        # Crear el ModeloAnio y asociar los años
        modelo_anio, created = ModeloAnio.objects.get_or_create(modelo=modelo)
        modelo_anio.anios.set(anios_objs)  # Asociar los años al modelo
        modelo_anio.save()

        print(f"ModeloAnio creado/actualizado: {modelo} con años {', '.join(str(a.anio) for a in anios_objs)}")

def agregar_anios():
    try:
        # Conectar a la base de datos SQLite
        connection = sqlite3.connect('db.sqlite3')
        cursor = connection.cursor()

        # Crear la tabla AnioAuto si no existe

        # Agregar años desde 1970 hasta 2024
        for anio in range(1990, 2025):
            try:
                cursor.execute('INSERT INTO repuestos_anioauto (anio) VALUES (?)', (anio,))
            except sqlite3.IntegrityError:
                # Si el año ya existe, pasar
                pass

        # Confirmar los cambios
        connection.commit()

        print("Años agregados exitosamente.")

    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")

    finally:
        if connection:
            cursor.close()
            connection.close()
            print("Conexión cerrada.")
     
def agregar_marcas():

    # Conexión a la base de datos SQLite
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()


    # Lista de marcas
    marcas = [
    {"nombre": "Toyota"},
    {"nombre": "Honda"},
    {"nombre": "Ford"},
    {"nombre": "Chevrolet"},
    {"nombre": "Nissan"},
    {"nombre": "BMW"},
    {"nombre": "Mercedes-Benz"},
    {"nombre": "Volkswagen"},
    {"nombre": "Audi"},
    {"nombre": "Hyundai"},
    {"nombre": "Kia"},
    {"nombre": "Mazda"},
    {"nombre": "Subaru"},
    {"nombre": "Tesla"},
    {"nombre": "Jeep"},
    {"nombre": "Volvo"},
    {"nombre": "Porsche"},
    {"nombre": "Jaguar"},
    {"nombre": "Lexus"},
    {"nombre": "Land Rover"},
    {"nombre": "Renault"},
    {"nombre": "Peugeot"},
    {"nombre": "Fiat"},
    {"nombre": "Mitsubishi"},
    {"nombre": "Suzuki"},
    {"nombre": "Chrysler"},
    {"nombre": "Dodge"},
    {"nombre": "Ram"},
    {"nombre": "Acura"},
    {"nombre": "Infiniti"},
    {"nombre": "Buick"},
    {"nombre": "GMC"},
    {"nombre": "Cadillac"},
    {"nombre": "Lincoln"},
    {"nombre": "Genesis"},
    {"nombre": "Alfa Romeo"},
    {"nombre": "Mini"},
    {"nombre": "Maserati"},
    {"nombre": "Bentley"},
    {"nombre": "Rolls-Royce"},
    {"nombre": "Ferrari"},
    {"nombre": "Lamborghini"},
    {"nombre": "Aston Martin"},
    {"nombre": "McLaren"},
    {"nombre": "Pagani"}
]

    nuevas = [
    {"nombre": "Seat"},
    {"nombre": "Skoda"},
    {"nombre": "Opel"},
    {"nombre": "Saab"},
    {"nombre": "Daewoo"},
    {"nombre": "SsangYong"},
    {"nombre": "Citroën"},
    {"nombre": "Daihatsu"},
    {"nombre": "Isuzu"},
    {"nombre": "Pontiac"},
    {"nombre": "Saturn"},
    {"nombre": "Hummer"},
    {"nombre": "Rover"},
    {"nombre": "MG"},
    {"nombre": "Geely"},
    {"nombre": "Chery"},
    {"nombre": "Great Wall"},
    {"nombre": "BYD"},
    {"nombre": "Tata"},
    {"nombre": "Mahindra"},
    {"nombre": "Lancia"},
    {"nombre": "Alpine"},
    {"nombre": "Dacia"},
    {"nombre": "Holden"},
    {"nombre": "Proton"},
    {"nombre": "Perodua"},
    {"nombre": "Maruti Suzuki"},
    {"nombre": "Spyker"},
    {"nombre": "Rimac"},
    {"nombre": "Koenigsegg"},
    {"nombre": "Lucid"},
    {"nombre": "Rivian"},
    {"nombre": "Fisker"},
    {"nombre": "Faraday Future"},
    {"nombre": "Polestar"}
]


    # Insertar marcas en la tabla
    for marca in nuevas:
        try:
            cursor.execute("INSERT INTO repuestos_marca (nombre) VALUES (?)", (marca['nombre'],))
        except sqlite3.IntegrityError:
            print(f"La marca {marca['nombre']} ya existe en la tabla.")

    # Guardar cambios y cerrar conexión
    conn.commit()
    conn.close()

    print("Datos insertados con éxito.")


if __name__ == "__main__":
    #agregar_marcas()
    #agregar_anios()
    #agregar_categorias()
    #agregar_marcar_modelos()
    agregar_modelos_anios()