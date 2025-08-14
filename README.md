# Servicio Social en el Laboratorio de Sistemas Biofísicos Excitables en la FC-UNAM Semestre 2024-2

> ⚠ **Proyecto en estado experimental**  
> Este repositorio contiene scripts, notebooks y prototipos desarrollados de forma no estructurada.  
> Algunos archivos están duplicados, otros scripts pueden no funcionar, y la GUI requiere reparación.  
> Usa el contenido con precaución.

---

## Descripción
Estudié los datos sobre intervalos entre latidos generados en el Laboratorio de Sistemas Excitables, por voluntarios que pedalean en una bicicleta ergonómica fija 325 CSX bajo cargas semanales crecientes de trabajo. 
Hay diversos protocolos. Para todos se debe llenar un cuestionario previo y se debe utilizar un electrocardiógrafo Zephyr tipo Bioharness para medir el pulso cardiaco. 
EL protocolo D con el cual se generaron los datos fue de la siguiente manera:
Hay una etapa de reposo de 7 minutos, una etapa de calentamiento de dos minutos a 50 Watts, una etapa de ejercicio de 11 minutos donde la carga es fija empezando a 50 Watts y 12 de recuperación. Las sesiones se pueden extender dependiendo del desempeño del sujeto (por ejemplo hasta 350 watts, es decir, 7 sesiones).

---

## Estructura y Flujo de Trabajo

Este repositorio contiene el trabajo realizado a partir de archivos obtenidos de un ensayo experimental.  
El flujo general fue el siguiente:

1. **Generación de estadísticas y PDF con gráficas**  
   - A partir de los archivos originales, se ejecutó un script que:
     - Calcula las estadísticas requeridas.
     - Exporta un archivo CSV con dichos datos.
     - Genera un PDF con todas las gráficas de los archivos procesados.

2. **Análisis en Jupyter Notebook**  
   - Lectura del CSV generado.
   - Visualización de todas las estadísticas en gráficos de dispersión (*scatterplots*).

3. **Interfaz Gráfica (GUI)**
   
   Debido a que en la toma de datos habia mucho ruido se limpiaban a mano usando excel, por esa misma razon, implemente la interfaz para limpiar la grtafica     usando el mouse y encerrando los puntos a eliminar, recortando el tiempo de 10-15 minutos por muestra a casi 2 minutos o menos.
   - Permite cargar un archivo `.csv` o `.txt`.
   - Limpia datos y elimina filas según ciertos criterios.
   - Exporta un nuevo `.csv` o `.txt` con los datos depurados.  
   *(Actualmente el script `.py` asociado está roto y requiere reparación).*

---

## Advertencias y Limitaciones

⚠ **Importante:**
- El repositorio contiene cuadernos Jupyter repetidos que serán eliminados en el futuro.
- Los scripts no están optimizados ni estructurados de forma modular.
- La GUI puede no funcionar en su estado actual.
- No existe un flujo automatizado; cada paso se ejecuta manualmente.
- La estructura de carpetas podría cambiar para mejorar la organización.

---

## Requisitos
- Python 3.x  
- Bibliotecas utilizadas: por agregar...

