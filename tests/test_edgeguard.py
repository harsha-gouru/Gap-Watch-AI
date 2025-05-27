import sys
import os
# Ensure gapwatch modules can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from gapwatch import edgeguard

def test_check_quantization_accuracy_no_alert():
    """Test EdgeGuard when accuracy drop is within threshold."""
    results = edgeguard.check_quantization_accuracy(
        model_fp16_path="dummy/fp16.pth",
        model_quantized_path="dummy/quant.pth",
        test_dataset_path="dummy/data.pt",
        accuracy_threshold_delta=0.05
    )
    # Default simulated values are 0.85 (fp16) and 0.82 (quantized) -> drop 0.03
    assert results["accuracy_fp16"] == 0.85 
    assert results["accuracy_quantized"] == 0.82
    assert abs(results["accuracy_drop"] - 0.03) < 0.001 # Using abs for float comparison
    assert results["alert_triggered"] is False

def test_check_quantization_accuracy_alert():
    """Test EdgeGuard when accuracy drop exceeds threshold."""
    results = edgeguard.check_quantization_accuracy(
        model_fp16_path="dummy/fp16.pth",
        model_quantized_path="dummy/quant.pth",
        test_dataset_path="dummy/data.pt",
        accuracy_threshold_delta=0.02 # Drop is 0.03, so this should trigger
    )
    assert results["alert_triggered"] is True
