"""
Genera data_github.json con datos anonimizados y actualiza index.html
para publicación en GitHub Pages.
"""
import json, random, string, os
from datetime import date, timedelta

random.seed(42)

# ── Datos de referencia ───────────────────────────────────────────────────────
CIUDADES = [
    "BOGOTA", "MEDELLIN", "CALI", "BARRANQUILLA", "BUCARAMANGA",
    "CARTAGENA", "MANIZALES", "ARMENIA", "PEREIRA", "IBAGUE",
    "VILLAVICENCIO", "CUCUTA", "SANTA MARTA", "MONTERIA", "PASTO",
    "NEIVA", "VALLEDUPAR", "SINCELEJO", "POPAYAN", "TUNJA"
]
PESOS_CIUDAD = [18,12,10,8,7,6,4,3,3,4,4,5,4,3,3,3,4,3,3,3]

RESOLUCIONES = [
    "RESOLUCION 2021-001", "RESOLUCION 2021-002",
    "RESOLUCION 2022-001", "RESOLUCION 2022-002",
    "RESOLUCION 2023-001", "RESOLUCION 2023-002", "RESOLUCION 2023-003",
    "RESOLUCION 2024-001",
]

TIPOS_NOVEDAD = [
    "NINGUNA", "NINGUNA", "NINGUNA", "NINGUNA",  # mayoría sin novedad
    "CAMBIO DE RESIDENCIA", "CAMBIO DE RESIDENCIA",
    "NO LOCALIZACIÓN", "NO LOCALIZACIÓN",
    "FALLECIMIENTO",
    "DUPLICIDAD",
    "INHIBICIÓN JUDICIAL",
    "TRASLADO",
    "SUBSIDIO VENCIDO",
]

ESTADOS_GENERALES = ["ACTIVO", "ACTIVO", "ACTIVO", "SUSPENDIDO", "EN PROCESO"]
ESTADOS_ACTUALES  = ["ACTIVO PAGANDO", "ACTIVO PAGANDO", "SUSPENDIDO", "BLOQUEADO", "EN PROCESO"]

NOMBRES = ["CARLOS","MARIA","JOSE","ANA","LUIS","DIANA","JORGE","PAOLA",
           "ANDRES","LAURA","JUAN","CLAUDIA","PEDRO","ANGELA","SERGIO",
           "PATRICIA","MANUEL","ADRIANA","MIGUEL","VIVIANA","DAVID","CAROLINA",
           "EDGAR","ALEJANDRA","HENRY","MARCELA","NELSON","NATALIA","OSCAR","YOLANDA"]

APELLIDOS = ["GARCIA","RODRIGUEZ","MARTINEZ","LOPEZ","GONZALEZ","PEREZ",
             "SANCHEZ","RAMIREZ","TORRES","FLORES","VARGAS","CASTRO",
             "MORENO","JIMENEZ","RUIZ","HERRERA","MEDINA","ROMERO",
             "GUTIERREZ","MENDOZA","REYES","SILVA","CHAVEZ","ORTIZ",
             "DIAZ","MORALES","PENA","SUAREZ","ACOSTA","BELTRAN"]

def fake_name():
    n = random.choice(NOMBRES) + " " + random.choice(NOMBRES)
    a = random.choice(APELLIDOS) + " " + random.choice(APELLIDOS)
    return f"{n} {a}"

def fake_doc():
    return str(random.randint(10_000_000, 99_999_999))

def fake_date(start_year=2021, end_year=2024):
    start = date(start_year, 1, 1)
    end   = date(end_year, 12, 31)
    delta = (end - start).days
    return (start + timedelta(days=random.randint(0, delta))).isoformat()

# ── Generar beneficiarios únicos ─────────────────────────────────────────────
N_BENS = 600
bens = []
for i in range(N_BENS):
    ciudad  = random.choices(CIUDADES, weights=PESOS_CIUDAD)[0]
    resol   = random.choice(RESOLUCIONES)
    nov     = random.choice(TIPOS_NOVEDAD)
    val_men = random.choice([350_000, 400_000, 450_000, 500_000, 550_000])
    pagos_n = random.randint(1, 12)
    pend    = val_men * (12 - pagos_n)
    bens.append({
        "doc":      fake_doc(),
        "nombre":   fake_name(),
        "ciudad":   ciudad,
        "resol":    resol,
        "nov":      nov,
        "val_men":  val_men,
        "pagos_n":  pagos_n,
        "pend":     pend,
        "fec_ini":  fake_date(2021, 2023),
        "arr_doc":  fake_doc(),
        "arr_nom":  fake_name(),
        "est_gral": random.choice(ESTADOS_GENERALES),
        "est_act":  random.choice(ESTADOS_ACTUALES),
        "id":       str(i + 1),
    })

