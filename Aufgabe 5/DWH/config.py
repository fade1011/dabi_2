from dataclasses import  dataclass

@dataclass(frozen=True)
class DatenbankWetter():
    HOSTNAME = '34.31.212.247'
    DBNAME = 'Wetter'
    USER = 'dabi'
    PASSWORD = 'Gejsaf-kokwur-5hopte'
    PORT = 3306

@dataclass(frozen=True)
class DatenbankUmsatz():
    HOSTNAME = '34.31.212.247'
    DBNAME = 'Umsatzdaten'
    USER = 'dabi'
    PASSWORD = 'Gejsaf-kokwur-5hopte'
    PORT = 3306
    
@dataclass(frozen=True)
class DatenbankUmsatzGewerbe():
    HOSTNAME = '34.31.212.247'
    DBNAME = 'Umsatzdaten_Gewerbe'
    USER = 'dabi'
    PASSWORD = 'Gejsaf-kokwur-5hopte'
    PORT = 3306