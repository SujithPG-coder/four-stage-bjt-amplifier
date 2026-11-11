"""Plot the measured frequency response of the 4-stage BJT amplifier.

    python plot_frequency_response.py
"""
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
df = pd.read_csv(ROOT / "data" / "measured_frequency_response.csv")

fig, ax = plt.subplots(figsize=(10, 5.5))
colors = ["#9fb3c8", "#5c88c4", "#2a9d8f", "#d1495b"]
for i, c in enumerate(colors, start=1):
    g = df[f"stage{i}_gain"]
    ax.semilogx(df.frequency_hz, 20 * np.log10(g), "o-", color=c, lw=2, ms=4,
                label=f"Output of stage {i}")

g4 = 20 * np.log10(df.stage4_gain)
mid = g4.max()
ax.axhline(mid - 3, color="#d1495b", ls=":", lw=1)
band = df.frequency_hz[g4 >= mid - 3]
ax.axvspan(band.min(), band.max(), color="#f4a261", alpha=0.12, label="-3 dB bandwidth (stage 4)")
ax.text(3e2, mid + 1.2, f"Mid-band gain ~ {df.stage4_gain.max():.0f} V/V ({mid:.1f} dB)",
        fontsize=10, color="#d1495b")
ax.set_xlabel("Frequency (Hz)")
ax.set_ylabel("Gain (dB)")
ax.set_title("Measured frequency response - 4-stage BC547 amplifier (Vin = 25 mV)", pad=12)
ax.set_ylim(top=mid + 5)
ax.grid(which="both", alpha=0.3)
ax.legend(loc="lower left")
fig.tight_layout()
out = ROOT / "docs" / "images" / "frequency_response.png"
fig.savefig(out, dpi=120)
print(f"Mid-band gain {mid:.2f} dB, -3 dB band ~ {band.min():g} Hz - {band.max():g} Hz")
print("Saved", out)
