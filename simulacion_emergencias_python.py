import random
import simpy as simpy
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

random.seed(10)

SIM_TIME = 24 * 60  
INTERVALO_LLEGADA_PACIENTES = {
    'normal': 10,     
    'fin_semana': 7,  
    'feriado': 5      
}

# Recursos y sus costos
COSTOS = {
    'enfermera': 15000,    # Costo mensual por enfermera (Q)
    'doctor': 40000,       # Costo mensual por doctor (Q)
    'rayosX': 500000,      # Costo de equipo de rayos X (Q)
    'laboratorio': 300000  # Costo de equipo de laboratorio (Q)
}

# Tiempos de atención en minutos
TIEMPOS = {
    'triage': 10,        # Tiempo que tarda la evaluación inicial
    'doctor': {          # Tiempo de atención médica según severidad
        1: 60,           # Emergencia crítica (1 hora)
        2: 45,           # Emergencia severa (45 min)
        3: 30,           # Emergencia moderada (30 min)
        4: 20,           # Emergencia leve (20 min)
        5: 15            # No emergencia (15 min)
    },
    'rayosX': 15,        # Tiempo para hacer rayos X
    'laboratorio': 20    # Tiempo para procesamiento de laboratorio
}

# Estadísticas
estadisticas = {
    'tiempo_total': [],            # Tiempo total en el sistema
    'tiempo_espera_triage': [],    # Tiempo esperando evaluación
    'tiempo_espera_doctor': [],    # Tiempo esperando doctor
    'tiempo_espera_rayosX': [],    # Tiempo esperando rayos X
    'tiempo_espera_lab': [],       # Tiempo esperando laboratorio
    'severidad': []                # Severidad asignada al paciente
}

class SalaEmergencia:
    def __init__(self, env, num_enfermeras, num_doctores, num_rayosX, num_lab, tipo_dia='normal'):
        self.env = env
        self.enfermeras = simpy.PriorityResource(env, capacity=num_enfermeras)
        self.doctores = simpy.PriorityResource(env, capacity=num_doctores)
        self.rayosX = simpy.PriorityResource(env, capacity=num_rayosX)
        self.laboratorio = simpy.PriorityResource(env, capacity=num_lab)
        self.tipo_dia = tipo_dia
        self.contador_pacientes = 0
    
    def llegada_paciente(self):
        """Genera la llegada de pacientes según el tipo de día"""
        while True:
            intervalo = INTERVALO_LLEGADA_PACIENTES[self.tipo_dia]
            yield self.env.timeout(random.expovariate(1.0/intervalo))
            
            self.contador_pacientes += 1
            self.env.process(self.proceso_paciente(self.contador_pacientes))
    
    def proceso_paciente(self, id_paciente):
        """Proceso completo de atención de un paciente"""
        tiempo_llegada = self.env.now
        tiempo_inicio_triage = 0
        tiempo_fin_triage = 0
        tiempo_inicio_doctor = 0
        tiempo_fin_doctor = 0
        tiempo_inicio_rayosX = 0
        tiempo_fin_rayosX = 0
        tiempo_inicio_lab = 0
        tiempo_fin_lab = 0
        tiempo_salida = 0
        
        print(f"[{self.env.now:.1f}] Paciente {id_paciente} llega a emergencias")
        
        tiempo_inicio_triage = self.env.now
        with self.enfermeras.request(priority=5) as req:
            yield req
            tiempo_espera_triage = self.env.now - tiempo_inicio_triage
            print(f"[{self.env.now:.1f}] Paciente {id_paciente} inicia triage después de esperar {tiempo_espera_triage:.1f} minutos")

            yield self.env.timeout(TIEMPOS['triage'])
            
            severidad = random.choices([1, 2, 3, 4, 5], weights=[5, 15, 30, 35, 15])[0]
            estadisticas['severidad'].append(severidad)
            print(f"[{self.env.now:.1f}] Paciente {id_paciente} tiene severidad {severidad}")
            tiempo_fin_triage = self.env.now
        

        estadisticas['tiempo_espera_triage'].append(tiempo_espera_triage)

        necesita_rayosX = random.random() < 0.40
 
        necesita_lab = random.random() < 0.60

        if necesita_rayosX:
            tiempo_inicio_rayosX = self.env.now
            with self.rayosX.request(priority=severidad) as req:
                yield req
                tiempo_espera_rayosX = self.env.now - tiempo_inicio_rayosX
                print(f"[{self.env.now:.1f}] Paciente {id_paciente} inicia rayos X después de esperar {tiempo_espera_rayosX:.1f} minutos")
                yield self.env.timeout(TIEMPOS['rayosX'])
                tiempo_fin_rayosX = self.env.now
            estadisticas['tiempo_espera_rayosX'].append(tiempo_espera_rayosX)

        if necesita_lab:
            tiempo_inicio_lab = self.env.now
            with self.laboratorio.request(priority=severidad) as req:
                yield req
                tiempo_espera_lab = self.env.now - tiempo_inicio_lab
                print(f"[{self.env.now:.1f}] Paciente {id_paciente} inicia laboratorio después de esperar {tiempo_espera_lab:.1f} minutos")
                yield self.env.timeout(TIEMPOS['laboratorio'])
                tiempo_fin_lab = self.env.now
            estadisticas['tiempo_espera_lab'].append(tiempo_espera_lab)

        tiempo_inicio_doctor = self.env.now
        with self.doctores.request(priority=severidad) as req:
            yield req
            tiempo_espera_doctor = self.env.now - tiempo_inicio_doctor
            print(f"[{self.env.now:.1f}] Paciente {id_paciente} inicia atención médica después de esperar {tiempo_espera_doctor:.1f} minutos")
            yield self.env.timeout(TIEMPOS['doctor'][severidad])
            tiempo_fin_doctor = self.env.now

        estadisticas['tiempo_espera_doctor'].append(tiempo_espera_doctor)

        tiempo_salida = self.env.now
        tiempo_total = tiempo_salida - tiempo_llegada
        estadisticas['tiempo_total'].append(tiempo_total)
        print(f"[{self.env.now:.1f}] Paciente {id_paciente} sale de emergencias después de {tiempo_total:.1f} minutos totales")

