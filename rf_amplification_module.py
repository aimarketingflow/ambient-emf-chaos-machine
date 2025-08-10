#!/usr/bin/env python3
"""
🌊 RF Signal Amplification Module ⚡
Lightweight RF amplification for EMF Chaos Engine
Uses detected device signals as carriers for extended range

Part of EMF Ambient Chaos Engine - Just a weekend project :)
"""

import math
import random
from typing import List, Dict

class SimpleRFAmplifier:
    """Lightweight RF signal amplification using detected device signals"""
    
    def __init__(self):
        self.amplification_modes = [
            'carrier_modulation',
            'harmonic_reflection', 
            'constructive_interference'
        ]
    
    def calculate_amplification(self, detected_devices: List[Dict], base_intensity: int) -> Dict:
        """Calculate amplification potential from detected devices"""
        if not detected_devices:
            return {'amplified_intensity': base_intensity, 'extended_range': 25, 'mode': 'none'}
        
        # Count strong signals that can act as carriers
        strong_signals = [d for d in detected_devices if d.get('signal', -100) > -60]
        carrier_count = len(strong_signals)
        
        # Calculate amplification factor
        amplification_factor = 1.0 + (carrier_count * 0.3)  # 30% boost per carrier
        amplified_intensity = min(100, int(base_intensity * amplification_factor))
        
        # Calculate extended range
        base_range = 25  # meters
        range_boost = carrier_count * 12  # 12m per carrier device
        extended_range = min(100, base_range + range_boost)
        
        # Select mode based on carrier count
        if carrier_count >= 4:
            mode = 'constructive_interference'
        elif carrier_count >= 2:
            mode = 'harmonic_reflection'
        else:
            mode = 'carrier_modulation'
        
        return {
            'amplified_intensity': amplified_intensity,
            'extended_range': extended_range,
            'amplification_factor': round(amplification_factor, 2),
            'carrier_count': carrier_count,
            'mode': mode,
            'coverage_area': round(math.pi * (extended_range ** 2), 1)
        }
    
    def get_amplification_summary(self, amp_data: Dict) -> str:
        """Get human-readable amplification summary"""
        if amp_data['mode'] == 'none':
            return "No amplification (no carriers detected)"
        
        range_increase = amp_data['extended_range'] - 25
        coverage_acres = amp_data['coverage_area'] / 4047  # Convert m² to acres
        
        return (f"🌊 {amp_data['mode'].replace('_', ' ').title()} | "
                f"Range: {amp_data['extended_range']}m (+{range_increase}m) | "
                f"Carriers: {amp_data['carrier_count']} | "
                f"Coverage: {coverage_acres:.1f} acres")

if __name__ == "__main__":
    # Test amplification
    amplifier = SimpleRFAmplifier()
    
    test_devices = [
        {'signal': -45, 'phone_type': 'iPhone'},
        {'signal': -52, 'phone_type': 'Android'},
        {'signal': -38, 'phone_type': 'Samsung'},
        {'signal': -67, 'phone_type': 'Unknown'}
    ]
    
    result = amplifier.calculate_amplification(test_devices, 75)
    summary = amplifier.get_amplification_summary(result)
    
    print("🌊 RF Amplification Test:")
    print(summary)
    print(f"⚡ Amplification Factor: {result['amplification_factor']}x")
    print(f"🎯 Coverage Area: {result['coverage_area']}m²")
