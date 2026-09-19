#! /usr/bin/env py
# Calculations of how much energy it took OpenAI to solve Navier-Stokes.  Likely
# off by a factor of ~2-10, since I only counted output token energy cost on the
# GPU, so am missing things like communication costs between agents and input
# token costs.

# https://epoch.ai/gradient-updates/how-much-energy-does-chatgpt-use
gpt5_flop_per_output_token = 1e14 / 500
h100_max_flop_per_second = 9.89e14
h100_typ_flop_per_second = h100_max_flop_per_second * 0.1
h100_max_watts = 1500  # includes server overhead
h100_typ_watts = h100_max_watts * 0.7

# https://openai.com/index/navier-stokes-solution/
navstokes_output_tokens = 300e9

joules_per_kwh = 3.6e6

# https://www.epa.gov/energy/greenhouse-gas-equivalencies-calculator-calculations-and-references
tonne_co2_per_kwh = 3.94e-4 

# https://afdc.energy.gov/fuels/properties?fuels=GS
btu_per_gasoline_gallon = 114_102
btu_per_kwh = 3.409
kwh_per_gasoline_gallon = btu_per_gasoline_gallon / btu_per_kwh

# https://www.energy.gov/cmei/vehicles/articles/fotw-1360-sept-16-2024-typical-ev-87-91-efficient-compared-30-conventional
kwh_car_per_kwh = 0.3
kwh_car_per_gasoline_gallon = kwh_per_gasoline_gallon * kwh_car_per_kwh

###########

navstokes_gpt5_flop = gpt5_flop_per_output_token * navstokes_output_tokens
navstokes_h100_seconds = navstokes_gpt5_flop / h100_typ_flop_per_second
navstokes_h100_joules = h100_typ_watts * navstokes_h100_seconds

navstokes_kwh = navstokes_h100_joules / joules_per_kwh
navstokes_car_gasoline_gallons = navstokes_kwh / kwh_car_per_gasoline_gallon
navstokes_tonne_co2 = navstokes_kwh * tonne_co2_per_kwh

print("Estimated Energy Cost of Open AI's Navier-Stokes Paper")
print(f"{navstokes_kwh:>12,.2f} KWh")
print(f"{navstokes_car_gasoline_gallons:>12,.2f} Gallons of gasoline in an internal-combustion car")
print(f"{navstokes_tonne_co2:>12,.2f} Tonnes of CO2")

