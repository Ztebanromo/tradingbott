import asyncio
import logging
from typing import Dict, List, Callable, Awaitable
from src.core.events import Event, EventType

logger = logging.getLogger(__name__)

class EventBus:
    """
    Bus de eventos asíncrono que permite la suscripción y publicación 
    de eventos en el sistema.
    """
    def __init__(self):
        self.queue: asyncio.Queue = asyncio.Queue()
        self._handlers: Dict[EventType, List[Callable[[Event], Awaitable[None]]]] = {
            t: [] for t in EventType
        }
        self._running = False

    def subscribe(self, event_type: EventType, handler: Callable[[Event], Awaitable[None]]):
        """Registra un manejador para un tipo de evento específico."""
        self._handlers[event_type].append(handler)
        logger.debug(f"Suscrito: {handler.__name__} a {event_type.name}")

    async def publish(self, event: Event):
        """Coloca un evento en la cola para su procesamiento."""
        await self.queue.put(event)
        logger.debug(f"Evento publicado: {event.type.name}")

    async def start(self):
        """Inicia el bucle de despacho de eventos."""
        self._running = True
        logger.info("EventBus iniciado.")
        while self._running:
            event = await self.queue.get()
            try:
                await self._dispatch(event)
            except Exception as e:
                logger.error(f"Error al despachar evento {event.type.name}: {e}")
            finally:
                self.queue.task_done()

    def stop(self):
        """Detiene el bus de eventos."""
        self._running = False
        logger.info("EventBus detenido.")

    async def _dispatch(self, event: Event):
        """Distribuye el evento a todos sus suscriptores registrados."""
        handlers = self._handlers.get(event.type, [])
        if not handlers:
            return

        # Ejecutamos los handlers en paralelo para no bloquear el bus
        tasks = [handler(event) for handler in handlers]
        await asyncio.gather(*tasks)
