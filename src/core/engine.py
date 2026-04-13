import asyncio
import logging
import signal
from src.core.bus import EventBus

logger = logging.getLogger(__name__)

class TradingEngine:
    """
    Coordinador central del sistema. Maneja el ciclo de vida del EventBus 
    y la terminación limpia del proceso.
    """
    def __init__(self):
        self.bus = EventBus()
        self._stop_event = asyncio.Event()

    async def run(self):
        """Bucle principal de ejecución."""
        logger.info("Iniciando Trading Engine...")
        
        # Tarea del bus de eventos
        bus_task = asyncio.create_task(self.bus.start())

        # Configurar señales de terminación (SIGINT, SIGTERM)
        loop = asyncio.get_running_loop()
        for sig in (signal.SIGINT, signal.SIGTERM):
            try:
                loop.add_signal_handler(sig, self._handle_exit)
            except NotImplementedError:
                # Esto sucede en Windows, usamos una alternativa o simplemente 
                # confiamos en el manejo de excepciones de asyncio.run
                pass

        try:
            # Mantener vivo el loop hasta que se reciba señal de stop
            await self._stop_event.wait()
        except asyncio.CancelledError:
            pass
        finally:
            logger.info("Apagando componentes...")
            self.bus.stop()
            await bus_task
            logger.info("Engine detenido.")

    def _handle_exit(self):
        """Callback para señales de terminación."""
        logger.info("Señal de salida recibida.")
        self._stop_event.set()

    def stop(self):
        """Método programático para detener el engine."""
        self._stop_event.set()
