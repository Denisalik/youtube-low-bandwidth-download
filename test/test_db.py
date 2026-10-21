import httpx


def test_get_all_endpoint(backend_server):
    response = httpx.get(f"{backend_server}/api/files")
    assert response.status_code == 200
    data = response.json()
    print(data)
    assert isinstance(data, list)
    #if you have data
    assert len(data) > 0
    assert all("id" in item for item in data)
