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

---

## Actualizaciones V6 (Leyendas, KPI orden, Pareto — Sesión 2026-10-14)

### Radar SALUD CIUDADES
- **Centro bajado**: `['50%', '55%']` → `['50%', '62%']` — el triángulo queda más pegado a los labels inferiores (PRESUPUESTO/BENEFICIARIOS).
- **Leyenda ampliada**: fontSize 7 → **10**, itemWidth 8 → **13**, itemHeight 5 → **9**, top 2 → 4.

### Leyendas y textos en todos los artefactos
| Artefacto | Cambio |
|---|---|
| Heatmap (Matriz Novedades) | yAxis fontSize 8 → **9**; visualMap fontSize 7 → **9**, items 12×8 → 14×10; label celdas fontSize 8 → **9** |
| Heatmap xAxis | Revertido a fontSize 7 (las etiquetas rotadas 42° se desbordaban con 9) |
| Pareto (Concentración Deuda) | Leyenda fontSize 8 → **10**, items 10×6 → 13×9; ejes Y nameTextStyle y axisLabel fontSize 8 → **9** |
| Mapas Tab 1 y Tab 2 | Scatter city labels fontSize 7.5 → **9**; barra de color (visualMap) fontSize 7 → **9** |
| labRadar (Tab 4) | axisName fontSize 9 → **11** |

### Strip KPIs Tab 3 — reorden
- **TOTAL BENEFICIARIOS** movido a la primera posición (antes era el último).
- Nuevo orden: TOTAL BENEFICIARIOS · BENS. CON NOVEDAD · NOVEDAD MÁS FRECUENTE · $ TOTAL BLOQUEADO · ARRENDADOR MAYOR RIESGO.

### Pareto — aprovechamiento vertical
- Grid: `bottom: '12%'` → **`'3%'`**, `top: '20%'` → **`'14%'`** (con `containLabel: true` ECharts ajusta las etiquetas solas; el área de barras ocupa casi todo el panel).
- Label "80%": posición `insideEndTop` (arriba de la línea punteada, extremo derecho) para no montarse sobre el "100%" del eje derecho.

### Backup de esta sesión
- `frontend_backup_20261014_legends_kpi_pareto.html` — estado luego de ajustes V6 iniciales.
- `frontend_backup_20261014_v6_colores_leyendas.html` — estado luego de ajustes V6 finales (ver V6b abajo).

---

## Actualizaciones V6b (Colores, Leyendas, Tooltips — Sesión 2026-10-14 continuación)

### Concentración Arrendadores
- Barras "Sin novedad": color magenta → **cian** (`#00ccff`) con gradiente, `borderRadius: [0,4,4,0]`.
- Barras "Con novedad": gradiente naranja con `borderRadius: [0,4,4,0]`.
- Labels de barras: color `#fff` → **`#ff5e00`** (naranja, igual que la serie).
- Leyenda: fontSize 8 → **10**, items 10×6 → **13×9**.
- Tooltip border: magenta → **cian**.

### Concentración de Deuda — Pareto
- Barras: gradiente magenta → **cian** (`#00ccff` → fade), `borderRadius: [5,5,0,0]`.
- Label 80%: `position: 'insideEndTop'` (arriba de la línea, extremo derecho).
- Grid: `bottom: '3%'`, `top: '14%'` (más aprovechamiento vertical).
- Leyenda Pareto: fontSize 8 → **10**, items 10×6 → **13×9**.

### Distribución de Pagos
- Labels sobre barras: fontSize 8 → **11**, color `#ccc` → **`#e0ecff`**.

### KPIs Tab 3 — compactación
- Subtextos (beneficiarios, de 0, en novedad, casos, con novedad): de `flex-col` → **`flex items-baseline gap-1`** (al lado del número, igual que Tab 1 y 2).

### Cuadraditos de panel (indicadores de color)
- CONCENTRACIÓN DE DEUDA: `■ magenta` → **`■ cian`** (alineado con barras).
- CONCENTRACIÓN ARRENDADORES: `■ magenta` → **`■ cian`** (alineado con barras).

### Tooltips ptip actualizados
| Panel | Cambio |
|---|---|
| Concentración Deuda 80/20 | "línea naranja" → "línea verde"; barras descritas como cian |
| Concentración Arrendadores | Colores actualizados (cian/naranja); descripción del número naranja |
| Salud Ciudades | Explicación de REL.: porcentaje relativo al máximo de las ciudades mostradas |

### Radar SALUD CIUDADES — tooltip
- Línea "Presup.(Rel.)" ahora incluye valor absoluto: `32% del máx · $3,169,399,875`.

---

## V7 — Filtros Activos con Highlight Naranja (14 oct 2026)
**Backup:** `frontend_backup_20261014_filtros_activos.html`

### Problema resuelto
Al navegar entre tabs con filtros activos, no había indicación visual de que un filtro seguía aplicado. El usuario podía estar viendo datos filtrados sin saberlo.

