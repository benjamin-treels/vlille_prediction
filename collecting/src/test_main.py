from main import (
    VLilleStationRecord, extract_stations_records, IleviaVLilleStationDataProvider,
    FetchAgent, Json, NoRecordsKeyInJsonError, WebAPIFetchAgent, WebRetriever, JsonKey,
    JsonValue
    )
from typing import  List, Dict
import pytest
from requests.models import Response

class TestExtractStationsRecord:

    """
    should return a list of StationRecord from a dict that contains correct data 
    """
    def test_extract_stations_records_happy_flow(self):
        station_mel =  dummy_vlille_station_records()[0]
        station_pont_de_labbaye = dummy_vlille_station_records()[1]

        expected = [station_mel, station_pont_de_labbaye]

        records: List[Dict[JsonKey, JsonValue]] = [
            {
                "@id": "7761385",
                "id": "1",
                "nom": "METROPOLE EUROPEENNE DE LILLE",
                "adresse": "MEL RUE DU BALLON",
                "code_insee": None,
                "commune": "LILLE",
                "etat": "RÉFORMÉ",
                "type": "AVEC TPE",
                "nb_places_dispo": 0,
                "nb_velos_dispo": 0,
                "etat_connexion": "DÉCONNECTÉ",
                "x": 3.075992,
                "y": 50.641926,
                "date_modification": "2022-11-29T10:47:16.181+00:00"
            },
            {
                "@id": "7761424",
                "id": "313",
                "nom": "PONT DE L'ABBAYE",
                "adresse": "6 rue du Pont de l'Abbaye",
                "code_insee": None,
                "commune": "Marquette Lez Lille",
                "etat": "EN SERVICE",
                "type": "AVEC TPE",
                "nb_places_dispo": 9,
                "nb_velos_dispo": 11,
                "etat_connexion": "CONNECTÉ",
                "x": 3.06415,
                "y": 50.666236,
                "date_modification": "2024-07-19T19:59:21.692+00:00"
            }
        ]

        result = extract_stations_records(records)

        assert result == expected

    """
    should return a empty list from a dict that contains incorrect data
    """
    def test_extract_stations_record_with_incorrect_data(self):

        expected = []

        records: List[Dict] = [
            {
                "age": 12,
                "id": 1,
                "firstname": "Tom",
                "lastname": "Jedusor",
            },
            {
                "age": 1500,
                "id": 5,
                "firstname": "Yoda",
                "lastname": "Baby",
            }
        ]

        result = extract_stations_records(records)

        assert result == expected

    """
    should return list of StationRecord from correct data in dict only
    """
    def test_extract_stations_record_with_some_correct_data(self):

        station_mel = dummy_vlille_station_records()[0]
        
        expected = [station_mel]

        records: List[Dict] = [
            {
                "@id": "7761385",
                "id": "1",
                "nom": "METROPOLE EUROPEENNE DE LILLE",
                "adresse": "MEL RUE DU BALLON",
                "code_insee": None,
                "commune": "LILLE",
                "etat": "RÉFORMÉ",
                "type": "AVEC TPE",
                "nb_places_dispo": 0,
                "nb_velos_dispo": 0,
                "etat_connexion": "DÉCONNECTÉ",
                "x": 3.075992,
                "y": 50.641926,
                "date_modification": "2022-11-29T10:47:16.181+00:00"
            },
            {
                "age": 12,
                "id": 1,
                "firstname": "Tom",
                "lastname": "Jedusor",
            },
            {
                "age": 1500,
                "id": 5,
                "firstname": "Yoda",
                "lastname": "Baby",
            }
        ]

        result = extract_stations_records(records)

        assert result == expected

