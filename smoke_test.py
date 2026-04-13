import asyncio
import logging
import sys
import os

# Añadir el path actual para poder importar los módulos
sys.path.append(os.getcwd())

from src.core.events import EventType, MarketEvent, SignalEvent, OrderEvent, ExecutionEvent
from src.core.engine import TradingEngine

# Configuración básica de logs
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("SmokeTest")

async def mock_detector(event: MarketEvent):
    logger.info(f"[Handler] Detector recibió datos: {event.symbol} @ {event.data['close']}")
    # Simulamos detección de señal
    signal = SignalEvent(
        symbol=event.symbol,
        side='LONG',
        confidence=0.85,
        strategy_id="FVG_V1"
    )
    # Publicamos de vuelta al bus (pasado por referencia o accedido globalmente)
    # En un entorno real, el engine o el bus estarían inyectados.
    # Aquí lo haremos manualmente para el test.

async def mock_executor(event: OrderEvent):
    logger.info(f"[Handler] Executor procesando orden: {event.side} {event.quantity} {event.symbol}")

async def main():
    engine = TradingEngine()
    
    # Suscribir handlers mock
    engine.bus.subscribe(EventType.MARKET, mock_detector)
    engine.bus.subscribe(EventType.ORDER, mock_executor)
    
    # Iniciar engine en background
    engine_task = asyncio.create_task(engine.run())
    
    # Pequeña espera para que el bus arranque
    await asyncio.sleep(1)
    
    # 1. Simular Market Event
    logger.info("Enviando MARKET event...")
    mkt_event = MarketEvent(
        symbol="EUR_USD",
        data={"open": 1.0850, "high": 1.0860, "low": 1.0845, "close": 1.0855, "volume": 100}
    )
    await engine.bus.publish(mkt_event)
    
    # 2. Simular Order Event
    logger.info("Enviando ORDER event...")
    order_event = OrderEvent(
        symbol="EUR_USD",
        order_type="MKT",
        quantity=1000,
        side="BUY"
    )
    await engine.bus.publish(order_event)
    
    # Esperar procesamiento
    await asyncio.sleep(2)
    
    # Cerrar engine
    engine.stop()
    await engine_task
    logger.info("Smoke Test finalizado exitosamente.")

if __name__ == "__main__":
    asyncio.run(main())
