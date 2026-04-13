# Arquitectura del Sistema

El sistema utiliza un diseño **Event-Driven (EDA)** para garantizar que cada componente sea reactivo y desacoplado.

## Flujo de Eventos

1. **Ingesta**: Un componente de infraestructura (CSV Loader o Oanda Stream) genera un `MarketEvent`.
2. **Detección**: Los detectores en el dominio escuchan `MarketEvents`, analizan la ventana temporal y emiten `SignalEvents` si encuentran patrones (ej. FVG).
3. **Estrategia (Cerebro)**: Escucha `SignalEvents`, aplica pesos y confluencias. Si se supera un umbral, emite un `OrderEvent`.
4. **Gestión de Riesgo**: Escucha `OrderEvents`. Valida el capital, stop loss y circuit breakers. Si es válido, re-emite o permite el `OrderEvent`.
5. **Ejecución**: El Broker Client escucha el `OrderEvent`, ejecuta la orden y emite un `ExecutionEvent`.

## Componentes Core

### EventBus (`src/core/bus.py`)
Utiliza `asyncio.Queue` para despachar eventos a múltiples suscriptores de forma asíncrona. Los manejadores (handlers) deben ser funciones `async`.

### Trading Engine (`src/core/engine.py`)
Maneja el bucle principal y coordina el apagado del sistema mediante señales `SIGINT/SIGTERM`.

### Modelos de Datos (`src/core/events.py`)
Definidos mediante `dataclasses` inmutables (`frozen=True`) y campos keyword-only (`kw_only=True`) para robustez.
