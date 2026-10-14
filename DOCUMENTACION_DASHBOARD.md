# Documentacin del Dashboard - Semilleros Balance Pagos
**Versin**: V1 Final (Neon Cyberpunk Layout)

## Archivos de Respaldo
Se han creado copias de seguridad de la versn estable actual para que puedas trabajar sobre ellas o volver a este punto en el futuro:
- `frontend_v1_final.html`: El cdigo HTML/JS estable con todos los ajustes de layout (4 columnas, sin padding, tooltips corregidos).
- `data_github_backup.json`: La data de prueba.

## Lgica de los Grficos Cuestionados

### 1. Ranking de Ejecucin Financiera (Pestaa 1) vs Eficacia de Pagos por Resolucin (Pestaa 2)
**Cmo funciona cada uno?**
- **Eficacia de Pagos (Pestaa 2)**: Es un grfico ESTTICO. Toma todas las resoluciones de la base de datos, calcula la frmula `(Valor Pagado / Valor Total) * 100`, y las grafica apilando Pagado (Verde) y Pendiente (Naranja). Su nico propsito es evaluar el rendimiento de las resoluciones.
- **Ranking de Ejecucin Financiera (Pestaa 1)**: Es un grfico DINMICO e interactivo. Este grfico est atado al filtro del grfico Sankey (Flujo de Capital). Si en el Sankey eliges ver "Resoluciones -> Ciudades", el ranking mostrar Resoluciones. Si cambias a "Departamento -> Ciudades", el ranking cambiar automticamente para mostrar Departamentos.

**Veredicto de fusin**: S, pueden combinarse. Dado que el de la Pestaa 1 ya hace el trabajo del de la Pestaa 2 (cuando est en modo resoluciones), el de la Pestaa 2 es redundante. Podramos eliminar el de la Pestaa 2 o convertir el de la Pestaa 1 en el grfico maestro.

### 2. Avance Top Ciudades (Pestaa 1) vs Ranking de Ineficiencia (Pestaa 2)
**Cmo se calculan?**
- **Avance Top Ciudades (Pestaa 1)**: Filtra las ciudades por el volumen total de dinero que mueven (Pagado + Pendiente). Te muestra las ciudades ms "pesadas" financieramente, y su barra te indica cunto han pagado.
- **Ranking de Ineficiencia (Pestaa 2)**: Calcula una "Tasa de Deuda" con la frmula `(Valor Pendiente / Valor Total) * 100` para cada ciudad. Ordena la lista de peor a mejor y te muestra el "Top 15" de las ciudades ms colgadas, sin importar si su presupuesto es de 1 milln o 100 mil millones.

**Veredicto de fusin**: Es una excelente idea. Para ahorrar espacio y centralizar, se podra colocar un botn o un 'switch' en el panel de *Avance Top Ciudades* en la Pestaa 1 que diga: `[Ordenar por Volumen] / [Ordenar por Tasa de Deuda (Ineficiencia)]`, unificando ambas inteligencias en un solo panel.

## Salud en Ciudades
Como IA orientada al diseo UI/UX, mi recomendacin es **no mover Salud en Ciudades a la Pestaa 1**. La Pestaa 1 logr una simetra de 4 columnas perfectas y elimin el scroll vertical. Si forzamos un grfico extra all, romperemos la "proporcin urea" del espacio y obligaremos al usuario a hacer scroll, perdiendo la inmersin tipo "Centro de Comando" de un solo vistazo. Es mejor mantener la Pestaa 2 para anlisis especficos y detallados.

## Especificaciones CSS/Layout Logradas
- **Manejo Flexbox**: Se forz `display: flex; flex-direction: column` en el contenedor `view_operacion` y `min-h-0` en los paneles hijos. Esto garantiza que los grficos de ECharts se compriman/estiren automticamente al 100% de la ventana, sin colapsar su altura a 0px.
- **Mrgenes (Cero Espacio Muerto)**: Se modific el CSS de la etiqueta `body` eliminando los 20px de padding inferior (`padding: 5px 20px 5px 20px;`) permitiendo que el tablero toque el suelo de la pantalla.
- **ECharts (Cmara)**: Se centr el mapa manualmente manipulando la latitud en el array `center: [-74.0, 7.5]` y bajando el zoom a `2.0` para obligar al renderizador a mostrar a Santa Marta y Cali simultneamente.


