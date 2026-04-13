# ICT Trading System - Institutional Grade

Sistema de trading algorítmico institucional basado en los conceptos de ICT (Inner Circle Trader), desarrollado con una arquitectura orientada a eventos (EDA) para máxima escalabilidad y rendimiento.

## 🏗️ Arquitectura
El sistema sigue los principios de **Clean Architecture**, separando estrictamente la lógica del dominio (trading/detectores) de la infraestructura (conectores/APIs).

- **Asincronía**: Basado en `asyncio` para manejo eficiente de eventos.
- **Rendimiento**: Procesamiento vectorizado con `pandas` para el análisis de mercado.
- **Seguridad**: Circuit Breakers integrados para la gestión de riesgo.

## 📂 Estructura del Proyecto
```text
trading/
├── docs/               # Documentación detallada
├── src/
│   ├── core/           # Bus de eventos y motor central
│   ├── domain/         # Detectores ICT y Lógica de Riesgo
│   ├── infrastructure/ # Adaptadores de datos y brokers
│   └── main.py         # Punto de entrada
├── tests/              # Pruebas de unidad e integración
└── smoke_test.py       # Script de verificación rápida
```

## 🚀 Inicio Rápido
1. Asegúrate de tener Python 3.10+.
2. Instala las dependencias (próximamente): `pip install -r requirements.txt`.
3. Ejecuta el test de humo para verificar el bus: `python smoke_test.py`.

Consulte [docs/architecture.md](docs/architecture.md) para más detalles técnicos.
