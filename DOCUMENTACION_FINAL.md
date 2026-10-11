

## 2026-10-10: Ajustes Menores — KPI Bars Dinámicas y Botones Tab 3

### KPI Strip — Barras dinámicas
Los 3 KPIs que tenían barra estática (siempre al 100%) ahora se actualizan con cada filtro:
- **Impacto Novedades** (`lineImpacto`): muestra `dinBloq / pendientes * 100` — qué proporción del pendiente total está bloqueada por novedades.
- **Ciudad Más Crítica** (`lineCiudad`): muestra `ciuDeuda[tc].p / pendientes * 100` — el peso de esa ciudad sobre el total pendiente.
- **Resolución Eficiente** (`lineRes`): muestra el `% pagado` de esa resolución (ya calculado como `rRate`).
- Todas tienen `transition-all duration-1000` para animación suave al filtrar.

### Botones Tab 3 — Estilo unificado visible
Los tres botones de control de Tab 3 pasaron de `text-gray-500` (gris inactivo, solo hover coloreado) a tener color visible permanente con su color semántico:
- **↺ REINICIAR** (Sunburst): `border-[#00ccff] text-[#00ccff]`
- **TOP 20** (Pareto): `border-[#bf00ff] text-[#bf00ff]`
- **ACUMULADO** (Flujo Pagos): `border-[#00ff88] text-[#00ff88]`
- Todos con `hover:bg-color/10` para feedback de interacción.

### Backup
`frontend_backup_20261010_ajustes_menores.html`

---

## 2026-10-10: Unificación Visual Tab 1 — Colores Semánticos, Estilos y Nuevos Controles

### AVANCE TOP CIUDADES
- **Color por tasa de deuda**: las barras ya no son todas cyan. Se colorean según `% pendiente/total` de cada ciudad: rojo `#ff0033` si >80%, naranja `#ff5e00` si >60%, amarillo `#ffcc00` si >40%, verde `#00ff88` si ≤40%. Aplica en ambos modos (VOLUMEN y TASA DEUDA). Ciudades filtradas/dimmed se muestran en cyan tenue `rgba(0,204,255,0.1)`.
- **Leyenda de colores**: se añadió una fila de píldoras de colores debajo del header con la descripción `COLOR = % PEND: 🔴 >80% 🟠 >60% 🟡 >40% 🟢 <40%`, aclarando la semántica.

### NOVEDADES — IMPACTO & FRECUENCIA
- **Más compacto**: ítems visibles en dataZoom aumentados de 8 a 12, `barCategoryGap` reducido a `'12%'` (antes default 20%). Las barras quedan más juntas e igualadas visualmente con AVANCE.

### RANKING EJECUCIÓN FINANCIERA
- **Estilo cyberpunk**: `Pagado` usa `LinearGradient(1,0,0,0, #00ff88 → rgba(0,255,136,0.15))`. `Pendiente` usa `LinearGradient(1,0,0,0, #ff5e00 → rgba(255,94,0,0.15))` con `borderRadius:[0,4,4,0]` en la punta.
- **% ejecutado visible**: label en la serie Pendiente (posición 'right') muestra el % pagado de cada barra (ej. `87%`). `grid.right` aumentado a 48px para dar espacio.

### FLUJO DE CAPITAL (Sankey)
- **Botón TOP 10 / TODAS**: añadido en el header del panel. Variable global `sankeyTopN` (null = todas). Al activar, filtra `tempLvl1` a los 10 nodos de mayor valor y propaga el filtro a los nodos nivel 2 y links. El botón cambia a verde cuando está activo.

### Backup
`frontend_backup_20261010_colores_tab1.html`

---

## 2026-10-10: Restructura Final de los 3 Tabs — Distribución Estratégica de Gráficos

### Tab 1 — OPERACIÓN DIARIA
- **Fila superior (col-12):** AVANCE TOP CIUDADES (col-4) · MAPA (col-2) · **NOVEDADES — IMPACTO & FRECUENCIA** (col-6, nuevo).
- El nuevo chart `chartNovedadCombo` fusiona los anteriores "TIPO NOVEDAD" (conteo de casos) e "IMPACTO FINANCIERO" ($ bloqueado) en un solo gráfico de barras horizontales, donde la longitud de la barra = $ bloqueado y la etiqueta muestra `$ · N casos`. El color codifica la severidad: rojo >70%, naranja >40%, amarillo >20%, cyan por defecto.
- Se eliminó el gráfico **TENDENCIA FLUJO M.** (lineChart), que usaba datos sin filtrar y no respondía a los filtros. Reemplazado por `chartFlujoPagos` en Tab 3.
- **Fila inferior (col-12):** FLUJO DE CAPITAL Sankey (col-9) · RANKING EJECUCIÓN FINANCIERA (col-3, altura completa).

