def test_health_check(client):
    """
    Test that the health endpoint returns 200 OK
    and include 'api':'ok' in the response
    """
    # 1. Arrange: Define your target endpoint
    endpoint = "/health"

    # 2. Act: Call the api uisng the client fixture
    response = client.get(endpoint)

    # 3. Assert: check if the response matches expectations
    assert response.status_code == 200
    # parse the data
    data = response.json()

    # verify the contents of the response
    assert data['api'] == "ok"
    assert "database" in data
    assert "redis" in data

def test_health_check_db_success(client, mocker):
    # This intercepts the get_db_conn fucntion and make it return a fake connection object intead of failing 
    mocker.patch("app.api.routes.get_db_conn")
    mocker.patch("app.api.routes.pool")

    response = client.get("/health")
    data = response.json()

    assert data["database"] == "ok"

def test_health_check_db_failure(client, mocker):
    mocker.patch("app.api.routes.get_db_conn", side_effect=Exception("DB is down!"))
    mocker.patch("app.api.routes.pool", side_effect=Exception("Poll is down"))
    
    response = client.get('/health')
    data = response.json()
    assert data["database"] == "fail"
