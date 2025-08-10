# 🌪️ EMF Ambient Chaos Engine ⚡

A weekend project exploring electromagnetic field chaos patterns and their response to mobile device movement.

## What is this?

Just a fun little experiment I threw together to visualize how EMF patterns might behave around mobile devices. Nothing too fancy - just some chaos theory applied to RF detection with a simple PyQt6 interface.

## Features

- **Real-time chaos pattern generation** - Dynamic patterns that respond to device detection
- **Zone-based threat assessment** - Extended detection ranges with directional positioning
- **6 reflection types** - Dynamic, Quad, Swiss Energy, Ambient, Chaos Burst, Mirror
- **Intensity scaling** - Automatically adjusts based on device count and signal strength
- **Live visualization** - Terminal-style output with real-time updates

## Detection Zones

- **🎯 Center Zone**: 5m radius (critical threats)
- **⬇️ South Zone**: 25m radius (high threats) - *10m extension for early detection*
- **⬆️ North/➡️ East/⬅️ West**: 15m radius (medium threats)

## Quick Start

```bash
# Clone and run
git clone <this-repo>
cd emf-chaos-engine
pip3 install -r requirements.txt
python3 emf_chaos_engine_standalone.py
```

## Sample Output

```
[15:18:00] 🌪️ Chaos Pattern: swiss_energy_disruption | Intensity: 86% | Phones: 8
⚡ Chaos Detection Range: 8 devices | 🎯 Core Zone: 4 devices
🎯 Detection Zones: 1 SOUTH | 4 CENTER | 2 NORTH | 1 WEST
📱 iPhone: syn_0:0... (-51dBm) ⬆️NORTH 6.8m 🟡 → Mirror Reflection
📱 Google Pixel: syn_5:2... (-57dBm) ➡️EAST 12.4m 🟡 → Quad Reflection
📱 Unknown Device: syn_1:3... (-84dBm) ⬇️SOUTH 21.3m 🟠 → Mirror Reflection
```

## How It Works

1. **Device Detection**: Simulates mobile device detection across different zones
2. **Chaos Calculation**: Intensity scales with device count and signal strength (15% per device)
3. **Pattern Selection**: Automatically switches between 4 chaos patterns based on intensity
4. **Zone Classification**: Separates detection range from core protection zone

## Chaos Patterns

- **ambient_monitoring** (0-25% intensity)
- **dynamic_chaos** (25-50% intensity) 
- **quad_reflection** (50-75% intensity)
- **swiss_energy_disruption** (75%+ intensity)

## Requirements

- Python 3.8+
- PyQt6
- Basic understanding of chaos theory (optional but fun!)

## License

MIT - Feel free to experiment and extend!

## Notes

This is just a proof-of-concept for EMF pattern visualization. Real-world RF detection would require actual hardware and proper signal processing. But hey, it's fun to see chaos patterns in action! 🌪️

*Built in a weekend because why not explore some chaos theory?* ⚡
