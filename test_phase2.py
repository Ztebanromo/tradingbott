import asyncio
import logging
import sys
import os

sys.path.append(os.getcwd())

from src.core.bus import EventType
from src.core.engine import TradingEngine
from src.infrastructure.loaders.csv_loader import CSVMarketDataLoader

# Configuración de logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger("TestPhase2")

class MockICTDetector:
    """Un detector simple que solo imprime los precios que recibe."""
    def __init__(self):
        self.candle_count = 0

    async def on_market_data(self, event):
        self.candle_count += 1
        close = event.data['close']
        timestamp = event.data['timestamp']
        if self.candle_count % 10 == 0:  # Mostrar cada 10 velas para no saturar
            logger.info(f"[Detector] Vela {self.candle_count} recibida: {event.symbol} Close={close:.5f} @ {timestamp}")

async def main():
    engine = TradingEngine()
    detector = MockICTDetector()
    
    # Suscribir el detector al bus
    engine.bus.subscribe(EventType.MARKET, detector.on_market_data)
    
    # Iniciar motor
    engine_task = asyncio.create_task(engine.run())
    
    # Inicializar el cargador de CSV
    loader = CSVMarketDataLoader(
        bus=engine.bus, 
        symbol="EUR_USD", 
        file_path="data/sample_data.csv"
    )
    
    # Ejecutar la carga (sin delay para el test)
    logger.info("Iniciando inyección de datos desde CSV...")
    await loader.load_and_stream(delay=0.01)
    
    # Pequeña espera para asegurar que el bus procesó todo
    await asyncio.sleep(1)
    
    # Cerrar todo
    logger.info(f"Test finalizado. Total velas procesadas: {detector.candle_count}")
    engine.stop()
    await engine_task

if __name__ == "__main__":
    asyncio.run(main())