# ── Expandir a registros por pago (melt) ─────────────────────────────────────
records = []
for b in bens:
    for p in range(1, b["pagos_n"] + 1):
        nov_tipo = b["nov"]
        records.append({
            "NUMERO DE DOCUMENTO":                       b["doc"],
            "NOMBRE BENEFICIARIO":                       b["nombre"],
            "CIUDAD":                                    b["ciudad"],
            "RESOLUCION":                                b["resol"],
            "ESTADO GENERAL":                            b["est_gral"],
            "LEGALIZADO":                                "Sí" if p >= 2 else "No",
            "PERIODO_PAGO":                              f"PAGO {p}",
            "VALOR_PAGADO":                              b["val_men"],
            "OBSERVACIONES":                             "",
            "PRESENTA NOVEDAD":                          "NINGUNA" if nov_tipo == "NINGUNA" else "SÍ",
            "FECHA DE LA NOVEDAD":                       fake_date(2022, 2024) if nov_tipo != "NINGUNA" else "",
            "TIPO DE NOVEDAD":                           nov_tipo,
            "ESTADO ACTUAL":                             b["est_act"],
            "PENDIENTE POR PAGAR":                       b["pend"],
            "VALOR SUBSIDIO AL CANON ARRIENDO MENSUAL":  b["val_men"],
            "# DOCUMENTO DEL ARRENDADOR":                b["arr_doc"],
            "NOMBRE ARRENDADOR":                         b["arr_nom"],
            "FECHA INICIO":                              b["fec_ini"],
            "ID":                                        b["id"],
            "NUMERO DE DOCUMENTO PPT":                   b["doc"],
        })

print(f"Registros generados: {len(records)}")

out_path = os.path.join(os.path.dirname(__file__), "data_github.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(records, f, ensure_ascii=False)
print(f"Guardado: {out_path}  ({os.path.getsize(out_path)//1024} KB)")

# ── Generar timeline (Tab 4) ──────────────────────────────────────────────────
SEMAFOROS   = ["VERDE","VERDE","VERDE","AMARILLO","AMARILLO","ROJO","CRITICO"]
ETAPAS      = ["CARGADO","CARGADO","LEGALIZADO","ASIGNADO"]
GESTORES    = ["GESTOR A","GESTOR B","GESTOR C","GESTOR D"]
ESTADOS_TL  = ["Activo","En proceso","Suspendido","Apto con subsidio vencido"]

timeline = []
for b in bens:
    sem = random.choice(SEMAFOROS)
    eta = random.choice(ETAPAS)
    d1  = random.randint(10, 120)
    d2  = random.randint(5, 90) if eta in ("LEGALIZADO","CARGADO") else None
    d3  = random.randint(3, 60) if eta == "CARGADO" else None
    d4  = random.randint(0, 180) if sem in ("ROJO","CRITICO") else random.randint(0, 30)
    timeline.append({
        "documento":         b["doc"],
        "nombre":            b["nombre"].split()[0],
        "apellidos":         " ".join(b["nombre"].split()[2:]),
        "ciudad":            b["ciudad"],
        "resolucion":        b["resol"],
        "estado":            random.choice(ESTADOS_TL),
        "legalizado":        "Sí" if eta in ("LEGALIZADO","CARGADO") else "No",
        "fecha_asignacion":  fake_date(2021, 2022),
        "fecha_postulacion": fake_date(2020, 2021),
        "fecha_legalizacion":fake_date(2022, 2023) if eta in ("LEGALIZADO","CARGADO") else None,
        "fecha_cargue":      fake_date(2023, 2024) if eta == "CARGADO" else None,
        "fecha_ultimo_pago": fake_date(2023, 2024),
        "num_pagos":         b["pagos_n"],
        "total_pagado":      b["val_men"] * b["pagos_n"],
        "gestor":            random.choice(GESTORES),
        "gestor_legal":      random.choice(GESTORES),
        "sexo":              random.choice(["M","F"]),
        "nacionalidad":      "COLOMBIANO",
        "mujer_cab_fam":     random.choice(["Sí","No"]),
        "adulto_mayor":      random.choice(["Sí","No"]),
        "discapacitado":     random.choice(["Sí","No"]),
        "victima":           random.choice(["Sí","No"]),
        "d1": d1, "d2": d2, "d3": d3, "d4_sin_pago": d4,
        "d_proceso": d1 + (d2 or 0) + (d3 or 0),
        "etapa":    eta,
        "semaforo": sem,
    })

tl_path = os.path.join(os.path.dirname(__file__), "data_timeline_github.json")
with open(tl_path, "w", encoding="utf-8") as f:
    json.dump(timeline, f, ensure_ascii=False)
print(f"Guardado: {tl_path}  ({os.path.getsize(tl_path)//1024} KB)")

# ── Sincronizar frontend.html → index.html (rutas GitHub Pages) ───────────────
src  = os.path.join(os.path.dirname(__file__), "frontend.html")
dest = os.path.join(os.path.dirname(__file__), "index.html")

with open(src, encoding="utf-8") as f:
    html = f.read()

# Reemplazar rutas absolutas → relativas y API → archivos estáticos
html = html.replace("fetch('/colombia.json')",           "fetch('colombia.json')")
html = html.replace("fetch('/api/data')",                "fetch('data_github.json')")
html = html.replace("fetch('/api/metadata')",            "fetch('data_metadata_github.json')")
html = html.replace("fetch('/api/timeline')",            "fetch('data_timeline_github.json')")

with open(dest, "w", encoding="utf-8") as f:
    f.write(html)
print(f"index.html actualizado: {os.path.getsize(dest)//1024} KB")

# ── Generar metadata estática ─────────────────────────────────────────────────
meta_path = os.path.join(os.path.dirname(__file__), "data_metadata_github.json")
with open(meta_path, "w", encoding="utf-8") as f:
    json.dump({"fileDate": "DEMO — DATOS FICTICIOS", "fileTime": "—"}, f)
print(f"Guardado: {meta_path}")

print("\n✅ Listo. Archivos generados:")
print("  index.html  (versión GitHub Pages)")
print("  data_github.json  (datos anonimizados)")
print("  data_timeline_github.json  (timeline anonimizado)")
print("  data_metadata_github.json  (metadata)")
