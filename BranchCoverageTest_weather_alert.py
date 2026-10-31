import pytest
from weather_alert import wind_alert, rain_alert, heat_alert, overall_alert

# Starter test cases
def test_calm_wind():
    assert wind_alert(10) == "none"

def test_no_alerts():
    assert overall_alert([]) == "none"

# ==========================================
# Branch Coverage Tests for wind_alert
# ==========================================
def test_wind_alert_warning_boundary():
    # speed_kmh >= 89 (True branch at line 5)
    assert wind_alert(89) == "warning"
    assert wind_alert(100) == "warning"

def test_wind_alert_watch_boundary():
    # speed_kmh >= 89 (False) and speed_kmh >= 62 (True branch at line 7)
    assert wind_alert(88) == "watch"
    assert wind_alert(62) == "watch"

def test_wind_alert_advisory_boundary():
    # speed_kmh >= 62 (False) and speed_kmh >= 39 (True branch at line 9)
    assert wind_alert(61) == "advisory"
    assert wind_alert(39) == "advisory"

def test_wind_alert_none_boundary():
    # speed_kmh >= 39 (False branch at line 9, fall through to line 11)
    assert wind_alert(38) == "none"
    assert wind_alert(0) == "none"

# ==========================================
# Branch Coverage Tests for rain_alert
# ==========================================
def test_rain_alert_heavy_saturated():
    # mm_per_hour >= 50 (True), soil_saturated (True) -> warning
    assert rain_alert(50, True) == "warning"
    assert rain_alert(80, True) == "warning"

def test_rain_alert_heavy_not_saturated():
    # mm_per_hour >= 50 (True), soil_saturated (False) -> watch
    assert rain_alert(50, False) == "watch"
    assert rain_alert(75, False) == "watch"

def test_rain_alert_moderate_saturated():
    # mm_per_hour >= 50 (False), mm_per_hour >= 10 (True), soil_saturated (True) -> watch
    assert rain_alert(49, True) == "watch"
    assert rain_alert(10, True) == "watch"

def test_rain_alert_moderate_not_saturated():
    # mm_per_hour >= 50 (False), mm_per_hour >= 10 (True), soil_saturated (False) -> advisory
    assert rain_alert(49, False) == "advisory"
    assert rain_alert(10, False) == "advisory"

def test_rain_alert_light_soil_saturated():
    # mm_per_hour >= 10 (False), soil_saturated (True) -> none
    assert rain_alert(9, True) == "none"
    assert rain_alert(0, True) == "none"

def test_rain_alert_light_soil_not_saturated():
    # mm_per_hour >= 10 (False), soil_saturated (False) -> none
    assert rain_alert(9, False) == "none"
    assert rain_alert(0, False) == "none"

# ==========================================
# Branch Coverage Tests for heat_alert
# ==========================================
def test_heat_alert_humidity_branch_true_warning():
    # humidity > 40 (True), index >= 45 (True) -> warning
    # temp_c = 44, humidity = 50 -> index = 44 + (50-40)*0.1 = 45.0
    assert heat_alert(44, 50) == "warning"

def test_heat_alert_humidity_branch_false_warning():
    # humidity > 40 (False), index >= 45 (True) -> warning
    assert heat_alert(45, 40) == "warning"
    assert heat_alert(46, 30) == "warning"

def test_heat_alert_watch_boundary():
    # index >= 45 (False), index >= 40 (True)
    # 1. humidity > 40 (False): temp_c = 40, humidity = 40 -> index = 40.0
    assert heat_alert(40, 40) == "watch"
    # 2. humidity > 40 (True): temp_c = 38, humidity = 60 -> index = 38 + 2.0 = 40.0
    assert heat_alert(38, 60) == "watch"
    # Just below 45
    assert heat_alert(44.9, 40) == "watch"

def test_heat_alert_advisory_boundary():
    # index >= 40 (False), index >= 35 (True)
    # 1. humidity <= 40: temp_c = 35, humidity = 40 -> index = 35.0
    assert heat_alert(35, 40) == "advisory"
    # 2. humidity > 40: temp_c = 34, humidity = 50 -> index = 34 + 1.0 = 35.0
    assert heat_alert(34, 50) == "advisory"
    # Just below 40
    assert heat_alert(39.9, 40) == "advisory"

def test_heat_alert_none_boundary():
    # index >= 35 (False) -> none
    # 1. humidity <= 40: temp_c = 34.9, humidity = 40 -> index = 34.9
    assert heat_alert(34.9, 40) == "none"
    # 2. humidity > 40: temp_c = 30, humidity = 45 -> index = 30.5
    assert heat_alert(30, 45) == "none"

# ==========================================
# Branch Coverage Tests for overall_alert
# ==========================================
def test_overall_alert_empty_list():
    # Loop 0 iterations (line 41 False branch)
    assert overall_alert([]) == "none"

def test_overall_alert_single_element():
    # Loop 1 iteration
    assert overall_alert(["watch"]) == "watch"

def test_overall_alert_increasing_severity():
    # SEVERITY[alert] > SEVERITY[worst] (True branch at line 44)
    assert overall_alert(["none", "advisory", "watch", "warning"]) == "warning"

def test_overall_alert_decreasing_severity():
    # SEVERITY[alert] > SEVERITY[worst] (False branch at line 44)
    assert overall_alert(["warning", "watch", "advisory", "none"]) == "warning"

def test_overall_alert_duplicate_severity():
    # SEVERITY[alert] > SEVERITY[worst] (False branch at line 44 with equal severity)
    assert overall_alert(["advisory", "advisory"]) == "advisory"

def test_overall_alert_invalid_alert():
    # alert not in SEVERITY (True branch at line 42)
    with pytest.raises(ValueError, match="unknown alert"):
        overall_alert(["tornado"])

def test_overall_alert_invalid_alert_mixed():
    # Invalid alert after valid alert
    with pytest.raises(ValueError, match="unknown alert"):
        overall_alert(["watch", "invalid"])
