import pytest
from fastapi import status

from app.models import Cargo, Rate


@pytest.mark.anyio
async def test_import_rates(client):
    dtime_1 = "2022-12-02"
    dtime_2 = "2023-12-02"
    dtime_3 = "2024-12-02"
    cargo_type_1 = "Vegetables"
    cargo_type_2 = "Furniture"
    cargo_type_3 = "Medicines"
    rate_1 = "1.1"
    rate_2 = "2.2"
    rate_3 = "3.3"
    import_data: dict = {
        dtime_1: {"cargo_type": cargo_type_1, "rate": rate_1},
        dtime_2: {"cargo_type": cargo_type_2, "rate": rate_2},
        dtime_3: {"cargo_type": cargo_type_3, "rate": rate_3},
    }

    assert await Cargo.all().count() == 0
    response = client.post("/api/rates/", json=import_data)
    assert response.status_code == status.HTTP_200_OK
    res_json = response.json()
    assert res_json["info"] == "Обработано тарифов: 3"
    assert await Cargo.all().count() == 3
    assert await Rate.all().count() == 3


@pytest.mark.anyio
async def test_get_rates(client):
    dtime = "2000-01-01"
    cargo_db = await Cargo.create(name="test 1")
    rate_db_1 = await Rate.create(cargo=cargo_db, rate=1.1, date=dtime)
    rate_db_2 = await Rate.create(cargo=cargo_db, rate=1.1, date=dtime)
    rate_db_3 = await Rate.create(cargo=cargo_db, rate=1.1, date=dtime)
    response = client.get("/api/rates/")
    assert response.status_code == status.HTTP_200_OK
    res_json = response.json()
    assert len(res_json) == 3
    for rate_json in res_json:
        assert "cargo_id" in rate_json
        assert "rate" in rate_json
        assert "date" in rate_json
        assert "id" in rate_json


@pytest.mark.anyio
async def test_cargo_detail(client):
    cargo_db = await Cargo.create(name="test 1")
    url: str = f"/api/cargos/{cargo_db.id}"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    res_json = response.json()
    assert res_json["name"] == cargo_db.name
    assert res_json["value"] == cargo_db.value
    assert res_json["id"] == cargo_db.id


@pytest.mark.anyio
async def test_set_cargo_value(client):
    cargo_db = await Cargo.create(name="test 1")
    url: str = f"/api/cargos/{cargo_db.id}"
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    res_json = response.json()
    assert res_json["value"] == 0

    new_value: float = 100.1
    response = client.patch(url, json={"value": new_value})
    assert response.status_code == status.HTTP_200_OK
    res_json = response.json()
    assert (
        res_json["info"] == f"Объявленная стоимость Груза {cargo_db.name} изменена на {new_value}"
    )

    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    res_json = response.json()
    assert res_json["value"] == new_value


@pytest.mark.anyio
def test_set_cargo_value_404(client):
    url: str = "/api/cargos/404"
    response = client.patch(url, json={"value": 404})
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.anyio
async def test_get_cargos(client):
    cargo_db_1 = await Cargo.create(name="test 1")
    cargo_db_2 = await Cargo.create(name="test 2")
    cargo_db_3 = await Cargo.create(name="test 3")
    response = client.get("/api/cargos/")
    assert response.status_code == status.HTTP_200_OK
    res_json = response.json()
    assert len(res_json) == 3
    for cargo_json in res_json:
        assert "value" in cargo_json
        assert "name" in cargo_json
        assert "id" in cargo_json


@pytest.mark.anyio
async def test_calc_cargo_insurance(client):
    dtime = "2000-01-01"
    rate: float = 1.1
    value: float = 2.2
    cargo_db = await Cargo.create(name="test 1", value=value)
    rate_db = await Rate.create(cargo=cargo_db, rate=rate, date=dtime)
    response = client.post(
        "/api/cargo_insurance/", json={"chosen_date": dtime, "cargo_type": cargo_db.name}
    )
    assert response.status_code == status.HTTP_200_OK
    res_json = response.json()
    assert res_json["date"] == str(rate_db.date)
    assert res_json["cargo_type"] == cargo_db.name
    assert res_json["rate"] == rate_db.rate
    assert res_json["value"] == cargo_db.value
    assert res_json["cargo_insurance"] == cargo_db.value * rate_db.rate


@pytest.mark.anyio
def test_calc_cargo_insurance_404_cargo(client):
    response = client.post(
        "/api/cargo_insurance/", json={"chosen_date": "2022-01-01", "cargo_type": "test"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Груз не найден"}


@pytest.mark.anyio
async def test_calc_cargo_insurance_404_rate(client):
    cargo_db = await Cargo.create(name="test 1")
    response = client.post(
        "/api/cargo_insurance/", json={"chosen_date": "2022-01-01", "cargo_type": cargo_db.name}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Тариф не найден"}
