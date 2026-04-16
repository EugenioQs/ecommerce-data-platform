# Power BI Design Guide — Ecommerce Data Platform

## Paso 0 — Importar el tema

View → Themes → Browse for themes → seleccionar `ecommerce-theme.json`

---

## Paso 1 — Canvas

View → Page view → Actual size

Format → Canvas settings:
- Width: `1440`
- Height: `900`
- Background color: `#0F1117`

---

## Paso 2 — Estructura de páginas

### Página 1 — Executive Overview

```
┌──────────────────────────────────────────────────────────┐
│  KPI: Revenue   KPI: Orders   KPI: Customers   KPI: AOV  │
├──────────────────────────┬───────────────────────────────┤
│  Line: Monthly Revenue   │  Bar: Top 5 Countries         │
│  Trend (2010–2011)       │  (horizontal, por revenue)    │
├──────────────────────────┴───────────────────────────────┤
│  Donut: Repeat vs One-Time Customers                     │
└──────────────────────────────────────────────────────────┘
```

KPIs:
- Total Revenue → `$7.3M`
- Total Orders → DISTINCTCOUNT de invoice_no
- Total Customers → `4,372`
- Avg Order Value → `$374`

---

### Página 2 — Products

- Horizontal bar: Top 10 Productos por Revenue
- Horizontal bar: Top 10 Productos por Units Sold
- Lado a lado, mismo eje Y para comparar directamente

---

### Página 3 — Customers

- Bar: Top 10 Customers por Lifetime Value
- KPI: % de Repeat Customers (70%)
- Table: customer_id | total_orders | lifetime_value con data bars en revenue

---

### Página 4 — Geography

- Filled Map: Revenue por país (UK va a dominar — perfecto visualmente)
- Table debajo: Country | Revenue | Total Orders con conditional formatting

---

## Paso 3 — Reglas visuales

| Nunca más | Siempre |
|---|---|
| Pie chart | Donut (1 métrica) o bar chart |
| Colores default | Solo colores del tema JSON |
| Bordes en cards | Sin bordes |
| Gridlines en ejes | Desactivadas en todos los charts |
| Títulos "Sum of revenue" | Renombrar siempre: "Revenue by Country" |
| Slicer en lista | Slicer en dropdown |
| Todas las fuentes iguales | 28px KPI → 14px título → 11px label |

---

## Paso 4 — Toques profesionales

### Rectangles como zonas de sección
Insert → Shapes → Rectangle
- Fill: `#1E2435`
- Sin borde
- Send to back
- Agrupa tus visuales encima → crea zonas claras sin que floten

### Conditional formatting en tablas
Columna de revenue → Format → Conditional formatting → Data bars
- Color: `#38BDF8`

### Títulos de página custom
Insert → Text box
- Título: Segoe UI 20px Bold `#F1F5F9`
- Subtítulo: Segoe UI 12px `#64748B`
- Eliminar los títulos de página default

### Navigation buttons
Insert → Buttons → Navigator
- Sin relleno
- Texto: `#94A3B8`
- Hover: `#38BDF8`
- Más limpio que las tabs default de Power BI

---

## Paleta de colores

| Uso | Hex |
|---|---|
| Accent / primary | `#38BDF8` |
| Highlight / alert | `#F59E0B` |
| Revenue / positive | `#34D399` |
| Background | `#0F1117` |
| Card surface | `#1E2435` |
| Texto principal | `#F1F5F9` |
| Texto secundario | `#94A3B8` |
