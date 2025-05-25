# powerup.py

def pupuk(game_instance, row, col):
    # Menggunakan game_instance.grid_size untuk batas, dan game_instance.matrix untuk akses ubin
    if 0 <= row < game_instance.grid_size and 0 <= col < game_instance.grid_size:
        # Cek apakah ada Tile di posisi tersebut (tidak None)
        if game_instance.matrix[row][col] is not None:
            # Akses nilai Tile melalui objek Tile di matrix
            game_instance.matrix[row][col].value *= 2 # Gandakan nilai ubin
            game_instance.score += game_instance.matrix[row][col].value 
            print(f"Pupuk diterapkan di R{row}, C{col}. Nilai ubin: {game_instance.matrix[row][col].value}")
        else:
            print("Tidak bisa memupuk ubin kosong.")
    else:
        print(f"Koordinat pupuk di luar batas papan: ({row}, {col})")


def penyiram_otomatis(game_instance):
    print("Penyiram Otomatis diaktifkan! Menambahkan ubin baru.")
    game_instance.add_new_tile() # Ini seharusnya menambahkan Tile ke matrix
    game_instance.score += 10


def bom(game_instance, row, col):
    # Menggunakan game_instance.grid_size untuk batas, dan game_instance.matrix untuk akses ubin
    if 0 <= row < game_instance.grid_size and 0 <= col < game_instance.grid_size:
        # Cek apakah ada Tile di posisi tersebut
        if game_instance.matrix[row][col] is not None:
            removed_tile = game_instance.matrix[row][col]
            removed_value = removed_tile.value
            
            # Hapus ubin dari matrix (set ke None)
            game_instance.matrix[row][col] = None 
            
            # Hapus ubin dari list tiles agar tidak digambar lagi
            if removed_tile in game_instance.tiles:
                game_instance.tiles.remove(removed_tile)

            game_instance.score -= removed_value // 2 
            print(f"Bom diledakkan di R{row}, C{col}. Nilai {removed_value} dihilangkan.")
        else:
            print("Tidak ada ubin untuk dibom di lokasi ini.")
    else:
        print(f"Koordinat bom di luar batas papan: ({row}, {col})")