def ejecutar_simulacion(num_enfermeras, num_doctores, num_rayosX, num_lab, tipo_dia='normal'):
    """Ejecuta una simulación con los parámetros dados"""
    for key in estadisticas:
        estadisticas[key] = []

    env = simpy.Environment()
    sala = SalaEmergencia(env, num_enfermeras, num_doctores, num_rayosX, num_lab, tipo_dia)

    env.process(sala.llegada_paciente())

    env.run(until=SIM_TIME)
    
    resultados = {
        'tiempo_promedio_total': np.mean(estadisticas['tiempo_total']) if estadisticas['tiempo_total'] else 0,
        'tiempo_promedio_espera_triage': np.mean(estadisticas['tiempo_espera_triage']) if estadisticas['tiempo_espera_triage'] else 0,
        'tiempo_promedio_espera_doctor': np.mean(estadisticas['tiempo_espera_doctor']) if estadisticas['tiempo_espera_doctor'] else 0,
        'tiempo_promedio_espera_rayosX': np.mean(estadisticas['tiempo_espera_rayosX']) if estadisticas['tiempo_espera_rayosX'] else 0,
        'tiempo_promedio_espera_lab': np.mean(estadisticas['tiempo_espera_lab']) if estadisticas['tiempo_espera_lab'] else 0,
        'num_pacientes': len(estadisticas['tiempo_total']),
        'costo_mensual': (num_enfermeras * COSTOS['enfermera'] + num_doctores * COSTOS['doctor']),
        'costo_equipos': (num_rayosX * COSTOS['rayosX'] + num_lab * COSTOS['laboratorio'])
    }
    
    return resultados

