

## 2026-10-13: Export a Excel XML (.xls) — Solución definitiva separadores y acumulación

### Problema resuelto — BOGOTÁ, D.C. se partía en dos columnas al abrir el CSV
- **Causa raíz**: el nombre de ciudad `BOGOTÁ, D.C.` contiene `,` y `;`. Ningún separador CSV era seguro porque alguno de los dos caracteres aparecía en los datos, causando que Excel partiera la celda aunque los valores estuvieran entre comillas.
- **Solución definitiva**: se reemplazó el formato CSV por **Excel XML Spreadsheet** (formato SpreadsheetML `.xls`). Los valores van dentro de etiquetas XML `<Data ss:Type="String">`, sin separadores. Ningún carácter en los datos puede causar splits.
- **Ambos botones cambiados**: DATA exporta `Semilleros_TODOS_<fecha>.xls`, FILTRADOS exporta `Semilleros_FILTRADOS_<fecha>.xls`.

### Bug fix — Columnas vacías en export (col.estAct y otras asignadas tarde)
- **Causa raíz**: `col.estAct`, `col.pend`, `col.valMen`, `col.arrDoc`, `col.arrNom`, `col.fecIni`, `col.id`, `col.docPpt` se asignaban **después** del loop `allData.forEach` de normalización. Dentro del loop, `col.estAct` era `undefined`, así que `d[undefined]` = `d['']` nunca se normalizaba.
- **Solución**: todas esas asignaciones se movieron **antes** del `forEach`.

### Nueva funcionalidad — Acumulación inteligente en export FILTRADOS (1 fila por beneficiario)
El export FILTRADOS deduplica a una fila por beneficiario. Se mejoró cómo se consolidan las columnas que pueden variar entre cuotas:

| Columna | Comportamiento anterior | Comportamiento nuevo |
|---|---|---|
| OBSERVACIONES | Primera no vacía | Todas únicas acumuladas con ` \| ` |
| TIPO NOVEDAD | Última fila | Todos los tipos únicos con ` \| ` |
| FECHA NOVEDAD | Primera fila | **Último** valor no vacío |
| ESTADO ACTUAL | Primera fila | **Último** valor no vacío |
| LEGALIZADO | Primer no vacío | **Último** valor no vacío |

### Backup
`frontend_backup_20261013_export_xls.html`

---

## 2026-10-11: Filtros CIUDAD y TIPO NOVEDAD — Opción "TODAS (excl. X)"

### Nueva funcionalidad — Acción rápida en dropdowns multi-select
- **Contexto**: los filtros CIUDAD y TIPO NOVEDAD son multi-select personalizados. El estado por defecto (ningún checkbox marcado) equivale a "TODAS" e incluye `SIN CIUDAD` y `NINGUNA`.
- **Problema**: no había forma rápida de seleccionar todo el universo **excepto** los registros sin ciudad asignada o sin novedad activa.
- **Solución**: se modificó `initMultiSelect(selectId, defaultText, opts)` para aceptar `opts.excludeVal`. Si se provee, inserta una fila de acción rápida al tope del dropdown con estilo amarillo `#ffcc00`:
  - Texto: `◉ TODAS (excl. <excludeVal>)`
  - Al hacer clic: marca todos los checkboxes del menú **excepto** el de `excludeVal`, actualiza el botón a `N SELECCIONES` y llama `applyFilters()`.
- **CIUDAD** inicializado con `{ excludeVal: 'SIN CIUDAD' }` → `◉ TODAS (excl. SIN CIUDAD)`
- **TIPO NOVEDAD** inicializado con `{ excludeVal: 'NINGUNA' }` → `◉ TODAS (excl. NINGUNA)`
- Los demás filtros (RESOLUCIÓN, PERIODO, ESTADO ACTUAL, ESTADO PAGO) no reciben `excludeVal` y no cambian.
- **Compatibilidad**: el resultado de `getCustomValues()` devuelve un array con todos los valores seleccionados (todos menos el excluido), que ya era manejado correctamente por `applyFilters()` a través de `Array.isArray(f.ciu) ? f.ciu.includes(...)`.

### Backup
`frontend_backup_20261011_filtros_excl.html`

---

## 2026-10-11: Tab 2 Mapa — SIN CIUDAD siempre visible + Leyenda esquina superior izquierda

