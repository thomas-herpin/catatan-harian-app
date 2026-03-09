from flask import Flask, jsonify, request

app = Flask(__name__)

catatan_list = []

# Endpoint untuk menambahkan catatan
@app.route('/catatan', methods=['POST'])
def add_catatan():
    data = request.get_json()
    if not data or 'judul' not in data or 'isi' not in data:
        return jsonify({"message": "Judul dan isi diperlukan!"}), 400
    
    new_catatan = {
        'id': len(catatan_list) + 1,
        'judul': data['judul'],
        'isi': data['isi']
    }
    catatan_list.append(new_catatan)
    return jsonify(new_catatan), 201

# Endpoint untuk mendapatkan semua catatan
@app.route('/catatan', methods=['GET'])
def get_catatan():
    return jsonify(catatan_list), 200

# Endpoint untuk mengubah catatan berdasarkan ID
@app.route('/catatan/<int:id>', methods=['PUT'])
def update_catatan(id):
    data = request.get_json()
    catatan = next((c for c in catatan_list if c['id'] == id), None)
    
    if not catatan:
        return jsonify({"message": "Catatan tidak ditemukan"}), 404
    
    catatan['judul'] = data['judul']
    catatan['isi'] = data['isi']
    return jsonify(catatan), 200

# Endpoint untuk menghapus catatan berdasarkan ID
@app.route('/catatan/<int:id>', methods=['DELETE'])
def delete_catatan(id):
    catatan = next((c for c in catatan_list if c['id'] == id), None)
    
    if not catatan:
        return jsonify({"message": "Catatan tidak ditemukan"}), 404
    
    catatan_list.remove(catatan)
    return jsonify({"message": "Catatan berhasil dihapus"}), 200

if __name__ == '__main__':
    app.run()