def generar_graficas(resultados_comparacion):
    """Genera gráficas comparativas de diferentes configuraciones"""
    df = pd.DataFrame(resultados_comparacion)
    df = df.sort_values('tiempo_promedio_total')
    
    plt.figure(figsize=(12, 6))
    plt.bar(df['configuracion'], df['tiempo_promedio_total'])
    plt.title('Tiempo promedio total en el sistema')
    plt.xlabel('Configuración (E-D-X-L)')
    plt.ylabel('Tiempo (minutos)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('tiempo_total.png')
    plt.show()

    plt.figure(figsize=(12, 8))
    x = np.arange(len(df['configuracion']))
    width = 0.2
    
    plt.bar(x - width*1.5, df['tiempo_promedio_espera_triage'], width, label='Espera Triage')
    plt.bar(x - width/2, df['tiempo_promedio_espera_doctor'], width, label='Espera Doctor')
    plt.bar(x + width/2, df['tiempo_promedio_espera_rayosX'], width, label='Espera Rayos X')
    plt.bar(x + width*1.5, df['tiempo_promedio_espera_lab'], width, label='Espera Laboratorio')
    
    plt.xlabel('Configuración (E-D-X-L)')
    plt.ylabel('Tiempo (minutos)')
    plt.title('Tiempos de espera por recurso')
    plt.xticks(x, df['configuracion'], rotation=45)
    plt.legend()
    plt.tight_layout()
    plt.savefig('tiempos_espera.png')
    
    plt.figure(figsize=(10, 6))
    plt.scatter(df['costo_mensual'] + df['costo_equipos']/36, df['tiempo_promedio_total'], s=100)
    plt.show()

    for i, txt in enumerate(df['configuracion']):
        plt.annotate(txt, (df['costo_mensual'].iloc[i] + df['costo_equipos'].iloc[i]/36, df['tiempo_promedio_total'].iloc[i]))
    
    plt.title('Costo mensual vs. Tiempo promedio total')
    plt.xlabel('Costo mensual (Q) [Equipos amortizados a 36 meses]')
    plt.ylabel('Tiempo promedio (minutos)')
    plt.grid(True)
    plt.savefig('costo_vs_tiempo.png')
    plt.show()

def main():

    resultados_comparacion = []
    
    configuraciones = [
        (2, 2, 1, 1),  # 2 enfermeras, 2 doctores, 1 rayos X, 1 laboratorio
        (3, 2, 1, 1),  # 3 enfermeras, 2 doctores, 1 rayos X, 1 laboratorio
        (3, 3, 1, 1),  # 3 enfermeras, 3 doctores, 1 rayos X, 1 laboratorio
        (3, 3, 2, 1),  # 3 enfermeras, 3 doctores, 2 rayos X, 1 laboratorio
        (3, 3, 2, 2),  # 3 enfermeras, 3 doctores, 2 rayos X, 2 laboratorios
        (4, 3, 2, 2),  # 4 enfermeras, 3 doctores, 2 rayos X, 2 laboratorios
        (4, 4, 2, 2),  # 4 enfermeras, 4 doctores, 2 rayos X, 2 laboratorios
        (5, 4, 2, 2),  # 5 enfermeras, 4 doctores, 2 rayos X, 2 laboratorios
    ]
    

    for config in configuraciones:
        num_enfermeras, num_doctores, num_rayosX, num_lab = config
        config_name = f"{num_enfermeras}-{num_doctores}-{num_rayosX}-{num_lab}"
        print(f"\nEjecutando simulación con configuración: {config_name}")
        
        resultados = ejecutar_simulacion(num_enfermeras, num_doctores, num_rayosX, num_lab, 'normal')
        resultados['configuracion'] = config_name
        resultados_comparacion.append(resultados)
        
        print(f"Pacientes atendidos: {resultados['num_pacientes']}")
        print(f"Tiempo promedio total: {resultados['tiempo_promedio_total']:.2f} minutos")
        print(f"Tiempo promedio espera triage: {resultados['tiempo_promedio_espera_triage']:.2f} minutos")
        print(f"Tiempo promedio espera doctor: {resultados['tiempo_promedio_espera_doctor']:.2f} minutos")
        print(f"Tiempo promedio espera rayos X: {resultados['tiempo_promedio_espera_rayosX']:.2f} minutos")
        print(f"Tiempo promedio espera laboratorio: {resultados['tiempo_promedio_espera_lab']:.2f} minutos")
        print(f"Costo mensual personal: Q{resultados['costo_mensual']:,.2f}")
        print(f"Costo equipos: Q{resultados['costo_equipos']:,.2f}")
    
    generar_graficas(resultados_comparacion)
    
    mejor_config = min(resultados_comparacion, key=lambda x: x['tiempo_promedio_total'])
    mejor_config_idx = resultados_comparacion.index(mejor_config)
    mejor_config_params = configuraciones[mejor_config_idx]
    
    print("\n--- Configuración recomendada ---")
    print(f"Enfermeras: {mejor_config_params[0]}")
    print(f"Doctores: {mejor_config_params[1]}")
    print(f"Equipos de Rayos X: {mejor_config_params[2]}")
    print(f"Equipos de Laboratorio: {mejor_config_params[3]}")
    print(f"Tiempo promedio total: {mejor_config['tiempo_promedio_total']:.2f} minutos")
    print(f"Costo mensual total: Q{mejor_config['costo_mensual'] + mejor_config['costo_equipos']/36:,.2f}")

if __name__ == "__main__":
    main()
