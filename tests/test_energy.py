import sys
import os
import time
# Ensure gapwatch modules can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gapwatch import energy

def test_green_meter_simulation():
    """Test the GreenMeter simulation flow and basic calculations."""
    # The config key in energy.py is co2_intensity_kg_per_kwh, not g_per_kwh
    # Also, the default value is 0.254 kg/kWh.
    # For testing, we can use a different value to ensure config is respected.
    meter = energy.GreenMeter(config={"co2_intensity_kg_per_kwh": 0.5}) # 0.5 kg CO2 per kWh
    
    meter.start_monitoring()
    # Simulate some work
    time.sleep(0.01) # Short sleep for testing
    meter.stop_monitoring()
    
    usage_data = meter.get_energy_usage(tokens_processed=100)
    
    assert "total_kwh" in usage_data
    assert "co2_emissions_kg" in usage_data
    assert "watt_hours_per_token" in usage_data
    
    assert usage_data["total_kwh"] > 0 
    # CO2 emissions depend on total_kwh and the intensity factor.
    # If total_kwh is positive, and intensity is positive, co2_emissions_kg should be positive.
    assert usage_data["co2_emissions_kg"] > 0
    assert usage_data["watt_hours_per_token"] > 0
    # Check if CO2 calculation is roughly correct: total_kwh * intensity
    assert abs(usage_data["co2_emissions_kg"] - (usage_data["total_kwh"] * 0.5)) < 0.0001


def test_green_meter_no_monitoring_calls():
    """Test behavior when get_energy_usage is called before monitoring."""
    meter = energy.GreenMeter()
    usage_data = meter.get_energy_usage()
    assert usage_data["total_kwh"] == 0.0
    assert usage_data["co2_emissions_kg"] == 0.0
    assert usage_data["watt_hours_per_token"] is None
    assert usage_data["elapsed_time_seconds"] == 0.0
