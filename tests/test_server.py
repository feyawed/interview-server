async def get_headers(cli):
    token = await get_token(cli)
    return {"Content-type": "application/json", "Authorization": f"Bearer {token}"}


async def get_token(cli):
    resp = await cli.post(
        "/api/auth",
        headers={"Content-type": "application/json"},
        json={"username": "test", "password": "1234"},
    )
    assert resp.status == 200, "Authentication Failed"
    resp_json = await resp.json()
    return resp_json["access_token"]


async def test_post_polydata(test_cli):
    headers = await get_headers(test_cli)
    data = {"data": [{"key": "key1", "val": "val1", "valType": "str"}]}
    resp = await test_cli.post("/api/poly", json=data, headers=headers)
    assert resp.status == 200
    resp_json = await resp.json()
    assert resp_json["object_id"]


async def test_get_polydata(test_cli):
    headers = await get_headers(test_cli)
    resp = await test_cli.get("/api/poly/2", headers=headers)
    assert resp.status == 200
    resp_json = await resp.json()
    assert resp_json["object_id"]


async def test_get_polydata_not_found(test_cli):
    headers = await get_headers(test_cli)
    resp = await test_cli.get("/api/poly/1222", headers=headers)
    assert resp.status == 404


async def test_delete_polydata(test_cli):
    headers = await get_headers(test_cli)
    resp = await test_cli.delete("/api/poly/1", headers=headers)
    assert resp.status == 204


async def test_no_headers(test_cli):
    resp = await test_cli.delete("/api/poly/1")
    assert resp.status == 400


async def test_auth(test_cli):
    resp = await test_cli.post(
        "/api/auth",
        headers={"Content-type": "application/json"},
        json={"username": "test", "password": "1234"},
    )
    assert resp.status == 200
    resp_json = await resp.json()
    assert resp_json["access_token"]


async def test_list_polydata(test_cli):
    headers = await get_headers(test_cli)
    resp = await test_cli.get("/api/poly", headers=headers)
    assert resp.status == 200
    resp_json = await resp.json()
    assert len(resp_json) > 0
