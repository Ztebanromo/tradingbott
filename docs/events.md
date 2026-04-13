# Referencia de Eventos

Todos los eventos heredan de la clase base `Event` y son inmutables.

## Tipos de Eventos

### 📈 MarketEvent
Generado por el cargador de datos o stream en vivo.
- `symbol`: El par de divisas (ej. "EUR_USD").
- `data`: Diccionario con valores OHLCV.
- `timestamp`: Momento de creación.

### 🔔 SignalEvent
Generado por detectores (ej. `FVGDetector`).
- `symbol`: Activo.
- `side`: Dirección del patrón ("LONG" o "SHORT").
- `confidence`: Nivel de confianza (0.0 a 1.0).
- `strategy_id`: Identificador del detector.
- `metadata`: Información adicional del patrón (ej. precios del gap).

### 🛒 OrderEvent
Generado por el "Cerebro" de estrategia.
- `symbol`: Activo.
- `order_type`: Tipo de orden ("MKT", "LMT").
- `quantity`: Tamaño de la posición.
- `side`: "BUY" o "SELL".

### ✅ ExecutionEvent
Confirmación del broker.
- `symbol`: Activo.
- `fill_price`: Precio real de ejecución.
- `quantity`: Cantidad llenada.
- `side`: Dirección.
- `commission`: Comisiones aplicadas.