### Tab 2 — ANÁLISIS DE EJECUCIÓN
- Se eliminaron los paneles `execRadar` y `execHeatmap` que ocupaban la fila inferior, ya que pertenecen temáticamente a Inteligencia Estratégica (Tab 3).
- Ahora contiene únicamente: KPI strip (5 tarjetas) + MAPA DE RED GEOGRÁFICO + TABLA DE DATOS (ancho completo, `flex-1`).
- Layout cambiado de `grid grid-cols-12 grid-rows-2` a `flex flex-col` para la tabla.

### Tab 3 — INTELIGENCIA ESTRATÉGICA (Restructura completa)
**Strip de 4 KPIs estratégicos (nuevo):**
1. **% CON NOVEDAD** — porcentaje y conteo de beneficiarios únicos con novedad activa (excluyendo NINGUNA). Barra de progreso en rojo.
2. **$ TOTAL BLOQUEADO** — suma de `col.pend` por beneficiario único (primer ocurrencia para evitar duplicados por melt).
3. **NOVEDAD MÁS FRECUENTE** — nombre y conteo de la novedad que más veces aparece.
4. **ARRENDADOR DE MAYOR RIESGO** — arrendador con más beneficiarios activos con novedad, y el conteo.

**Fila 1:** execSunburst (col-6, con botón ↺ REINICIAR que llama `resetSunburst()`) + visionChartPareto (col-6, con botón TOP 10/TOP 20 toggle que llama `toggleParetoTop()`).

**Fila 2 (movido desde Tab 2):** execRadar (col-6) + execHeatmap (col-6). Seguro porque `renderExecCharts()` se llama incondicionalmente en `updateDashboard()` y `switchTab()` hace `resize()` en todos los charts.

**Fila 3 (sin cambios):** chartArrendadores (col-5) + chartDistPagos (col-7).

**Fila 4 (nuevo):** `chartFlujoPagos` (col-12, h-320px) — Flujo acumulado de pagos por periodo (PAGO 1–12). Dual Y-axes: $ pagado (izquierda, barras verdes) + beneficiarios activos (derecha, línea punteada cyan). Botón **ACUMULADO / POR PERIODO** toggle que llama `toggleFlujoModo()` y cambia entre barras por periodo y área acumulada.

### Variables y funciones nuevas
- `let paretoTopN = 10;` — global, controla cuántas ciudades muestra el Pareto. Toggle entre 10 y 20 con `toggleParetoTop()`.
- `resetSunburst()` — re-renderiza el sunburst al nivel raíz.
- `toggleParetoTop()` — alterna entre TOP 10 / TOP 20 en el Pareto y llama `updateDashboard()`.
- `toggleFlujoModo()` — alterna `data-modo` entre `periodo` y `acum` en el botón del chartFlujoPagos.

### Bug crítico corregido
`charts.line` fue eliminado de `init()` (al remover TENDENCIA FLUJO de Tab 1), pero `updatePyramidChart()` seguía siendo llamada desde `updateDashboard()` línea 2955 y hacía `charts.line.setOption(...)` sin guard, lanzando un **TypeError que abortaba silenciosamente todo el render** de `updateDashboard()`. Corregido añadiendo `if(!charts.line) return;` en `updatePyramidChart()`.

---

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

## Pestaña 4: Estadística Avanzada
Esta pestaña consolida las 5 métricas estadísticas operativas clave mediante un sub-menú de navegación rápida:
1. **Defect Rate (Tasa de Incidencia):** Porcentaje de beneficiarios con novedades críticas.
2. **Riesgo Financiero:** Exposición monetaria exacta clasificada por tipo de novedad.
3. **Efectividad Territorial:** Ranking porcentual de pago por ciudad (Top Mejores y Peores).
4. **Cuellos de Botella:** Días promedio de estancamiento operativo.
5. **Funnel de Pagos (Deserción):** Caída de usuarios activos entre el Periodo 1 y los periodos subsecuentes.

## Pestaña 5: Visión Ejecutiva (Proyecciones)
Diseñada exclusivamente para la alta gerencia, incluye gráficos de planificación estratégica:
1. **Curva de Pareto de Concentración (80/20):** Combina barras (Deuda absoluta) y una línea (% acumulado). Revela rápidamente si el 80% del dinero bloqueado está concentrado en un puñado de ciudades para focalizar esfuerzos.
2. **Tiempo Promedio de Cierre:** Gauge chart (Tacómetro) que mide la agilidad de los cierres (en meses).
3. **Tendencia de Anomalías Sistémicas (Histórico):** Gráfico de líneas (Time-series) que compara el total de registros contra la aparición de nuevas novedades, vital para detectar si un problema es estacionario o está empeorando mes a mes.
