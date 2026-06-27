
def get_reynolds_number(V, chord, rho=1.225, mu=1.81e-5):
    return (rho * V * chord) / mu

def takeoff_distance(weight_N, thrust_N, wing_area, CL_max, rho):
   
    mu_rolling = 0.05 
    v_stall = math.sqrt((2 * weight_N) / (rho * wing_area * CL_max))
    distance = (1.21 * (weight_N / (thrust_N - mu_rolling * weight_N)) * v_stall**2) / (2 * 9.81)
    return distance

def battery_usable_energy(total_kwh, dod=0.8):
    return total_kwh * dod