### Bug fix — Punto SIN CIUDAD no aparecía en el mapa Tab 2
- **Causa raíz**: la serie `effectScatter` de SIN CIUDAD usaba `data: sinCiuDataT2.map(...)`. Si no hay registros con ciudad vacía en el dataset filtrado, `sinCiuDataT2 = []` y la serie no renderiza nada.
- **Solución**: separar la lógica de datos de la lógica de render. Se crea `sinCiuEntry` con los valores reales si existen, o `{ total:0, pagado:0, pendiente:0 }` como fallback. `sinCiuSeriesData` es siempre un array de 1 elemento en `[-73.5, 4.3]`.
- **Resultado**: el punto púrpura `#bf00ff` con ripple y label "SIN\nCIUDAD" siempre aparece en el mapa Tab 2, tenga o no datos.

### Fix — Leyenda (visualMap) del mapa Tab 2 estaba en el centro del mapa
- **Causa**: `orient: 'horizontal', left: 'center', bottom: 4` centraba la leyenda horizontalmente y la anclaba al fondo del contenedor ECharts — que es el centro visual del panel cuando el mapa ocupa solo parte de la altura.
- **Solución**: cambiado a `orient: 'vertical', left: 8, top: 8` — esquina superior izquierda, igual al posicionamiento de la leyenda del Tab 1. `itemWidth: 7, itemHeight: 60`.

### Backup
`frontend_backup_20261011_tab2_mapa_sincuidad.html`

---

## 2026-10-11: Rediseño Completo Tab 2 — Unificación Visual con Tab 1

### KPI Strip — Formato unificado Tab 1
- Los 5 KPIs del Tab 2 fueron reescritos completamente con el mismo markup de Tab 1: `p-2`, `text-[9px]` título, `text-lg` valor principal, círculo SVG `w-8 h-8` con `r=14 stroke-width=3 dasharray=87.96`, texto interior `text-[7px]`, barra `h-1 mt-1.5`.
- El círculo de progreso fue corregido: `dashoffset = 87.96 - (87.96 * pct) / 100` (antes usaba 125.6 de un `r=20` más grande).
- **KPI 2 renombrado**: "PAGOS/REGISTROS" (púrpura) → **"REGISTROS TOTALES"** (cyan `#00ccff`). El valor muestra total de registros tras unpivot.
- **KPI 3 (AVANCE PAGOS)**: reformateado como dual-stat (% pagado + $ pagado / % pendiente + $ pendiente). IDs actualizados: `t2_kpiAvancePct`, `t2_kpiAvancePagado`, `t2_kpiAvancePendPct`, `t2_kpiAvancePendiente`, `t2_kpiAvanceBar`. Guard JS cambiado de `t2_kpiAvance` → `t2_kpiAvancePct`.
- Todos los 5 KPIs tienen tooltip ⓘ (sistema `#globalTip`).

### Mapa Tab 2 — SIN CIUDAD visible
- **Bug corregido**: `renderTab2Map()` excluía explícitamente `SIN CIUDAD` con `ciu !== 'SIN CIUDAD'`. Removida la exclusión.
- Separación en dos arrays: `realCitiesT2` (todas menos SIN CIUDAD) + `sinCiuDataT2` (solo SIN CIUDAD).
- Añadida **3ª serie `effectScatter`** de color púrpura `#bf00ff` con ripple, posición fija `[-73.5, 4.3]` (dentro del bounding `[[-76.8, 11.3], [-70.5, 3.2]]`). Label "SIN\nCIUDAD" en `position: 'right'`.
- La coordenada original de SIN CIUDAD `[-74.08, 3.20]` estaba en el borde del bounding; el punto fijo `[-73.5, 4.3]` garantiza visibilidad.

### Panel headers Tab 2 — Renombrados + tooltips ⓘ
- **EJECUCIÓN REGIONAL TERRITORIAL**: ⓘ añadido al título.
- **PROPORCIÓN DE EJECUCIÓN** (treemap): ⓘ añadido, subtítulo movido a `text-gray-500` separado.
- **TERMINAL_BASE_DE_DATOS** → **"BASE DE DATOS · SEMILLEROS"** en cyan `#00ccff` + ⓘ.
- El innerHTML del título del mapa en `renderTab2Map()` fue actualizado para incluir el ⓘ.

### Backup
`frontend_backup_20261011_tab2_redesign.html`

---

## 2026-10-10: Tooltips ⓘ Funcionales + Sankey → RANKING Click-to-Focus

