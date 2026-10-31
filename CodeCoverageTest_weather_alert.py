import pytest
from weather_alert import wind_alert, rain_alert, heat_alert, overall_alert

# Starter test cases
def test_calm_wind():
    assert wind_alert(10) == "none"

def test_no_alerts():
    assert overall_alert([]) == "none"

# Additional tests for line coverage of wind_alert
def test_wind_alert_warning():
    assert wind_alert(90) == "warning"

def test_wind_alert_watch():
    assert wind_alert(70) == "watch"

def test_wind_alert_advisory():
    assert wind_alert(45) == "advisory"

# Tests for line coverage of rain_alert
def test_rain_alert_warning():
    assert rain_alert(60, True) == "warning"

def test_rain_alert_watch_heavy_rain():
    assert rain_alert(60, False) == "watch"

def test_rain_alert_watch_moderate_rain():
    assert rain_alert(25, True) == "watch"

def test_rain_alert_advisory():
    assert rain_alert(25, False) == "advisory"

def test_rain_alert_none():
    assert rain_alert(5, False) == "none"

# Tests for line coverage of heat_alert
def test_heat_alert_warning_with_humidity():
    assert heat_alert(44, 60) == "warning"

def test_heat_alert_watch():
    assert heat_alert(40, 30) == "watch"

def test_heat_alert_advisory():
    assert heat_alert(36, 30) == "advisory"

def test_heat_alert_none():
    assert heat_alert(30, 30) == "none"

# Tests for line coverage of overall_alert
def test_overall_alert_valid_and_upgrade():
    assert overall_alert(["advisory", "warning"]) == "warning"

def test_overall_alert_invalid():
    with pytest.raises(ValueError, match="unknown alert"):
        overall_alert(["invalid_alert"])
