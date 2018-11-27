# параметры зрения
raze_amount = 8
sector_size = 4

# кол-во нейроннов в слоях
inp_layer = 2*sector_size
hidden_layers = [4]
hidden_layers_count = len(hidden_layers)
out_layer = 3
mutation_rate = 1

step_amount = 15 # количество шагов

start_distance = 100
amount = 40  # всегда должно быть кратно 4

resource_radius = 20
cell_radius = 5
