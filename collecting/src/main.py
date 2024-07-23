from typing import List, Dict, Union, Any
from pydantic import BaseModel, ValidationError
from abc import ABC, abstractmethod
import requests
import json
from requests.models import Response

class VLilleStationRecord(BaseModel):
    id: str
    nom: str
    adresse: str
    commune: str
    etat: str
    type: str
    nb_places_dispo: int
    nb_velos_dispo: int
    etat_connexion: str
    x: float
    y: float
    date_modification: str

JsonValue = Union[Dict[str, Any], List[Any], str, int, float, bool, None]
JsonKey = str

class JsonPair(BaseModel):
    key: JsonKey
    value: JsonValue

class Json(BaseModel):
    json_value: Dict[JsonKey, JsonValue]

class VLilleStationDataProvider(ABC):
    @abstractmethod
    def fetch_station_datas(self) -> List[VLilleStationRecord]:
        pass

class FetchAgent(ABC):
    @abstractmethod
    def fetch(self) -> Json:
        pass

class WebRetriever(ABC):
    @abstractmethod
    def retrieve(self) -> Response:
        pass

class RequestsWebRetriever(WebRetriever):
    def __init__(self, url: str) -> None:
        self.url = url
        super().__init__()
    
    def retrieve(self) -> Response:
        response = Response()
        try:
            response = requests.get(self.url)
            response.raise_for_status()

            return response
        except requests.exceptions.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except requests.exceptions.Timeout as timeout_err:
            print(f'Timeout error occurred: {timeout_err}')
        except requests.exceptions.RequestException as req_err:
            print(f'Request error occurred: {req_err}')
        finally:
            return response

class WebAPIFetchAgent(FetchAgent):
    def __init__(self, retriever: WebRetriever):
        self.retriever: WebRetriever = retriever

    def fetch(self) -> Json:
        try:
            response = self.retriever.retrieve()
            return Json(json_value=response.json())
        
        except ValidationError as e:
            print(f"Validation error for json {json}: {e}")
            return Json(json_value={})
        except json.JSONDecodeError as e:
            print(f"JSON decoding error: {e}")
            return Json(json_value={})

class NoRecordsKeyInJsonError(Exception):
    def __init__(self) -> None:
        self.message = "No Records Key Found in Json"
        super().__init__(self.message)

class IleviaVLilleStationDataProvider(VLilleStationDataProvider):
    def __init__(self, fetch_agent: FetchAgent) -> None:
        self.fetch_agent = fetch_agent
    
    def fetch_station_datas(self) -> List[VLilleStationRecord]:
        try:
            json: Json = self.fetch_agent.fetch()

            return extract_stations_records(json.json_value["records"])
        except KeyError:
            raise NoRecordsKeyInJsonError()

def extract_stations_records(records: List[Dict[JsonKey, JsonValue]]) -> List[VLilleStationRecord]:
    stations_records: List[VLilleStationRecord] = []    
    
    for record in records:
        try:
            stations_records.append(VLilleStationRecord(**record))
        except ValidationError as e:
            print(f"Validation error for record {record}: {e}")

    return stations_records


if __name__ == "__main__":
    
    retriever = RequestsWebRetriever("https://data.lillemetropole.fr/data/ogcapi/collections/vlille_temps_reel/items?f=json&limit=-1")
    fetch_agent = WebAPIFetchAgent(retriever)
    service = IleviaVLilleStationDataProvider(fetch_agent)
    
    vlille_records = service.fetch_station_datas()

    print(vlille_records)
