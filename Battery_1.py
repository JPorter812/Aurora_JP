import pandas as pd


# battery that just charges and discharges at maximum rate.
class Battery:

    VALUES = "Values"

    # units are MW, hours, and £
    def __init__(self, battery_file):
        battery_specs = pd.read_excel(battery_file, index_col=0)
        self.max_charging = float(
            battery_specs.loc["Max charging rate"][Battery.VALUES]
        )
        self.max_discharge = float(
            battery_specs.loc["Max discharging rate"][Battery.VALUES]
        )
        self.max_storage_volume = float(
            battery_specs.loc["Max storage volume"][Battery.VALUES]
        )
        self.charge_efficiency = float(
            battery_specs.loc["Battery charging efficiency"][Battery.VALUES]
        )
        self.discharge_efficiency = float(
            battery_specs.loc["Battery discharging efficiency"][Battery.VALUES]
        )
        self.fixed_cost_per_year = float(
            battery_specs.loc["Fixed Operational Costs"][Battery.VALUES]
        )

        self.stored_energy = 0.0

    # returns energy successfully stored on battery
    def charge(self, time) -> bool:
        projected_stored_energy = self.stored_energy + self.max_discharge * time
        if projected_stored_energy > self.max_storage_volume + 0.00001:
            return False
        else:
            self.stored_energy = projected_stored_energy
        return True

    # returns energy successfully supplied to grid
    def discharge(self, time) -> bool:
        projected_stored_energy = self.stored_energy - self.max_discharge * time
        if projected_stored_energy < -0.00001:
            return False
        else:
            self.stored_energy = projected_stored_energy
            return True
