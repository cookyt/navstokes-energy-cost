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
# https://www.eia.gov/energyexplained/units-and-calculators/british-thermal-units.php
btu_per_kwh = 3412
kwh_per_gasoline_gallon = btu_per_gasoline_gallon / btu_per_kwh

# https://www.eia.gov/tools/faqs/faq.php?id=97&t=3
kwh_per_house_year = 10_791

# https://www.autozone.com/diy/trustworthy-advice/what-is-considered-good-gas-mileage
typical_car_miles_per_gallon = 30

# https://afdc.energy.gov/vehicles/electric-emissions-sources
electric_vehicle_miles_per_kwh = 3.6

# https://en.wikipedia.org/wiki/Harvesting_lightning_energy
joules_per_lightning_bolt = 5e9
kwh_per_lightning_bolt = joules_per_lightning_bolt / joules_per_kwh

###########

navstokes_gpt5_flop = gpt5_flop_per_output_token * navstokes_output_tokens
navstokes_h100_seconds = navstokes_gpt5_flop / h100_typ_flop_per_second
navstokes_h100_joules = h100_typ_watts * navstokes_h100_seconds

navstokes_kwh = navstokes_h100_joules / joules_per_kwh
navstokes_tonne_co2 = navstokes_kwh * tonne_co2_per_kwh
navstokes_house_years = navstokes_kwh / kwh_per_house_year
navstokes_gasoline_gallons = navstokes_kwh / kwh_per_gasoline_gallon
navstokes_ice_car_miles = navstokes_gasoline_gallons * typical_car_miles_per_gallon
navstokes_ev_car_miles = navstokes_kwh * electric_vehicle_miles_per_kwh
navstokes_lightning_bolts = navstokes_kwh / kwh_per_lightning_bolt

def fmt(v):
  return f"{v:>12,.0f}"

print("Estimated Energy Cost of Open AI's Navier-Stokes Paper")
print(f"| {fmt(navstokes_kwh)} | KWh of Electricity |")
print(f"| {fmt(navstokes_tonne_co2)} | Tonnes of CO2 |")
print(f"| {fmt(navstokes_house_years)} | American homes powered for one year |")
print(f"| {fmt(navstokes_gasoline_gallons)} | Gallons of gasoline |")
print(f"| {fmt(navstokes_ice_car_miles)} | Miles driven in a mid-size gasoline-powered sedan |")
print(f"| {fmt(navstokes_ev_car_miles)} | Miles driven in a mid-size all-electric sedan |")
print(f"| {fmt(navstokes_lightning_bolts)} | Lightning Bolts |")
