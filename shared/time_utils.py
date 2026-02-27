from datetime import datetime, timezone
from zoneinfo import ZoneInfo

TZ_CHILE = ZoneInfo("America/Santiago")

def to_utc_naive(dt: datetime) -> datetime:
    """
    Convierte un datetime recibido (naive=Chile) a UTC naive para guardar en SQLite.
    """
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=TZ_CHILE)  # interpretamos input como Chile
    dt_utc = dt.astimezone(timezone.utc)
    return dt_utc.replace(tzinfo=None)  # guardamos naive UTC

def utc_now_naive() -> datetime:
    """
    UTC naive para comparar con lo guardado en SQLite.
    """
    return datetime.now(timezone.utc).replace(tzinfo=None)

def utc_naive_to_chile(utc_naive: datetime) -> datetime:
    """
    Para UI: lo guardado (UTC naive) -> Chile aware
    """
    return utc_naive.replace(tzinfo=timezone.utc).astimezone(TZ_CHILE)