

## 2026-10-09: Ajustes a la Tabla y Tooltip Avanzado
- Se cambió el encabezado DOCUMENTO PPT a DOC PPT.
- Se limpió la columna Observaciones Técnicas para mostrar sólo el botón VER MÁS en naranja, eliminando el texto previo para mayor limpieza.
- Se replicó la estructura HTML compleja del Tooltip del Mapa Hacia el Treemap, incluyendo los totales por nivel (Total, Pagado, Pendiente, Beneficiarios).


## 2026-10-09: Pruebas de Laboratorio Visual
- Se creó una vista de Laboratorio Visual con 5 gráficos experimentales.
- El usuario decidió integrar 3 de ellos (Radar, Sunburst, Heatmap) en la vista principal de Ejecución, reestructurando el panel de la tabla de datos en una cuadrícula 2x2.


## 2026-10-09: Refinamiento de Gráficos del Grid 2x2
- Heatmap: Se aumentó el límite de ciudades mostradas y se ajustó el margen inferior para que los textos en el eje X no se corten.
- Radar: Se aumentó el radio del gráfico para aprovechar mejor el contenedor y se incrementó el grosor de las líneas.
- Sunburst: Se ocultaron las etiquetas de texto que se solapaban en secciones muy pequeñas (minAngle) para limpiar el diseño visual.


## 2026-10-09: Ajustes a Matriz y Sunburst
- Heatmap: Se implementó un diccionario de abreviaturas inteligentes para el eje X, permitiendo recuperar la proporción cuadrada de las celdas sin cortar los textos largos.
- Sunburst: Se modificó la jerarquía de anillos. Antes era Estado (Pagado/Pendiente) -> Novedad -> Ciudad. Ahora es Ciudad -> Novedad, asignando colores neón únicos a cada ciudad y resaltando en rojo las novedades reales.
- Se corrigió un error de sintaxis JS duplicada que causaba fallos de renderizado.
