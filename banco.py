# -*- coding: utf-8 -*-
"""
BANCO DE EVALUACIÓN – Educación para el Trabajo (3.° de secundaria)
HT 70 % (14 pts)  |  HE 20 % (4 pts)  |  HD 10 % (2 pts)   → nota sobre 20

Los casos numéricos se generan con una semilla distinta por alumno (DNI + id):
cada estudiante tiene cifras propias y no puede copiar la respuesta de otro.
Python puro: se puede probar sin Streamlit (python banco.py).
"""
import random, re

DIAS = 15
PESO = {"HT": 14.0, "HE": 4.0, "HD": 2.0}
FOTO_AUTO = 0.40          # 40 % del puntaje de un caso con foto = dato de control (automático)
                          # 60 % = revisión del cuaderno por el docente
TOL = 0.05
NOMBRES = ["Minions", "Tayrom", "Altiplano", "Camino Contable", "Titicaca", "Qori", "San Carlos"]
RUBRICA = ("Rúbrica del docente (60 %): datos del alumno en cada hoja (nombres, grado, sección, fecha) · "
           "cuentas correctas · Debe = Haber · glosa · orden y limpieza.")

def s(x):
    return f"S/ {x:,.2f}"

# ───────────────────────── CASOS HT CON FOTO / NUMÉRICOS ─────────────────────────
def g_balance(r):
    caja = r.choice(range(30000, 80001, 5000)); cxc = r.choice(range(10000, 30001, 5000))
    merc = r.choice(range(10000, 50001, 5000)); veh = r.choice([20000, 25000, 30000, 35000, 40000])
    cxp = r.choice(range(5000, 20001, 5000));   deu = r.choice(range(10000, 40001, 5000))
    A = caja + cxc + merc + veh; pat = A - cxp - deu
    cap = round(pat * .7 / 1000) * 1000; res = round(pat * .1 / 1000) * 1000; ra = pat - cap - res
    t = (f"La empresa {r.choice(NOMBRES)} S.A. abre operaciones con: dinero en cuenta corriente {s(caja)}; "
         f"cuentas por cobrar {s(cxc)}; mercadería {s(merc)}; vehículo {s(veh)}; cuentas por pagar a proveedores "
         f"{s(cxp)}; deudas financieras {s(deu)}; capital {s(cap)}; reservas {s(res)}; resultados acumulados {s(ra)}.")
    return dict(texto=t, tarea="Elabora en tu cuaderno el BALANCE INICIAL (Estado de Situación Financiera de apertura), "
                "clasificando Activo, Pasivo y Patrimonio, y verifica que Activo = Pasivo + Patrimonio.",
                control=float(A), etiqueta="Total del ACTIVO (S/)")

def g_compra(r):
    base = r.choice(range(10000, 60001, 5000)); tot = base * 1.18
    t = (f"El {r.randint(2, 9)}/01/2027 se compra mercadería por un valor total de {s(tot)} incluido IGV, "
         f"con factura, y se paga al contado con depósito en cuenta corriente.")
    return dict(texto=t, tarea="Registra en tu cuaderno los asientos: (1) compra 6011 / 40111 / 4212; "
                "(2) ingreso al almacén 20111 / 6111; (3) pago 4212 / 1041. Separa el IGV del valor de compra.",
                control=round(base * .18, 2), etiqueta="IGV de la compra (S/)")

