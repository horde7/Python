from dataclasses import dataclass

@dataclass
class Ticker:
    symbol: str
    name: str
    currency: str
    exchange: str
    dta: int