## Actualizaciones V2 (Ajustes de UI y Lógica Espacial)
- **Representación de SIN CIUDAD**: Se implementó una lógica de unificación donde cualquier registro con ciudad en blanco es etiquetado como `"SIN CIUDAD"`. Se le asignó una coordenada geográfica aislada (Latitud 3.20, Longitud -74.08, al sur de Bogotá) para que aparezca en el mapa. 
- **Desvinculación del visualMap**: En el mapa de la pestaña 1, `"SIN CIUDAD"` acumulaba tanto dinero que rompía la escala de colores (termómetro), haciendo que todas las demás ciudades se vieran rojas. Se separó a `"SIN CIUDAD"` en su propia `series` de ECharts con un color verde fijo, permitiendo que el `visualMap` calcule sus mínimos y máximos basándose exclusivamente en las ciudades reales.
- **Gráfico Radial (Tipo Novedad)**: 
  - Se redujo su espacio a `col-span-2` y se amplió "Impacto Financiero" a `col-span-4`.
  - Para evitar recortes en la caja pequeña, se ajustó el `center` a `[52%, 45%]` y el `radius` interior/exterior a `['15%', '90%']`.
  - Se eliminó el límite de novedades mostradas (ahora grafica el Top 15, cubriendo todo el espectro).
  - Se aplicó un espaciado cibernético entre los aros usando `barWidth: '50%'`.
  - Se implementó un mapeo de abreviaturas para los nombres largos (ej. "CAMBIO DE RESIDENCIA" -> "RESIDENCIA") para evitar que los textos del eje izquierdo se desborden o sobrepongan, garantizando que quepan limpiamente las 15 líneas.
- **Tooltips Flotantes (Anti-Overflow)**: Se añadió la propiedad `appendToBody: true` (y `confine: true`) a los tooltips de ECharts que estaban dentro de contenedores pequeños. Esto extrae el cuadro informativo del contenedor y lo inyecta en el `body` principal, evitando que sea cortado por el límite de la caja (`overflow: hidden`).


## Actualizaciones V3 (Limpieza Tab 3 — Sesión 2026-10-10)

### Cambios aplicados en Tab 3 — INTELIGENCIA ESTRATÉGICA
- **Eliminado**: Panel "Eficacia de Pagos por Resolución" (`intChartRes`) — era redundante con el Ranking de Ejecución Financiera dinámico del Tab 1.
- **Eliminado**: Panel "Ranking de Ineficiencia: Top 15 Ciudades" (`intChartCiudades`) — era redundante con el botón "TASA DEUDA %" del panel Avance Top Ciudades en Tab 1.
- **Modificado**: Sunburst expandido a ancho completo (`col-span-12`) con altura dinámica `calc(100vh - 160px)`.
- **Nueva jerarquía del Sunburst**: `TIPO_NOVEDAD → CIUDAD` donde el valor de cada hoja es el **$ pendiente bloqueado** por esa causa en esa ciudad. Excluye "NINGUNA". Antes mostraba `PAGADO/PENDIENTE → EstadoActual → Ciudad` (sin valor económico real).
- El Sunburst ahora tiene `nodeClick: 'rootToNode'` para drill-down interactivo y tooltips con `formatMoney`.

### Análisis de redundancias Tab 3 vs Tab 1
| Gráfico eliminado (Tab 3) | Equivalente en Tab 1 |
|---|---|
| Eficacia de Pagos por Resolución | Ranking Ejecución Financiera (dinámico, responde a Sankey) |
| Ranking Ineficiencia Top 15 ciudades | Avance Top Ciudades → botón "TASA DEUDA %" |

### Estado de Tabs 4 y 5 (pendiente de decisión)
- **Tab 4 (view_estadistica)**: Existe en HTML pero sin botón de navegación (tab huérfano). Contiene 5 sub-análisis: Defect Rate, Riesgo Financiero ($real), Efectividad Territorial, Cuellos Botella (MOCKEADO con Math.random()), Funnel de Pagos.
- **Tab 5 (Visión Ejecutiva)**: Pareto 80/20 (real), Tiempo Promedio (MOCKEADO), Tendencia Anomalías (MOCKEADO con meses random de 2023).
- Los análisis reales de Tab 4 (Riesgo Financiero, Funnel) son candidatos a rescatar. Los mockeados requieren campos de fecha reales.

### Backup creado
- `frontend_backup_20261010_pre_tab3_cleanup.html` — estado previo a esta sesión.