### Implementación
Nueva función `applyFilterBtnStyle(btn, isActive)` (justo antes de `initMultiSelect`):
- **Activo** → `borderColor: #ff5e00`, `color: #ff5e00`, `boxShadow: 0 0 8px rgba(255,94,0,0.35)`
- **Inactivo** → limpia estilos inline (Tailwind recupera `text-[#00ff88] border-[#1f2940]`)

Llamada en 5 puntos dentro de `initMultiSelect`:
| Punto | Cuándo | isActive |
|---|---|---|
| `cb.onchange` | usuario marca/desmarca checkbox | `checked.length > 0` |
| `quickRow.onclick` | "TODAS (excl. X)" | `true` |
| `select.resetCustom` | BORRAR o reset programático | `false` |
| `select.setCustomValue` | asignación programática de 1 valor | `true` |
| `select.selectCustom` | clic en mapa/barra activa filtro | `true` |

Aplica a los 6 filtros: RESOLUCIÓN, CIUDAD, PERIODO, TIPO NOVEDAD, ESTADO ACTUAL, ESTADO PAGO.

---

## V8 — Bug fixes, Tab 2 KPI redesign, círculos legibles (14 oct 2026)
**Backup:** `frontend_backup_20261014_kpis_circles_fix.html`

### Bug: IMPACTO NOVEDADES (Tab 1 KPI 3) — conteo 8-9× inflado
**Causa:** el formato "melt" del ETL genera ~9 filas por beneficiario (una por periodo de pago). `dinBloq` sumaba el valor `PENDIENTE` por cada fila, multiplicando el monto real 8-9 veces.
**Fix:** Set `dinBloqSeen` que registra `docKey = DOC_PPT + novedad`; sólo acumula la primera ocurrencia por par (beneficiario × tipo_novedad).
- Valor antes: ~$1,279,236,500 (ficticio) → Valor después: $142,248,500 (coincide con Tab 3 `$ TOTAL BLOQUEADO` ✓).

### Tab 2 (ANÁLISIS DE EJECUCIÓN) — rediseño de KPIs
Los 5 KPIs del strip de Tab 2 rediseñados con cálculos reales:

| KPI | Título anterior | Título nuevo | Cálculo |
|---|---|---|---|
| KPI 1 | BENEFICIARIOS ÚNICOS | BENEFICIARIOS ÚNICOS | sin cambio (% filtrado/total) |
| KPI 2 | REGISTROS TOTALES | **PAGOS REALIZADOS** | filas con `VALOR_PAGADO > 0` |
| KPI 3 | sin cambio | sin cambio | sin cambio |
| KPI 4 | TIPO NOV: [span] | **BENS CON NOVEDAD** | Set único de DOC_PPT con novedad ≠ NINGUNA → tamaño/currentBen |
| KPI 5 | ESTADO: [span] | **CIUDAD TOP** | ciudad con mayor ratio `pagos/total` en el filtro activo |

- KPI 5 subtexto (`t2_kpiEstTot`): muestra `"xx.x% ejecución"` (tasa de la ciudad top).

### Tab 2 — círculos KPI: texto legible
- Tamaño de fuente: `text-[7px]` → **`text-[9px]`** en todos los círculos del strip.
- Añadido **`whitespace-nowrap`** para evitar que valores como "100%" se partan en 2 líneas dentro del círculo de 32px.
- **Tab 1** `circBenText`: cambio de `.toFixed(1)` → **`.toFixed(0)`** (eliminaba el decimal "88.0%" que se veía extraño en el círculo).

### Tab ESTADÍSTICA — eliminada
- La 5ª pestaña ("ESTADÍSTICA") fue activada temporalmente para revisión y luego removida (botón de navegación eliminado del nav).
- El `div#view_estadistica` permanece en el HTML pero inaccesible; sus KPIs tenían el mismo bug de `dinBloq` duplicado.

### Radar Tab 3 — radio recortado
- `radius: '80%'` → **`'62%'`** para que las etiquetas de los vértices no queden cortadas por el borde del panel.

---

## V9 — Etiquetas completas y % visibles en subtítulos (14 oct 2026)
**Backup:** `frontend_backup_20261014_benef_pct_labels.html`

### Sin abreviatura "BENS" en ningún tab
| Tab | Antes | Después |
|---|---|---|
| Tab 2 KPI 4 | `BENS CON NOVEDAD` | `BENEFICIARIOS CON NOVEDAD` |
| Tab 3 KPI 2 | `BENS. CON NOVEDAD` | `BENEFICIARIOS CON NOVEDAD` |

Tab 1 ya usaba "BENEFICIARIOS ÚNICOS" completo — sin cambio.

### Porcentajes como texto en subtítulos Tab 2
Patrón estandarizado para KPIs de conteo en Tab 2: número absoluto grande + subtítulo gris `"de N · X%"`.
Antes el % sólo aparecía en el círculo de 32px (difícil de leer). Ahora también como texto en el subtítulo gris.

