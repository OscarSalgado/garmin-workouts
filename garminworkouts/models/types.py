SPORT_TYPES = {
    'running': 1,
    'trail_running': 1,
    'cycling': 2,
    'gravel_cycling': 2,
    'mountain_biking': 2,
    'swimming': 4,
    'strength_training': 5,
    'cardio_training': 6,
    'yoga': 7,
    'pilates': 8,
    'hiit': 9,
    'other': 3
}


INTENSITY_TYPES = {
    'active': 1,
    'rest': 2,
    'warmup': 3,
    'cooldown': 4,
}

STEP_TYPES = {
    'warmup': 1,
    'cooldown': 2,
    'run': 3,
    'interval': 3,
    'recovery': 4,
    'rest': 5,
    'repeat': 6,
    'other': 7
}

END_CONDITIONS = {
    'lap.button': 1,
    'time': 2,
    'distance': 3,
    'calories': 4,
    'iterations': 7,
    'fixed.rest': 8,
    'fixed.repetition': 9,
    'training.peaks.tss': 11,
    'repetition.time': 12,
    'time.at.valid.cda': 13,
    'power.last.lap': 14,
    'max.power.last.lap': 15,
    'reps': 10,
    'power': 5,         # Potencia por encima de un umbral ('endConditionCompare': 'gt')
                        # Potencia por debajo de un umbral ('endConditionCompare': 'lt')
    'heart.rate': 6,    # Pulsaciones por encima de un umbral ('endConditionCompare': 'lt')
                        # Pulsaciones por debajo de un umbral ('endConditionCompare': 'gt')
}

STROKE_TYPES = {
    'any_stroke': 1,         # Cualquiera
    'backstroke': 2,         # Espalda
    'breaststroke': 3,       # Braza
    'drill': 4,              # Tecnica
    'fly': 5,                # Mariposa
    'free': 6,               # Croll
    'individual_medley': 7,  # Estilos
    'mixed': 8,
}

EQUIPMENT_TYPES = {
    'fins': 1,          # Aletas
    'kickboard': 2,     # Tabla
    'paddles': 3,       # Palas
    'pull_buoy': 4,     # Pull buoy
    'snorkel': 5,       # Tubo buceo
    'none': 0           # Sin equipo
}

POOL_LENGTHS = {
    'short': 25,
    'olympic': 50
}

TARGET_TYPES = {
    'no.target': 1,
    'power.zone': 2,
    'cadence.zone': 3,
    'cadence': 3,
    'heart.rate.zone': 4,
    'speed.zone': 5,
    'pace.zone': 6,  # meters per second
    'grade': 7,
    'heart.rate.lap': 8,
    'power.lap': 9,
    'power.3s': 10,
    'power.10s': 11,
    'power.30s': 12,
    'speed.lap': 13,
    'swim.stroke': 14,
    'resistance': 15,
    'power.curve': 16
}

ACTIVITY_TYPES = {
    'running': 1,
    'cycling': 2,
    'hiking': 3, 'other': 4,
    'mountain_biking': 5,
    'trail_running': 6,
    'street_running': 7,
    'track_running': 8,
    'walking': 9,
    'road_biking': 10,
    'indoor_cardio': 11,
    'strength_training': 13,
    'casual_walking': 15,
    'speed_walking': 16,
    'all': 17,
    'treadmill_running': 18,
    'cyclocross': 19,
    'downhill_biking': 20,
    'track_cycling': 21,
    'recumbent_cycling': 22,
    'indoor_cycling': 25,
    'swimming': 26,
    'lap_swimming': 27,
    'open_water_swimming': 28,
    'fitness_equipment': 29,
    'elliptical': 30,
    'stair_climbing': 31,
    'indoor_rowing': 32,
    'mountaineering': 37,
    'wind_kite_surfing': 41,
    'horseback_riding': 44,
    'driving_general': 49,
    'flying': 52,
    'whitewater_rafting_kayaking': 60,
    'inline_skating': 63,
    'golf': 88,
    'multi_sport': 89,
    'steps': 108,
    'bmx': 131,
    'hunting_fishing': 133,
    'sky_diving': 134,
    'rc_drone': 136,
    'rock_climbing': 139,
    'hang_gliding': 140,
    'wingsuit_flying': 141,
    'gravel_cycling': 143,
    'diving': 144,
    'single_gas_diving': 145,
    'multi_gas_diving': 146,
    'gauge_diving': 147,
    'apnea_diving': 148,
    'floor_climbing': 150,
    'stop_watch': 151,
    'virtual_ride': 152,
    'virtual_run': 153,
    'obstacle_run': 154,
    'apnea_hunting': 155,
    'indoor_running': 156,
    'safety': 157,
    'assistance': 158,
    'incident_detected': 159,
    'pilates': 160,
    'ccr_diving': 161,
    'auto_racing': 162,
    'yoga': 163,
    'breathwork': 164,
    'winter_sports': 165,
    'snowmobiling_ws': 166,
    'snow_shoe_ws': 167,
    'skating_ws': 168,
    'backcountry_skiing_snowboarding_ws': 169,
    'skate_skiing_ws': 170,
    'cross_country_skiing_ws': 171,
    'resort_skiing_snowboarding_ws': 172,
    'indoor_climbing': 173,
    'bouldering': 174,
    'e_bike_mountain': 175,
    'e_bike_fitness': 176,
    'hiit': 180,
    'ultra_run': 181,
    'e_sport': 182,
    'motorcycling_v2': 185,
    'motocross_v2': 186,
    'atv_v2': 187,
    'transition_v2': 189,
    'swimToBikeTransition_v2': 190,
    'bikeToRunTransition_v2': 191,
    'runToBikeTransition_v2': 192,
    'hunting': 193,
    'backcountry_skiing': 203,
    'backcountry_snowboarding': 204,
    'disc_golf': 205,
    'team_sports': 206,
    'cricket': 207,
    'rugby': 208,
    'ice_hockey': 209,
    'field_hockey': 210,
    'lacrosse': 211,
    'volleyball': 212,
    'ultimate_disc': 213,
    'softball': 214,
    'soccer': 215,
    'american_football': 216,
    'basketball': 217,
    'baseball': 218,
    'racket_sports': 219,
    'table_tennis': 220,
    'platform_tennis': 221,
    'racquetball': 222,
    'squash': 223,
    'badminton': 224,
    'pickleball': 225,
    'paddelball': 226,
    'tennis_v2': 227,
    'water_sports': 228,
    'boating_v2': 229,
    'fishing_v2': 230,
    'kayaking_v2': 231,
    'kiteboarding_v2': 232,
    'offshore_grinding_v2': 233,
    'onshore_grinding_v2': 234,
    'paddling_v2': 235,
    'whitewater_rafting_v2': 236,
    'rowing_v2': 237,
    'sailing_v2': 238,
    'stand_up_paddleboarding_v2': 239,
    'surfing_v2': 240,
    'water_tubing': 241,
    'windsurfing_v2': 242,
    'wakeboarding_v2': 243,
    'wakesurfing': 244,
    'waterskiing': 245,
    'boxing': 246,
    'archery': 247,
    'mixed_martial_arts': 248,
    'overland': 249,
    'snorkeling': 250
    }