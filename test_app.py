import pytest
from app import app, catatan_list

@pytest.fixture
def client():
    catatan_list.clear()
    with app.test_client() as client:
        yield client

# Test untuk menambahkan catatan (POST)
def test_add_catatan(client):
    response = client.post('/catatan', json={"judul": "Catatan Pertama", "isi": "Ini adalah isi catatan pertama"})
    assert response.status_code == 201
    assert "id" in response.json
    assert response.json['judul'] == "Catatan Pertama"
    assert response.json['isi'] == "Ini adalah isi catatan pertama"

# Test untuk menambahkan catatan dengan data yang kurang (POST)
def test_add_catatan_invalid(client):
    response = client.post('/catatan', json={"judul": "Catatan Tanpa Isi"})
    assert response.status_code == 400
    assert response.json['message'] == "Judul dan isi diperlukan!"

# Test untuk melihat semua catatan (GET)
def test_get_catatan(client):
    client.post('/catatan', json={"judul": "Catatan Pertama", "isi": "Isi catatan pertama"})
    response = client.get('/catatan')
    assert response.status_code == 200
    assert response.json['jumlah_catatan'] == 1
    assert len(response.json['catatan']) == 1
    assert response.json['catatan'][0]['judul'] == "Catatan Pertama"

# Test untuk mengubah catatan (PUT)
def test_update_catatan(client):
    client.post('/catatan', json={"judul": "Catatan Pertama", "isi": "Isi catatan pertama"})
    response = client.put('/catatan/1', json={"judul": "Catatan Diperbarui", "isi": "Isi catatan yang diperbarui"})
    assert response.status_code == 200
    assert response.json['judul'] == "Catatan Diperbarui"
    assert response.json['isi'] == "Isi catatan yang diperbarui"

# Test untuk mengubah catatan yang tidak ada (PUT)
def test_update_catatan_not_found(client):
    response = client.put('/catatan/999', json={"judul": "Catatan Tidak Ada", "isi": "Isi catatan yang tidak ada"})
    assert response.status_code == 404
    assert response.json['message'] == "Catatan tidak ditemukan"

# Test untuk menghapus semua catatan
def test_delete_all_catatan(client):
    client.post('/catatan', json={"judul": "Catatan Pertama", "isi": "Isi catatan pertama"})
    client.post('/catatan', json={"judul": "Catatan Kedua", "isi": "Isi catatan kedua"})
    
    response = client.delete('/catatan/all')
    assert response.status_code == 200
    assert response.json['message'] == "Semua catatan berhasil dihapus"
    
    # Setelah penghapusan, tidak ada catatan yang tersisa
    response = client.get('/catatan')
    assert response.status_code == 200
    assert response.json['jumlah_catatan'] == 0
    assert len(response.json['catatan']) == 0