| KPI | Subtítulo antes | Subtítulo después |
|---|---|---|
| BENEFICIARIOS ÚNICOS | `de 1,873` | `de 1,873 · 100%` |
| PAGOS REALIZADOS | `de 16,580` | `de 16,580 · 100%` |
| BENEFICIARIOS CON NOVEDAD | `de 1,873` | `de 1,873 · 2%` |

El círculo se mantiene como indicador visual; el subtítulo es la lectura rápida.

---

## V10 — Tab 4 rediseño + porcentajes Tab 1/3 + correcciones (14 oct 2026)
**Backup:** `frontend_backup_20261014_tab4_redesign.html`

### Tab 4 SEGUIMIENTO Y ALERTAS — rediseño completo
- **KPI strip**: Mismo estilo que Tab 1/2/3 — `text-lg` + círculo gauge + subtítulo `de N` + barra inferior + borde izquierdo de color. Eliminado el `text-[34px]` desproporcionado anterior.
- **Círculos KPI**: Muestran qué % del total (1983 bens) está en cada nivel: 🚨0.9% · 🔴47.8% · 🟡51.2% · 🟢0.2%
- **Layout cuerpo**: `flex-row` con columna izquierda `33%` (gráficas apiladas) y columna derecha `flex-1` (tabla).
- **Gráficas**: Pipeline (encima) + Distribución días (debajo), cada una `flex-1 min-h-0` dentro de su columna.
- **Tabla**: Ocupa toda la altura disponible (`flex-1 min-h-0 overflow-auto`), eliminado `max-height:420px`.
- **Campo Estado** — solo 3 valores en datos actuales: `Asignados` / `Apto con subsidio vencido` (→CRÍTICO) / `Perdida de ejecutoriedad de asignación de SFV` (→CRÍTICO).

### Tab 1 CIUDAD MÁS CRÍTICA — % añadido
- Nuevo elemento `kpiIntCiudadPct` bajo la ciudad/valor: muestra `"65.5% del pendiente total"`.
- `pctCiu` ya estaba calculado para la barra; ahora también se muestra como texto.

### Tab 3 correcciones de porcentajes
| KPI | Antes | Después |
|---|---|---|
| NOVEDAD MÁS FRECUENTE | `93 casos` (conteo de filas) | `17 bens (46%)` — beneficiarios únicos, % sobre total con novedad |
| $ TOTAL BLOQUEADO | `$142M en novedad` | `$142M` + `0.2%` del pendiente total |
| ARRENDADOR MAYOR RIESGO | `1 con novedad` | `1 de 1 (100%)` — novedad/total del arrendador |
- `novFrecMap` cambió de `count++` a `Set.add(docKey)` para contar beneficiarios únicos.
- `arrRiesgoMap` ahora tiene campo `total` (Set de todos los bens) además de `bens` (solo con novedad).

### Tab 2 — subtítulos sin % duplicado
- Revertida la adición `· X%` en subtítulos de KPIs 1, 2 y 4. El % solo aparece en el círculo.

### Estándar de KPI resultante
- **Número absoluto**: valor principal (grande, coloreado)
- **Subtítulo gris**: `"de TOTAL · X%"` — contexto inmediato sin mirar el círculo
- **Círculo/anillo**: gauge visual del porcentaje
- Tab 3 KPI "BENEFICIARIOS CON NOVEDAD" mantiene su patrón inverso (`XX%` grande + `N de M` pequeño) porque ahí el % de riesgo es el dato primario.

## V11 — Tab 3 dot izquierda + Tab 4 tooltips ptip (14 oct 2026)
**Backup:** `frontend_backup_20261014_tab4_tooltips.html`

### Tab 3 BENEFICIARIOS CON NOVEDAD — indicador al lado izquierdo
- El cuadrado rojo `w-1.5 h-1.5 bg-[#ff0033]` movido del lado derecho al lado izquierdo del panel.
- El layout pasó de `justify-between` a `flex gap-1.5` con el dot como primer hijo, coherente con la lectura izquierda→derecha y el patrón "invertido" (% es el dato primario).

### Tab 4 KPIs — tooltips ⓘ añadidos
Todos los 4 encabezados de KPI de semáforo tienen ahora botón ⓘ con `.ptip`:
| KPI | Texto tooltip |
|---|---|
| 🚨 CRÍTICO | Estado subsidio vencido o pérdida de ejecutoriedad. Gestión inmediata. |
| 🔴 ROJO | +90 días sin pago o +365 días en proceso sin legalizar. Riesgo alto. |
| 🟡 AMARILLO | 60-90 días sin pago o 180-365 días en proceso. Seguimiento activo. |
| 🟢 VERDE | Pagos al día, proceso dentro de plazos normales. |
- El sistema `ptip` se inicializa al cargar la página (IIFE); los paneles de Tab 4 son HTML estático, por lo que los tooltips quedan registrados correctamente.
