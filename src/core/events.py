from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, Dict, Optional
from datetime import datetime

class EventType(Enum):
    MARKET = auto()
    SIGNAL = auto()
    ORDER = auto()
    EXECUTION = auto()

@dataclass(frozen=True, kw_only=True)
class Event:
    """Clase base para todos los eventos del sistema."""
    type: EventType
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass(frozen=True, kw_only=True)
class MarketEvent(Event):
    """Evento que contiene datos de mercado (OHLCV)."""
    symbol: str
    data: Dict[str, Any]  # Habitualmente contendrá Open, High, Low, Close, Volume
    type: EventType = EventType.MARKET

@dataclass(frozen=True, kw_only=True)
class SignalEvent(Event):
    """Evento generado por un detector al encontrar un patrón (ej. FVG)."""
    symbol: str
    side: str  # 'LONG', 'SHORT'
    confidence: float
    strategy_id: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    type: EventType = EventType.SIGNAL

@dataclass(frozen=True, kw_only=True)
class OrderEvent(Event):
    """Evento que representa la intención de ejecutar una operación."""
    symbol: str
    order_type: str  # 'MKT', 'LMT'
    quantity: float
    side: str
    type: EventType = EventType.ORDER

@dataclass(frozen=True, kw_only=True)
class ExecutionEvent(Event):
    """Evento de confirmación tras la ejecución en el broker."""
    symbol: str
    fill_price: float
    quantity: float
    side: str
    commission: float
    type: EventType = EventType.EXECUTION
