from Battery_1 import Battery

battery_file = r"Second Round Technical Question - Attachment 1.xlsx"


def test_battery_parsing():
    battery = Battery(battery_file)
    assert battery.max_charging == 2.0
    assert battery.max_storage_volume == 4.0


def test_battery_charge():
    battery = Battery(battery_file)
    battery.charge(1, 1)
    assert battery.stored_energy == 1


def test_battery_discharge():
    battery = Battery(battery_file)
    battery.charge(2, 2)
    should_be_stored = 4.0
    assert battery.stored_energy == should_be_stored
    battery.discharge(2, 1)
    assert battery.stored_energy == 2.0


def test_battery_overcharge():
    battery = Battery(battery_file)
    battery.charge(2, 3)
    assert battery.stored_energy == 0.0
    battery.discharge(2, 3)
    assert battery.stored_energy == 0.0
