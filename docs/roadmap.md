# Roadmap de Implementaciones Futuras

El sistema actual establece las bases del motor de eventos. A continuación se detallan los módulos y características planificadas para las siguientes fases:

## 🚀 Próximas Fases (Inmediatas)

### Fase 2: Ingesta de Datos (Infraestructura)
- [ ] **CSV Historical Loader**: Motor de lectura secuencial para backtesting.
- [ ] **OANDA Stream Client**: Integración asíncrona mediante WebSockets para recepción de ticks en tiempo real.

### Fase 3: Detectores ICT (Dominio)
- [ ] **FVG Detector**: Identificación de Fair Value Gaps alcistas y bajistas en ventanas de 3 velas.
- [ ] **Order Block Detector**: Detección de zonas de oferta y demanda institucional.
- [ ] **Liquidity Sweep**: Identificación de toma de liquidez por encima/debajo de altos y bajos anteriores.

## 🛠️ Mejoras Técnicas y de UI

### Dashboard de Monitoreo
- Desarrollo de una interfaz con **Streamlit** para visualizar:
    - Estado de las órdenes.
    - Equity Curve en tiempo real.
    - Alertas de detección de patrones en vivo.

### Optimización y Machine Learning
- **Refinement de Confluencias**: Uso de algoritmos de optimización para ajustar los pesos del "Cerebro".
- **Análisis de Régimen**: Detector de mercado en tendencia vs rango para ajustar la sensibilidad de los patrones ICT.

## 🛡️ Seguridad y Robustez
- **Hardened Circuit Breaker**: Integración con PostgreSQL para persistir el estado del sistema y evitar "resetear" el contador de pérdidas al reiniciar la app.
- **Auditoría Estricta**: Sistema de logs que exporte cada decisión tomada por el Cerebro en formato JSON para análisis forense post-operativa.
