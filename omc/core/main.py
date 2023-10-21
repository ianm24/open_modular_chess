import omc.core.load_set as load_set

print(piece_map := load_set.get_piece_map("base_set"))
print(load_set.get_board("base_set", piece_map))