### Bug fix — Tooltips ⓘ recortados por `clip-path` de `.cyber-panel`
- **Causa raíz**: `.cyber-panel` tiene `clip-path: polygon(...)` que recorta TODOS sus descendientes, incluyendo `position: fixed`. No hay escape CSS posible.
- **Solución**: Crear un singleton `<div id="globalTip">` directamente en JS con `document.createElement` + `document.body.appendChild`. Al estar en `<body>` a nivel raíz, escapa cualquier `clip-path` ancestro.
- **Flujo**: `mouseenter` en `.ptip` → copia `innerHTML` de `.ptip-box` (siempre `display:none !important`, solo almacén) → lo pega en `#globalTip` → lo posiciona con `getBoundingClientRect()` → `display:block`. `mouseleave` → `display:none`.
- **Intentos fallidos previos**: `position: fixed` + posicionador JS (sigue recortado por clip-path). `setTimeout(0)` para defer DOM (el div `#globalTip` estático en HTML aún no existe cuando corre el setTimeout en algunos browsers). La solución correcta fue crear el div en JS.

### Funcionalidad — Sankey click resalta resolución en RANKING
- Al hacer click en un nodo del Sankey, `activeSankeyNode` se setea (ya existía este mecanismo).
- **Nuevo**: `renderExecutionView()` ahora calcula `highlightBarName`: limpia sufijos `(Ciu)` / `(Res)` del nodo clickeado y busca match en `barData`.
- Si hay match: las barras no relacionadas en `chartBarExec` se dimean a `rgba(..., 0.06)` (casi invisibles). La barra resaltada mantiene su gradiente original.
- `dispatchAction` hace scroll automático del dataZoom del RANKING para centrar la resolución resaltada (`startValue: hIdx-3`, `endValue: hIdx+6`).
- Click en el mismo nodo o en un edge deselecciona y el RANKING vuelve al estado normal.
- Funciona en ambos modos: `res_ciu` (nodo lvl1 = resolución directa) y `ciu_res` (nodo lvl2 con sufijo `(Res)` → se limpia para match).

### Código muerto removido
- Atributo `style="left:auto;right:0;"` en `.ptip-box` del RANKING — sin efecto con el nuevo sistema globalTip.

### Backup
`frontend_backup_20261010_tooltips_sankey_ranking.html`

---

## 2026-10-10: Leyendas Visibles en Todos los Paneles + Mapa Mejorado

### AVANCE TOP CIUDADES — Leyenda realzada
- Píldoras de color 10×10px con `box-shadow` glow neón por nivel de deuda pendiente.
- Texto coloreado con el mismo color semántico del nivel (rojo/naranja/amarillo/verde), tamaño 9px (antes 8px color `#4a5f7a` casi invisible).
- Backup: `frontend_backup_20261010_leyendas.html`

### NOVEDADES — IMPACTO & FRECUENCIA — Nueva leyenda
- Fila `IMPACTO: >70% | >40% | >20% | resto` añadida debajo del panel-header.
- Colores exactamente los mismos que el `novGradient()` del chart: `#ff0033 / #ff5e00 / #ffcc00 / #00ccff`.

### FLUJO DE CAPITAL (Sankey) — Nueva leyenda inline
- Leyenda `EJECUCIÓN: 100% | ≥50% | <50% | TOTAL` integrada en el header junto al título.
- Colores coinciden con la lógica del nodo en `renderExecutionView()`: `#00ff88 / #ffcc00 / #ff5e00 / #00ccff`.

### Mapa — Leyenda y labels de ciudades
- `visualMap` cambiado de vertical arriba-izquierda a **horizontal centrado** (`orient:'horizontal'`, `left:'center'`, `bottom:4`).
- Texto eliminado `'Mayor $' / 'Menor $'`; reemplazado por valores enteros reales con `toLocaleString('es-CO')`.
- Color de texto: `#c8ddf0` (antes `#7890b5` apagado).
- Labels de ciudades: ahora muestran nombre + valor abreviado en dos líneas (`formatMoneyShort`), color `#e0ecff`.

### Bug fix crítico — SyntaxError `let topCiuArr` duplicado
- Al añadir las barras dinámicas de KPI, el bloque original `// Top Ciudad` con `let topCiuArr` quedó sin eliminar.
- El bloque nuevo también declaraba `let topCiuArr` en el mismo scope → **SyntaxError** que cancelaba todo el script.
- Fix: eliminado el bloque duplicado original (líneas ~3216-3225). El bloque nuevo gestiona tanto la ciudad como la barra dinámica `lineCiudad`.

---

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