def g_venta(r):
    base = r.choice(range(20000, 80001, 5000)); tot = base * 1.18
    costo = int(base * r.choice([.45, .5, .55, .6]) // 100 * 100)
    t = (f"El {r.randint(10, 20)}/01/2027 se vende mercadería por {s(tot)} incluido IGV; el costo de venta es "
         f"{s(costo)}. Se cobra al contado por transferencia a la cuenta corriente.")
    return dict(texto=t, tarea="Registra: (1) la venta 1212 / 40111 / 70121; (2) el costo de ventas 69121 / 20111; "
                "(3) el cobro 1041 / 1212. Calcula la utilidad bruta.",
                control=round(base - costo, 2), etiqueta="Utilidad bruta de la operación (S/)")

def g_planilla(r):
    suel = r.choice([1230, 1500, 1800, 2000, 2200, 2500]); asig = r.choice([0, 123]); br = suel + asig
    t = (f"Un trabajador afiliado a la ONP y a EsSalud tiene remuneración básica de {s(suel)}"
         f"{' y asignación familiar de S/ 123.00' if asig else ' (sin asignación familiar)'}. "
         f"ONP 13 % a cargo del trabajador; EsSalud 9 % a cargo del empleador. Se paga por la cuenta corriente.")
    return dict(texto=t, tarea="Registra la planilla: gasto 6211 y 6271; tributos 4031 (EsSalud) y 4032 (ONP); "
                "remuneraciones por pagar 4111. Luego el pago 4111 / 1041.",
                control=round(br - br * .13, 2), etiqueta="Neto a pagar al trabajador (S/)")

def g_dep(r):
    costo = r.choice([3600, 4800, 6000, 9000, 12000, 24000]); tasa = r.choice([10, 20, 25])
    t = (f"Un activo cuesta {s(costo)} (sin IGV) y se deprecia por línea recta al {tasa} % anual, sin valor residual, "
         f"desde el mes siguiente a su compra.")
    return dict(texto=t, tarea="Calcula la depreciación mensual y registra el asiento (cuenta 68 / cuenta 39) con su destino "
                "(94 o 95 / 791).", control=round(costo * tasa / 100 / 12, 2), etiqueta="Depreciación mensual (S/)")

def g_prestamo(r):
    saldo, n = r.choice([(20000, 10), (25000, 10), (30000, 10), (36000, 12), (40000, 8)])
    tasa = r.choice([1.2, 1.5, 1.6, 2.0]); cap = saldo / n; inte = saldo * tasa / 100
    t = (f"Un préstamo bancario tiene saldo de {s(saldo)}, {n} cuotas pendientes con capital constante y "
         f"tasa de {tasa} % mensual sobre el saldo. Se paga la primera cuota por cuenta corriente.")
    return dict(texto=t, tarea="Registra el pago de la cuota: 4511 (capital) y 673 (intereses) contra 1041. "
                "Calcula capital, interés y cuota total.", control=round(cap + inte, 2), etiqueta="Cuota total (S/)")

def g_resultados(r):
    v = r.choice(range(80000, 200001, 10000)); c = int(v * r.choice([.55, .6, .65]) // 100 * 100)
    ga = r.choice([4000, 6000, 8000]); gv = r.choice([2000, 3000, 5000]); gf = r.choice([400, 800, 1200])
    ai = v - c - ga - gv - gf; neta = round(ai * (1 - .295), 2)
    t = (f"Ventas netas {s(v)}; costo de ventas {s(c)}; gastos de administración {s(ga)}; gastos de ventas {s(gv)}; "
         f"gastos financieros {s(gf)}. Tasa del impuesto a la renta: 29.5 %.")
    return dict(texto=t, tarea="Elabora el ESTADO DE GANANCIAS Y PÉRDIDAS por función: utilidad bruta, utilidad operativa, "
                "utilidad antes de impuestos, impuesto a la renta y utilidad neta.",
                control=neta, etiqueta="Utilidad neta del ejercicio (S/)")

# ───────────────────────── PREGUNTAS NUMÉRICAS HT ─────────────────────────
def n_pago(r):
    base = r.choice(range(10000, 50001, 5000)); tot = base * 1.18; p1, p2 = r.choice([(.5, .2), (.6, .1), (.7, .1), (.8, .1)])
    return dict(tipo="num", texto=f"Una compra de mercadería es de {s(tot)} (IGV incluido). Se paga el {int(p1*100)} % y luego "
                f"el {int(p2*100)} %. ¿Cuánto queda pendiente en la cuenta 4212?", etiqueta="Saldo pendiente (S/)",
                resp=round(tot * (1 - p1 - p2), 2))

def n_rhe(r):
    h = r.choice(range(1500, 5001, 500))
    return dict(tipo="num", texto=f"Se paga un recibo por honorarios de {s(h)} a un profesional de 4.ª categoría; la empresa "
                f"retiene el 8 % de renta. ¿Cuánto se transfiere al profesional?", etiqueta="Neto transferido (S/)", resp=round(h * .92, 2))

def n_igv(r):
    v = r.choice(range(60000, 150001, 10000)); c = r.choice(range(30000, 59001, 5000))
    return dict(tipo="num", texto=f"En el mes: ventas gravadas (valor de venta) {s(v)}; compras gravadas (valor de compra) {s(c)}. "
                f"¿Cuál es el IGV por pagar (18 %)?", etiqueta="IGV por pagar (S/)", resp=round((v - c) * .18, 2))

def n_dep(r):
    c = r.choice([2400, 3600, 6000, 7200, 9600, 15000]); t = r.choice([10, 20, 25])
    return dict(tipo="num", texto=f"Un bien de {s(c)} se deprecia al {t} % anual por línea recta. ¿Cuál es la depreciación mensual?",
                etiqueta="Depreciación mensual (S/)", resp=round(c * t / 100 / 12, 2))

def n_essalud(r):
    b = r.choice([1353, 1500, 1800, 2200, 2500, 3000])
    return dict(tipo="num", texto=f"Un trabajador gana {s(b)} brutos al mes. ¿Cuánto aporta el EMPLEADOR a EsSalud (9 %)?",
                etiqueta="Aporte a EsSalud (S/)", resp=round(b * .09, 2))

def n_interes(r):
    sd = r.choice([15000, 20000, 25000, 40000]); t = r.choice([1.2, 1.5, 1.6, 2.0])
    return dict(tipo="num", texto=f"Un préstamo tiene saldo de {s(sd)} y tasa de {t} % mensual sobre el saldo. "
                f"¿Cuánto es el interés de la cuota del mes?", etiqueta="Interés del mes (S/)", resp=round(sd * t / 100, 2))

# ───────────────────────── CONSTRUCTORES GENÉRICOS ─────────────────────────

GRUPOS = "ABCD"
def grupo_de(dni):
    """Grupo por defecto según el último dígito del DNI (el docente puede cambiarlo)."""
    return GRUPOS[int(dni[-1]) % 4]

# Variantes B, C, D de las preguntas de alternativa múltiple (la versión base es el grupo A).
VAR = {
"En la compra de mercadería con IGV, al crédito, ¿qué cuentas se cargan (Debe) y cuál se abona (Haber)?": [
 ("En la venta de mercadería al crédito con IGV, ¿qué cuentas se cargan y cuáles se abonan (sin el costo)?", "Debe 1212 Facturas por cobrar; Haber 40111 IGV y 70121 Ventas", ["Debe 70121 y 40111; Haber 1212", "Debe 1212 y 70121; Haber 40111", "Debe 4212; Haber 70121"]),
 ("Al registrar el COSTO DE VENTAS de una mercadería vendida, se carga y se abona:", "Debe 69121 Costo de ventas; Haber 20111 Mercaderías", ["Debe 20111; Haber 69121", "Debe 70121; Haber 20111", "Debe 69121; Haber 70121"]),
 ("Al pagar por transferencia una factura de compra ya registrada, el asiento es:", "Debe 4212 Facturas por pagar; Haber 1041 Cuentas corrientes", ["Debe 1041; Haber 4212", "Debe 6011; Haber 1041", "Debe 40111; Haber 4212"])],
"La cuenta 40111 «IGV – cuenta propia» en una COMPRA se usa para registrar:": [
 ("En una VENTA, la cuenta 40111 «IGV – cuenta propia» registra:", "El IGV cobrado al cliente, que se debe pagar a la SUNAT", ["El costo de la mercadería", "La depreciación del mes", "El capital del dueño"]),
 ("El IGV por pagar del mes se determina así:", "IGV de las ventas (débito) menos IGV de las compras (crédito fiscal)", ["Ventas menos compras, sin IGV", "IGV de las compras más IGV de las ventas", "Solo el IGV de las compras"]),
 ("La tasa del IGV en el Perú, incluido el IPM, es:", "18 %", ["16 %", "19 %", "20 %"])],
"Según la Ley de Bancarización, desde qué monto deben usarse medios de pago (banco) en lugar de efectivo:": [
 ("Una factura de S/ 5,000 se paga. Según la bancarización, debe pagarse:", "Con transferencia, depósito en cuenta u otro medio de pago", ["En efectivo, siempre", "Con vales internos", "Sin documento alguno"]),
 ("¿Cuál NO es un medio de pago bancario?", "Entregar efectivo en mano", ["Transferencia de fondos", "Cheque no negociable", "Tarjeta de débito"]),
 ("En el pago de una compra de S/ 3,000, la cuenta de salida del dinero es:", "1041 Cuentas corrientes operativas", ["101 Caja", "4212 Facturas por pagar", "20111 Mercaderías"])],
"La ecuación contable básica es:": [
 ("Si el activo es S/ 100,000 y el pasivo S/ 40,000, el patrimonio es:", "S/ 60,000", ["S/ 140,000", "S/ 40,000", "S/ 100,000"]),
 ("Capital, reservas y resultados acumulados pertenecen al:", "Patrimonio", ["Activo", "Pasivo", "Gasto"]),
 ("Las cuentas «Vehículo» y «Mercadería» son cuentas de:", "Activo", ["Pasivo", "Patrimonio", "Ingreso"])],
"¿Cuál es la PRIMERA etapa del Design Thinking?": [
 ("En Design Thinking, construir una versión simple para probar la idea es:", "Prototipar", ["Empatizar", "Definir", "Vender"]),
 ("Entrevistar y observar a los usuarios para comprender su problema corresponde a:", "Empatizar", ["Prototipar", "Idear", "Evaluar"]),
 ("La etapa en que se generan muchas ideas de solución es:", "Idear", ["Definir", "Evaluar", "Empatizar"])],
"¿Cuántos bloques tiene el Lean Canvas?": [
 ("En el Lean Canvas, el bloque que responde «¿Cómo gano dinero?» es:", "Fuentes de ingreso", ["Canales", "Problema", "Métricas clave"]),
 ("El bloque «Propuesta de valor» responde:", "¿Qué beneficio único recibe el cliente?", ["¿Cuánto cuesta el local?", "¿Quién es mi competencia?", "¿Cuántos trabajadores tengo?"]),
 ("El Lean Canvas se caracteriza por ser:", "Un modelo de negocio en una sola hoja, rápido de probar y mejorar", ["Un plan de 100 páginas", "Un contrato legal", "Un estado financiero"])],
"Una buena segmentación de mercado agrupa a los clientes según:": [
 ("Un negocio de útiles escolares tiene como segmento más claro a:", "Estudiantes de primaria y secundaria y sus padres", ["Cualquier persona del mundo", "Solo empresas mineras", "Solo turistas extranjeros"]),
 ("El estudio de mercado sirve principalmente para:", "Conocer la demanda, la competencia y a los clientes antes de invertir", ["Pagar impuestos", "Registrar asientos contables", "Elegir el logotipo"]),
 ("El segmento de mercado se define con variables como:", "Edad, ubicación, ingresos y hábitos de consumo", ["El color del local", "El horario del emprendedor", "El número de RUC"])],
"Tu emprendimiento no vendió lo esperado. Una mentalidad emprendedora de crecimiento haría:": [
 ("La persona con mentalidad emprendedora ve un obstáculo como:", "Una oportunidad de aprender y mejorar", ["Una señal para abandonar", "Un castigo", "Algo sin solución"]),
 ("Una característica del emprendedor es:", "Iniciativa, creatividad y perseverancia", ["Evitar todo riesgo", "Esperar que otros decidan", "Copiar sin pensar"]),
 ("Ante la crítica de un cliente sobre tu producto, lo mejor es:", "Escuchar, analizar y mejorar el producto", ["Ignorarla", "Discutir con el cliente", "Cerrar el negocio"])],
"Para saber qué piensan los posibles clientes antes de invertir, la técnica más útil es:": [
 ("¿Cuál es una técnica de estudio de mercado?", "Encuesta a posibles clientes", ["Sorteo de premios", "Contar el dinero de caja", "Depreciar un activo"]),
 ("Una versión mínima del producto para probar con clientes reales se llama:", "Prototipo (MVP)", ["Balance inicial", "Factura", "Planilla"]),
 ("Observar los precios, productos y atención de la competencia es parte del:", "Análisis de la competencia", ["Cierre de caja", "Asiento de diario", "Depreciación"])],
"Para convertir un documento de Word en PDF:": [
 ("Un PDF se usa principalmente porque:", "Mantiene el formato igual en cualquier dispositivo", ["Permite cambiar fórmulas de Excel", "Siempre pesa menos de 1 KB", "Solo se abre en Word"]),
 ("Para guardar una hoja de Excel como PDF:", "Archivo → Exportar o Guardar como → PDF", ["Archivo → Cerrar sin guardar", "Insertar → Imagen", "Revisar → Ortografía"]),
 ("Desde el celular, una forma de convertir fotos a PDF es:", "Usar «Escanear documento» o una app de escáner", ["Cambiar la extensión a .doc", "Enviarlas por llamada", "Apagar el celular"])],
"Para convertir la foto de un texto en texto EDITABLE se usa:": [
 ("OCR significa:", "Reconocimiento óptico de caracteres", ["Organización de cuentas reales", "Orden de compra rápida", "Oficina de contabilidad regional"]),
 ("Después de aplicar OCR a la foto de un cuaderno, debes:", "Revisar y corregir el texto, porque puede tener errores", ["Enviarlo sin leer", "Borrar la foto antes", "Cambiar solo la tipografía"]),
 ("Una forma de pasar el texto de una imagen a Word es:", "Abrirla con Google Documentos o usar «Copiar texto de la imagen»", ["Renombrarla como .docx", "Imprimirla en blanco", "Comprimirla en .zip"])],
"Vas a enviar por correo 5 fotos pesadas de tu cuaderno. Lo más adecuado es:": [
 ("Comprimir una carpeta (.zip) sirve para:", "Reducir el peso y juntar varios archivos en uno", ["Aumentar la calidad de las fotos", "Borrar archivos", "Cambiar el idioma"]),
 ("Un correo formal debe llevar:", "Asunto claro, saludo, mensaje breve y despedida con tu nombre", ["Solo emojis", "Todo en mayúsculas", "Ningún saludo"]),
 ("Si un archivo es muy pesado para adjuntarlo al correo, lo mejor es:", "Comprimirlo o compartirlo con un enlace de Drive", ["Enviarlo en partes sin avisar", "Borrar la mitad", "Cambiarle el nombre"])],
"Al usar una IA (como Claude) para estudiar contabilidad, lo correcto es:": [
 ("Si una IA te da un asiento contable, debes:", "Comprobarlo con tu cuaderno y verificar que Debe = Haber", ["Copiarlo sin revisar", "Asumir que es correcto", "Darle tu DNI para mejorar la respuesta"]),
 ("Un buen uso de la IA para estudiar es:", "Pedirle que te explique un error y luego resolver tú un caso parecido", ["Pedirle que haga todo el examen", "Entregar su trabajo como propio", "Usarla sin leer"]),
 ("Un buen mensaje (prompt) para una IA es:", "Claro, con el contexto y lo que necesitas", ["Una sola palabra", "Con datos personales y claves", "Sin explicar el tema"])],
}

def mc(r, texto, correcta, malas):
    g = getattr(r, "grupo", "A")
    if g != "A" and texto in VAR:
        texto, correcta, malas = VAR[texto][GRUPOS.index(g) - 1]
    ops = [correcta] + malas; r.shuffle(ops)
    return dict(tipo="mc", texto=texto, opciones=ops, resp=correcta)

def match(r, texto, pares, n=None):
    ps = r.sample(pares, n) if n else list(pares)
    der = [p[1] for p in ps]; r.shuffle(der)
    return dict(tipo="match", texto=texto, izq=[p[0] for p in ps], opciones=der, resp={p[0]: p[1] for p in ps})

def fill(r, texto, frases, banco):
    b = list(banco); r.shuffle(b)
    return dict(tipo="fill", texto=texto, frases=[f[0] for f in frases], opciones=b, resp=[f[1] for f in frases])

def formula(texto, aceptadas):
    return dict(tipo="formula", texto=texto, resp=[a.lower().replace(" ", "").replace("$", "") for a in aceptadas])

# ───────────────────────── HT OBJETIVAS ─────────────────────────
HT_CUENTAS = [("101", "Caja"), ("1041", "Cuentas corrientes operativas"), ("1212", "Facturas por cobrar (emitidas en cartera)"),
              ("20111", "Mercaderías – costo"), ("40111", "IGV – cuenta propia"), ("4212", "Facturas por pagar (emitidas)"),
              ("6011", "Compras de mercaderías"), ("69121", "Costo de ventas – mercaderías"), ("70121", "Ventas de mercaderías – terceros")]
HT_DOCS = [("Nota de ingreso a almacén", "Sustenta la entrada de mercadería al almacén"),
           ("Nota de salida de almacén", "Sustenta la salida de mercadería y su costo"),
           ("Guía de remisión", "Sustenta el traslado de los bienes"),
           ("Voucher bancario", "Constancia de una operación en el banco"),
           ("Recibo por honorarios", "Sustenta un servicio de 4.ª categoría"),
           ("Planilla de remuneraciones", "Resume ingresos, descuentos y neto de los trabajadores"),
           ("Comprobante de egreso", "Sustenta la salida de dinero")]

def q_ht1(r): return mc(r, "En la compra de mercadería con IGV, al crédito, ¿qué cuentas se cargan (Debe) y cuál se abona (Haber)?",
                        "Debe 6011 Mercaderías y 40111 IGV; Haber 4212 Facturas por pagar",
                        ["Debe 4212 y 40111; Haber 6011", "Debe 70121 y 40111; Haber 1212", "Debe 6011; Haber 40111 y 4212"])
def q_ht2(r): return mc(r, "La cuenta 40111 «IGV – cuenta propia» en una COMPRA se usa para registrar:",
                        "El crédito fiscal que se podrá descontar del IGV de las ventas",
                        ["El impuesto a la renta del año", "El ingreso por ventas", "El gasto por depreciación"])
def q_ht3(r): return mc(r, "Según la Ley de Bancarización, desde qué monto deben usarse medios de pago (banco) en lugar de efectivo:",
                        "S/ 2,000 o US$ 500", ["S/ 500 o US$ 100", "S/ 10,000", "S/ 50,000"])
def q_ht4(r): return mc(r, "La ecuación contable básica es:", "Activo = Pasivo + Patrimonio",
                        ["Activo = Pasivo − Patrimonio", "Pasivo = Activo + Patrimonio", "Patrimonio = Activo + Pasivo"])
def q_ht5(r): return match(r, "Relaciona cada cuenta con su nombre.", HT_CUENTAS, 6)
def q_ht6(r): return match(r, "Relaciona cada documento fuente con su función.", HT_DOCS, 5)
def q_ht7(r): return fill(r, "Completa con la palabra correcta.",
                          [("Las cuentas de activo aumentan por el ___.", "Debe"), ("Las cuentas de pasivo aumentan por el ___.", "Haber"),
                           ("Las cuentas de ingresos aumentan por el ___.", "Haber"), ("Las cuentas de gastos se cargan por el ___.", "Debe"),
                           ("En cada asiento, el total del Debe es ___ al total del Haber.", "igual")],
                          ["Debe", "Haber", "igual", "mayor"])
def q_ht8(r): return fill(r, "Completa con el estado financiero que corresponde.",
                          [("El ___ muestra la utilidad o pérdida del periodo.", "Estado de Ganancias y Pérdidas"),
                           ("El ___ muestra activo, pasivo y patrimonio a una fecha.", "Estado de Situación Financiera"),
                           ("El ___ explica cómo aumentó o disminuyó el efectivo.", "Estado de Flujo de Efectivo"),
                           ("El ___ muestra las variaciones de capital, reservas y resultados acumulados.", "Estado de Cambios en el Patrimonio Neto")],
                          ["Estado de Ganancias y Pérdidas", "Estado de Situación Financiera", "Estado de Flujo de Efectivo", "Estado de Cambios en el Patrimonio Neto"])

# ───────────────────────── HE ─────────────────────────
DT = [("Empatizar", "Conocer y comprender al usuario y su problema"), ("Definir", "Formular con claridad el problema a resolver"),
      ("Idear", "Generar muchas ideas de solución"), ("Prototipar", "Construir una versión simple para probar la idea"),
      ("Evaluar", "Probar con usuarios y mejorar")]
LEAN = [("Problema", "¿Qué dolor o necesidad tiene el cliente?"), ("Segmento de clientes", "¿Quiénes son mis clientes?"),
        ("Propuesta de valor", "¿Qué beneficio único ofrezco?"), ("Solución", "¿Qué características resuelven el problema?"),
        ("Canales", "¿Cómo llego a mis clientes?"), ("Fuentes de ingreso", "¿Cómo gano dinero?"),
        ("Estructura de costos", "¿Cuáles son mis gastos principales?"), ("Métricas clave", "¿Cómo mido si voy bien?"),
        ("Ventaja competitiva", "¿Qué no pueden copiar fácilmente?")]
def e1(r): return mc(r, "¿Cuál es la PRIMERA etapa del Design Thinking?", "Empatizar", ["Prototipar", "Evaluar", "Vender"])
def e2(r): return match(r, "Relaciona cada etapa del Design Thinking con su descripción.", DT, 4)
def e3(r): return mc(r, "¿Cuántos bloques tiene el Lean Canvas?", "9", ["5", "7", "12"])
def e4(r): return match(r, "Relaciona cada bloque del Lean Canvas con su pregunta.", LEAN, 5)
def e5(r): return fill(r, "Completa con el término de emprendimiento.",
                       [("El ___ es el grupo de personas al que se dirige mi producto.", "segmento de mercado"),
                        ("El estudio de mercado busca conocer la ___ y a la competencia.", "demanda"),
                        ("La ___ explica el beneficio único que recibe el cliente.", "propuesta de valor"),
                        ("El ___ es una versión simple del producto para probar la idea.", "prototipo")],
                       ["segmento de mercado", "demanda", "propuesta de valor", "prototipo", "oferta"])
def e6(r): return mc(r, "Una buena segmentación de mercado agrupa a los clientes según:",
                     "Características comunes: edad, ubicación, necesidades o hábitos de consumo",
                     ["El precio más bajo del mercado", "El color favorito del emprendedor", "El número de trabajadores del negocio"])
def e7(r): return mc(r, "Tu emprendimiento no vendió lo esperado. Una mentalidad emprendedora de crecimiento haría:",
                     "Analizar qué falló, aprender del error y volver a probar con mejoras",
                     ["Abandonar de inmediato", "Culpar a los clientes", "Copiar el producto de otro sin analizar"])
def e8(r): return mc(r, "Para saber qué piensan los posibles clientes antes de invertir, la técnica más útil es:",
                     "Encuestas y entrevistas (estudio de mercado)", ["Adivinar según la intuición", "Bajar el precio sin probar", "Imprimir más volantes"])

# ───────────────────────── HD ─────────────────────────
PROG = [("Word", "Redactar cartas, informes y documentos"), ("Excel", "Hojas de cálculo, fórmulas y tablas"),
        ("PowerPoint", "Presentaciones con diapositivas"), ("Gmail / Outlook", "Enviar y recibir correo electrónico"),
        ("Google Forms", "Crear formularios y encuestas en línea")]
def d1(r): return formula("En Excel, la celda A1 tiene un precio que YA INCLUYE IGV. Escribe la fórmula que obtiene la BASE (sin IGV).",
                          ["=A1/1.18", "=A1/(1+0.18)", "=A1/(1+18%)", "=A1/118%"])
def d2(r): return formula("En Excel, A1 tiene el precio SIN IGV. Escribe la fórmula que calcula SOLO el monto del IGV (18 %).",
                          ["=A1*0.18", "=A1*18%", "=0.18*A1", "=A1*.18"])
def d3(r): return formula("En Excel, A1 tiene el precio SIN IGV. Escribe la fórmula del TOTAL con IGV.",
                          ["=A1*1.18", "=A1+A1*0.18", "=A1*(1+0.18)", "=A1+(A1*18%)", "=A1*118%"])
def d4(r): return match(r, "Relaciona cada programa con su uso.", PROG, 4)
def d5(r): return mc(r, "Para convertir un documento de Word en PDF:", "Archivo → Guardar como / Exportar → elegir formato PDF",
                     ["Cambiar el nombre a .jpg", "Imprimirlo y escanearlo con celular apagado", "No se puede hacer"])
def d6(r): return mc(r, "Para convertir la foto de un texto en texto EDITABLE se usa:",
                     "Un OCR (por ejemplo, Google Drive/Documentos o «Copiar texto» del celular)",
                     ["Un programa de música", "Comprimir la foto en .zip", "Cambiar el brillo de la foto"])
def d7(r): return mc(r, "Vas a enviar por correo 5 fotos pesadas de tu cuaderno. Lo más adecuado es:",
                     "Comprimirlas en un .zip, adjuntarlas y poner un asunto claro con tu nombre y grado",
                     ["Enviarlas sin asunto ni mensaje", "Pegarlas una por una en el chat de un amigo", "Borrar las más pesadas"])
def d8(r): return mc(r, "Al usar una IA (como Claude) para estudiar contabilidad, lo correcto es:",
                     "Pedir explicaciones, verificar con mi cuaderno y no entregar su respuesta sin revisarla",
                     ["Copiar y pegar todo sin leer", "Creer que nunca se equivoca", "Darle mis datos personales y claves"])

# ───────────────────────── PLAN: (id, área, día, generador, puntos, tipo-foto?) ─────────────────────────
def _foto(gen): return gen
PLAN = [
    ("HT-O1", "HT", 1, q_ht1, .5), ("HT-O2", "HT", 1, q_ht2, .5), ("HE-1", "HE", 1, e1, .5),
    ("HT-F1", "HT", 2, g_balance, 1.0), ("HD-1", "HD", 2, d1, .25),
    ("HT-O3", "HT", 3, n_pago, .5), ("HT-O5", "HT", 3, q_ht5, .5), ("HE-2", "HE", 3, e2, .5),
    ("HT-F2", "HT", 4, g_compra, 1.0), ("HD-2", "HD", 4, d2, .25),
    ("HT-O4", "HT", 5, n_rhe, .5), ("HT-O8b", "HT", 5, q_ht3, .5), ("HE-3", "HE", 5, e3, .5),
    ("HT-F3", "HT", 6, g_venta, 1.0), ("HD-3", "HD", 6, d3, .25),
    ("HT-O6", "HT", 7, n_igv, .5), ("HT-O9", "HT", 7, q_ht4, .5), ("HE-4", "HE", 7, e4, .5), ("HD-4", "HD", 7, d4, .25),
    ("HT-F4", "HT", 8, g_planilla, 1.0), ("HE-5", "HE", 8, e5, .5),
    ("HT-O10", "HT", 9, n_dep, .5), ("HT-O13", "HT", 9, q_ht6, .5), ("HD-5", "HD", 9, d5, .25),
    ("HT-F5", "HT", 10, g_dep, 1.0), ("HE-6", "HE", 10, e6, .5),
    ("HT-O11", "HT", 11, n_essalud, .5), ("HT-O7", "HT", 11, q_ht7, .5), ("HD-6", "HD", 11, d6, .25),
    ("HT-F6", "HT", 12, g_prestamo, 1.0), ("HE-7", "HE", 12, e7, .5),
    ("HT-O14", "HT", 13, n_interes, .5), ("HD-7", "HD", 13, d7, .25),
    ("HT-F7", "HT", 14, g_resultados, 1.0), ("HE-8", "HE", 14, e8, .5),
    ("HT-O12", "HT", 15, q_ht8, .5), ("HD-8", "HD", 15, d8, .25),
]
ITEMS = [dict(id=i, area=a, dia=d, gen=g, pts=p, foto=i.startswith("HT-F")) for i, a, d, g, p in PLAN]

def construir(item, dni, grupo="A"):
    """Genera el caso del alumno (reproducible: misma semilla = mismo caso)."""
    r = random.Random(f"{dni}|{grupo}|{item['id']}"); r.grupo = grupo
    d = item["gen"](r)
    if item["foto"]:
        d["tipo"] = "foto"
    return d

# ───────────────────────── CALIFICACIÓN ─────────────────────────
def fraccion(caso, resp):
    t = caso["tipo"]
    if t in ("mc",): return 1.0 if resp == caso["resp"] else 0.0
    if t == "num":   return 1.0 if resp is not None and abs(float(resp) - caso["resp"]) <= TOL else 0.0
    if t == "foto":  return 1.0 if resp is not None and abs(float(resp) - caso["control"]) <= TOL else 0.0
    if t == "match": return sum(resp.get(k) == v for k, v in caso["resp"].items()) / len(caso["resp"])
    if t == "fill":  return sum(a == b for a, b in zip(resp, caso["resp"])) / len(caso["resp"])
    if t == "formula":
        x = str(resp).lower().replace(" ", "").replace("$", "")
        return 1.0 if x in caso["resp"] else 0.0
    return 0.0

def puntaje_item(item, caso, ans):
    if not ans: return 0.0
    if item["foto"]:
        rev = ans.get("rev")
        return item["pts"] * (FOTO_AUTO * fraccion(caso, ans["resp"]) + (1 - FOTO_AUTO) * (rev or 0.0))
    return item["pts"] * fraccion(caso, ans["resp"])

def totales(dni, respuestas, grupo="A"):
    t = {"HT": 0.0, "HE": 0.0, "HD": 0.0}
    for it in ITEMS:
        a = respuestas.get(it["id"])
        if a: t[it["area"]] += puntaje_item(it, construir(it, dni, grupo), a)
    t["TOTAL"] = round(sum(t.values()), 2)
    return t

if __name__ == "__main__":      # autoprueba
    assert abs(sum(i["pts"] for i in ITEMS if i["area"] == "HT") - 14) < 1e-9
    assert abs(sum(i["pts"] for i in ITEMS if i["area"] == "HE") - 4) < 1e-9
    assert abs(sum(i["pts"] for i in ITEMS if i["area"] == "HD") - 2) < 1e-9
    fotoHT = sum(i["pts"] for i in ITEMS if i["foto"]); print("HT con foto:", fotoHT, "de 14 =", fotoHT / 14)
    resp = {}
    for it in ITEMS:                                   # alumno perfecto
        c = construir(it, "12345678")
        if it["foto"]:   resp[it["id"]] = {"resp": c["control"], "rev": 1.0}
        elif c["tipo"] == "formula": resp[it["id"]] = {"resp": c["resp"][0]}
        else:            resp[it["id"]] = {"resp": c["resp"]}
    print(totales("12345678", resp))
    for g in GRUPOS:
        resp = {}
        for it in ITEMS:
            c = construir(it, "12345678", g)
            resp[it["id"]] = {"resp": c["control"], "rev": 1.0} if it["foto"] else {"resp": c["resp"][0] if c["tipo"] == "formula" else c["resp"]}
        print("Grupo", g, totales("12345678", resp, g)["TOTAL"], "|", construir(ITEMS[0], "12345678", g)["texto"][:70])
