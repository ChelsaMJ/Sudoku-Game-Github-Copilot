import app as app_module


def test_new_route_returns_puzzle_and_stores_solution(client):
    response = client.get('/new?clues=35')

    assert response.status_code == 200
    payload = response.get_json()
    assert 'puzzle' in payload
    assert len(payload['puzzle']) == 9
    assert all(len(row) == 9 for row in payload['puzzle'])
    assert app_module.CURRENT['solution'] is not None


def test_check_route_reports_no_game_in_progress(client):
    app_module.CURRENT['solution'] = None

    response = client.post('/check', json={'board': [[0] * 9 for _ in range(9)]})

    assert response.status_code == 400
    assert response.get_json() == {'error': 'No game in progress'}


def test_check_route_reports_correct_and_incorrect_cells(client):
    client.get('/new')
    solution = app_module.CURRENT['solution']

    correct_response = client.post('/check', json={'board': solution})
    assert correct_response.status_code == 200
    assert correct_response.get_json() == {'incorrect': []}

    submitted_board = [row[:] for row in solution]
    submitted_board[0][0] = (solution[0][0] % 9) + 1
    incorrect_response = client.post('/check', json={'board': submitted_board})

    assert incorrect_response.status_code == 200
    assert incorrect_response.get_json() == {'incorrect': [[0, 0]]}


import pytest


@pytest.fixture
def client():
    app_module.app.config.update(TESTING=True)
    app_module.CURRENT['puzzle'] = None
    app_module.CURRENT['solution'] = None
    with app_module.app.test_client() as test_client:
        yield test_client
    app_module.CURRENT['puzzle'] = None
    app_module.CURRENT['solution'] = None
