import pandas as pd
import asyncio
import logging
from typing import Optional
from src.core.bus import EventBus
from src.core.events import MarketEvent

logger = logging.getLogger(__name__)

class CSVMarketDataLoader:
    """
    Cargador de datos históricos desde archivos CSV. 
    Empaqueta cada fila en un MarketEvent y lo publica en el bus.
    """
    def __init__(self, bus: EventBus, symbol: str, file_path: str):
        self.bus = bus
        self.symbol = symbol
        self.file_path = file_path
        self._running = False

    async def load_and_stream(self, delay: float = 0.0):
        """
        Lee el CSV y empieza a inyectar eventos al bus.
        delay: Tiempo de espera entre velas en segundos (0 para máxima velocidad).
        """
        try:
            # Cargamos el CSV (podríamos usar chunks si fuera masivo)
            logger.info(f"Cargando datos desde {self.file_path} para {self.symbol}...")
            df = pd.read_csv(self.file_path)
            
            # Asegurar que el timestamp sea legible si existe
            if 'timestamp' in df.columns:
                df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            self._running = True
            for index, row in df.iterrows():
                if not self._running:
                    break
                
                # Crear diccionario de datos de la vela
                candle_data = row.to_dict()
                
                # Crear MarketEvent
                event = MarketEvent(
                    symbol=self.symbol,
                    data=candle_data
                )
                
                # Publicar al bus
                await self.bus.publish(event)
                
                if delay > 0:
                    await asyncio.sleep(delay)
            
            logger.info(f"Streaming de {self.file_path} completado.")
            
        except FileNotFoundError:
            logger.error(f"Archivo no encontrado: {self.file_path}")
        except Exception as e:
            logger.error(f"Error en CSVMarketDataLoader: {e}")

    def stop(self):
        """Detiene el streaming."""
        self._running = False