class TestIleviaVLilleStationDataProvider:
    """
    should return VLilleStationRecord from IleviaAPI 
    """
    def test_happy_flow(self):
        expected = dummy_vlille_station_records()
    
        service = IleviaVLilleStationDataProvider(fetch_agent=DummyFetchAgent())
    
        result = service.fetch_station_datas()
    
        assert result == expected

    """
    should return KeyError when no "records" key is present in json
    """
    def test_key_error_when_no_records_key(self):
        service = IleviaVLilleStationDataProvider(fetch_agent=DummyFetchAgent2())
        with pytest.raises(NoRecordsKeyInJsonError) as e:
            service.fetch_station_datas()
        assert str(e.value) == "No Records Key Found in Json"
        

class TestWebAPIFetchAgent:
    """
    Fetch happy flow 
    """
    def test_fetch_happy_flow(self):
        expected = Json(json_value={"status": 200, "records" :[{"toto":"tata"},{"alice":"bob"}] } )
        
        service = WebAPIFetchAgent(DummyWebRetriever())
        
        result = service.fetch()

        assert result.json_value == expected.json_value


class DummyWebRetriever(WebRetriever):
    def __init__(self) -> None:
        super().__init__()
    
    def retrieve(self) -> Response:
        response = Response()
        response._content = b'{"status": 200, "records": [{"toto": "tata"}, {"alice": "bob"}]}'
        return response

class DummyFetchAgent(FetchAgent):
    def __init__(self) -> None:
        pass
    
    def fetch(self) -> Json:
        json = {
            "numberMatched": 289,
            "numberReturned": 289,
            "records": [
                {
                    "@id": "8145177",
                    "id": "1",
                    "nom": "METROPOLE EUROPEENNE DE LILLE",
                    "adresse": "MEL RUE DU BALLON",
                    "code_insee": None,
                    "commune": "LILLE",
                    "etat": "RÉFORMÉ",
                    "type": "AVEC TPE",
                    "nb_places_dispo": 0,
                    "nb_velos_dispo": 0,
                    "etat_connexion": "DÉCONNECTÉ",
                    "x": 3.075992,
                    "y": 50.641926,
                    "date_modification": "2022-11-29T10:47:16.181+00:00"
                },
                {
                    "@id": "7761424",
                    "id": "313",
                    "nom": "PONT DE L'ABBAYE",
                    "adresse": "6 rue du Pont de l'Abbaye",
                    "code_insee": None,
                    "commune": "Marquette Lez Lille",
                    "etat": "EN SERVICE",
                    "type": "AVEC TPE",
                    "nb_places_dispo": 9,
                    "nb_velos_dispo": 11,
                    "etat_connexion": "CONNECTÉ",
                    "x": 3.06415,
                    "y": 50.666236,
                    "date_modification": "2024-07-19T19:59:21.692+00:00"
                }
            ]
        }
        return Json(json_value=json)

class DummyFetchAgent2(FetchAgent):
    def __init__(self) -> None:
        pass
    def fetch(self) -> Json:
        json = {
            "numberMatched": 289,
            "numberReturned": 289,
        }
        return Json(json_value=json) 
    
def dummy_vlille_station_records() -> List[VLilleStationRecord]:
    return [
        VLilleStationRecord(**{
            "id": "1",
            "nom": "METROPOLE EUROPEENNE DE LILLE",
            "adresse": "MEL RUE DU BALLON",
            "commune": "LILLE",
            "etat": "RÉFORMÉ",
            "type": "AVEC TPE",
            "nb_places_dispo": 0,
            "nb_velos_dispo": 0,
            "etat_connexion": "DÉCONNECTÉ",
            "x": 3.075992,
            "y": 50.641926,
            "date_modification": "2022-11-29T10:47:16.181+00:00"
        }),
        VLilleStationRecord(**{
            "id": "313",
            "nom": "PONT DE L'ABBAYE",
            "adresse": "6 rue du Pont de l'Abbaye",
            "commune": "Marquette Lez Lille",
            "etat": "EN SERVICE",
            "type": "AVEC TPE",
            "nb_places_dispo": 9,
            "nb_velos_dispo": 11,
            "etat_connexion": "CONNECTÉ",
            "x": 3.06415,
            "y": 50.666236,
            "date_modification": "2024-07-19T19:59:21.692+00:00"
        })
    ]