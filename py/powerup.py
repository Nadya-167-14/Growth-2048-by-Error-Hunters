def pupuk(game_instance, row, col):
    if 0 <= row < game_instance.grid_size and 0 <= col < game_instance.grid_size:
        if game_instance.matrix[row][col] is not None:
            game_instance.matrix[row][col].value *= 2
            game_instance.score += game_instance.matrix[row][col].value 
        else:
            return
    else:
        return


def penyiram_otomatis(game_instance):
    game_instance.add_new_tile() 
    game_instance.score += 10


def bom(game_instance, row, col):
    if 0 <= row < game_instance.grid_size and 0 <= col < game_instance.grid_size:
        if game_instance.matrix[row][col] is not None:
            removed_tile = game_instance.matrix[row][col]
            removed_value = removed_tile.value
            
            game_instance.matrix[row][col] = None 
            
            if removed_tile in game_instance.tiles:
                game_instance.tiles.remove(removed_tile)

            game_instance.score -= removed_value // 2 
        else:
            return
    else:
        return