## Pipeline Backend (ETL Python en server.py)
Es vital entender cómo se transforman los datos de Excel a JSON antes de modificar el `frontend.html`. El archivo `server.py` no es un simple servidor estático, contiene un motor ETL en Pandas que se ejecuta al vuelo:
1. **Detección Automática**: Usa `glob` para encontrar el archivo de Excel más reciente que empiece por `BALANCE DE PAGOS *.xlsx`.
2. **Consolidación de Hojas**: Lee todas las hojas (pestañas) saltándose 2 filas de header. Agrega la columna `RESOLUCION` mapeando el nombre de la hoja original para unificar la base de datos.
3. **Melt (Unpivot)**: Toma las columnas horizontales de pagos (`VALOR A PAGAR`, `.1`, `.2`, etc.) y hace un "unpivot" convirtiéndolas en filas bajo dos nuevas columnas: `PERIODO_PAGO` y `VALOR_PAGADO`.
4. **Limpieza**: Renombra `.1` a `PAGO 2`, etc., y elimina los registros donde el valor pagado es nulo (`dropna`). El output en memoria RAM se sirve como un array de objetos JSON por el endpoint `/api/data`.

---

## Actualizaciones V4 (Tab 3 Reestructura Completa — Sesión 2026-10-10/11)

### Restructura layout Tab 3
- **Sunburst eliminado**: No aportaba valor analítico suficiente.
- **Layout 2 filas flex sin scroll**: Fila 1 (`flex:3`) = Pareto + Radar + Heatmap. Fila 2 (`flex:2`) = Arrendadores + Dist. Pagos + Flujo Pagos.
- **KPI strip de 5 paneles** (`grid-cols-5`): BENS. CON NOVEDAD · NOVEDAD MÁS FRECUENTE · $ TOTAL BLOQUEADO · ARRENDADOR MAYOR RIESGO · TOTAL BENEFICIARIOS.

### Radar "Salud Ciudades"
- Reconstruido como **5 series independientes** (una por ciudad) para que ECharts detecte hover por ciudad individualmente.
- Tooltip usa `p.seriesName` para identificar la ciudad y mostrar datos correctos.
- Indicadores: `% EJECUCIÓN`, `PRESUPUESTO (REL.)`, `BENEFICIARIOS (REL.)` — todos normalizados 0–100%.
- Radio aumentado a `80%`, centro `['50%','56%']`.

### Pareto
- Eliminado botón TOP10/TOP20/TODAS — siempre muestra todas las ciudades.

### Heatmap (Matriz de Novedades)
- Color dinámico de etiqueta: texto oscuro (`#030610`) en celdas claras (< 60% del máx), blanco en celdas saturadas (≥ 60%).
- Columna "NINGUNA" eliminada.
- Scroll con rueda del mouse (dataZoom inside).

---

## Actualizaciones V5 (KPIs y Pulido Final — Sesión 2026-10-13/14)

### Strip de 5 KPIs — ajustes de layout y texto
| KPI | Cambio |
|---|---|
| **BENS. CON NOVEDAD** | Subtexto "0 de 0" apila *debajo* del porcentaje (`flex-col`) en vez de en línea |
| **NOVEDAD MÁS FRECUENTE** | Nombre de novedad completo (sin truncar a 14 chars); casos debajo del nombre |
| **$ TOTAL BLOQUEADO** | "en novedad" apila debajo del monto (`flex-col`) |
| **ARRENDADOR MAYOR RIESGO** | Nombre completo (sin truncar); contador cambia de "N bens." → "N con novedad" |
| **TOTAL BENEFICIARIOS** | "beneficiarios" (sin abreviatura) apila debajo del número (`flex-col`) |

### Radar — etiquetas de vértices
- `axisName.fontSize`: 10 → **13** (los nombres `% EJECUCIÓN`, `PRESUPUESTO (REL.)`, `BENEFICIARIOS (REL.)` son más legibles).

### Export a Excel
- Botón **EXPORTAR XLS** en Tab 3: genera archivo XML `.xls` con los beneficiarios filtrados activos (novedades + datos clave).
- Lógica de acumulación inteligente: si el filtro muestra todos los periodos (ACUMULADO), exporta el pago más reciente por beneficiario; si hay un periodo específico, exporta ese periodo.

### Backup de esta sesión
- `frontend_backup_20261013_export_xls.html` — estado previo al export XLS.
- `frontend_backup_20261014_kpi_subtitles_radar_labels.html` — estado luego de ajustes V5.
