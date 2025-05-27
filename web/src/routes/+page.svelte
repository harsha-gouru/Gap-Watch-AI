<script>
  // Placeholder data - this will eventually come from GapWatch results
  let energyUsage = {
    total_kwh: 0.12,
    co2_emissions_kg: 0.05,
    watt_hours_per_token: 0.002
  };

  let accuracyData = {
    fp16: 0.85,
    quantized: 0.82,
    drop: 0.03,
    alert_triggered: false
  };

  let runId = "run_xyz123";
</script>

<svelte:head>
  <title>GapWatch-AI Dashboard</title>
</svelte:head>

<div style="font-family: sans-serif; padding: 20px;">
  <h1>GapWatch-AI Dashboard</h1>

  <section>
    <h2>Run ID: {runId}</h2>
  </section>

  <section>
    <h2>Energy Usage</h2>
    <p>Total kWh: {energyUsage.total_kwh}</p>
    <p>CO2 Emissions (kg): {energyUsage.co2_emissions_kg}</p>
    <p>Watt-hours / token: {energyUsage.watt_hours_per_token || 'N/A'}</p>
  </section>

  <section>
    <h2>Quantization Accuracy</h2>
    <p>FP16 Accuracy: {accuracyData.fp16}</p>
    <p>Quantized Accuracy: {accuracyData.quantized}</p>
    <p>Accuracy Drop: {accuracyData.drop.toFixed(3)}</p>
    {#if accuracyData.alert_triggered}
      <p style="color: red;"><strong>Alert: Accuracy drop exceeds threshold!</strong></p>
    {/if}
  </section>

  <section>
    <h2>Actions</h2>
    <button on:click={() => alert('Replay for ' + runId + ' initiated (simulation).')}>
      Replay Run
    </button>
  </section>

  <style>
    section {
      margin-bottom: 20px;
      padding: 15px;
      border: 1px solid #eee;
      border-radius: 5px;
    }
    h2 {
      margin-top: 0;
    }
  </style>
</div>
