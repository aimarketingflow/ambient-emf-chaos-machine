#!/usr/bin/env python3
"""
Environmental RF Propagation Module for EMF Chaos Engine
Integrates real-time wind direction, humidity, and atmospheric conditions as RF factors
"""

import requests
import json
import math
import time
from typing import Dict, Tuple, Optional
from datetime import datetime

class EnvironmentalRFFactors:
    """
    Integrates environmental conditions into EMF chaos calculations
    - Wind direction affects RF beam steering and atmospheric ducting
    - Humidity impacts RF absorption and multipath propagation
    - Temperature gradients create atmospheric layers affecting signal bounce
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or "demo_key"  # Use demo for testing
        self.last_weather_update = 0
        self.weather_cache = {}
        self.location = self.get_current_location()
        
    def get_current_location(self) -> Dict[str, float]:
        """Get current location - San Diego Hillcrest"""
        return {
            'lat': 32.7503,  # San Diego Hillcrest coordinates
            'lon': -117.1661,
            'name': 'San Diego Hillcrest, CA'
        }
    
    def fetch_weather_data(self) -> Dict:
        """Fetch real-time weather data including wind and humidity"""
        current_time = time.time()
        
        # Cache weather data for 10 minutes to avoid API spam
        if current_time - self.last_weather_update < 600 and self.weather_cache:
            return self.weather_cache
        
        try:
            # Using OpenWeatherMap API (free tier)
            url = f"http://api.openweathermap.org/data/2.5/weather"
            params = {
                'lat': self.location['lat'],
                'lon': self.location['lon'],
                'appid': self.api_key,
                'units': 'metric'
            }
            
            response = requests.get(url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                self.weather_cache = self.parse_weather_data(data)
                self.last_weather_update = current_time
                return self.weather_cache
            else:
                # Fallback to simulated data
                return self.generate_simulated_weather()
                
        except Exception as e:
            print(f"Weather API error: {e}")
            return self.generate_simulated_weather()
    
    def parse_weather_data(self, data: Dict) -> Dict:
        """Parse weather API response into RF-relevant factors"""
        return {
            'wind_speed': data.get('wind', {}).get('speed', 0),  # m/s
            'wind_direction': data.get('wind', {}).get('deg', 0),  # degrees
            'humidity': data.get('main', {}).get('humidity', 50),  # percentage
            'temperature': data.get('main', {}).get('temp', 20),  # celsius
            'pressure': data.get('main', {}).get('pressure', 1013),  # hPa
            'visibility': data.get('visibility', 10000) / 1000,  # km
            'timestamp': datetime.now().strftime("%H:%M:%S"),
            'location': self.location['name']
        }
    
    def generate_simulated_weather(self) -> Dict:
        """Generate realistic simulated weather data for San Diego Hillcrest"""
        import random
        
        # Simulate San Diego weather patterns
        base_wind_dir = random.randint(240, 280)  # Prevailing westerly winds from Pacific
        wind_variation = random.randint(-20, 20)
        
        return {
            'wind_speed': round(random.uniform(1.5, 6.5), 1),  # Typical San Diego winds
            'wind_direction': (base_wind_dir + wind_variation) % 360,
            'humidity': random.randint(55, 85),  # San Diego coastal humidity
            'temperature': round(random.uniform(18, 28), 1),  # San Diego temperatures
            'pressure': random.randint(1012, 1018),
            'visibility': round(random.uniform(10, 20), 1),  # Excellent visibility
            'timestamp': datetime.now().strftime("%H:%M:%S"),
            'location': self.location['name'],
            'simulated': True
        }
    
    def calculate_wind_rf_impact(self, weather: Dict) -> Dict:
        """Calculate how wind affects RF propagation"""
        wind_speed = weather['wind_speed']
        wind_direction = weather['wind_direction']
        
        # Wind creates atmospheric turbulence affecting RF paths
        turbulence_factor = min(wind_speed / 10.0, 1.0)  # Normalize to 0-1
        
        # Wind direction affects beam steering (atmospheric ducting)
        # Convert wind direction to RF impact zones
        wind_rad = math.radians(wind_direction)
        
        # Calculate directional RF enhancement/degradation
        rf_zones = {}
        for zone_angle in range(0, 360, 45):  # 8 directional zones
            zone_rad = math.radians(zone_angle)
            
            # Calculate wind alignment with RF zone
            alignment = math.cos(wind_rad - zone_rad)
            
            # Wind can enhance or degrade RF in different directions
            if alignment > 0:  # Wind blowing toward zone
                enhancement = 1.0 + (alignment * turbulence_factor * 0.15)
            else:  # Wind blowing away from zone
                enhancement = 1.0 + (alignment * turbulence_factor * 0.08)
            
            rf_zones[f"zone_{zone_angle}"] = round(enhancement, 3)
        
        return {
            'turbulence_factor': round(turbulence_factor, 3),
            'primary_enhancement_direction': wind_direction,
            'zone_factors': rf_zones,
            'overall_impact': round(1.0 + (turbulence_factor * 0.1), 3)
        }
    
    def calculate_humidity_rf_impact(self, weather: Dict) -> Dict:
        """Calculate how humidity affects RF absorption and multipath"""
        humidity = weather['humidity']
        temperature = weather['temperature']
        
        # Humidity increases RF absorption, especially at higher frequencies
        # More humid air = more RF attenuation
        humidity_factor = humidity / 100.0
        
        # Temperature affects humidity's impact on RF
        temp_factor = 1.0 + ((temperature - 20) / 100.0)  # Baseline at 20°C
        
        # Calculate frequency-dependent absorption
        absorption_2_4ghz = humidity_factor * temp_factor * 0.05  # 2.4GHz impact
        absorption_5ghz = humidity_factor * temp_factor * 0.12    # 5GHz impact
        
        # Humidity also affects multipath propagation
        multipath_factor = 1.0 + (humidity_factor * 0.08)
        
        # Range impact (higher humidity = shorter range)
        range_factor = 1.0 - (humidity_factor * 0.06)
        
        return {
            'humidity_factor': round(humidity_factor, 3),
            'absorption_2_4ghz': round(absorption_2_4ghz, 3),
            'absorption_5ghz': round(absorption_5ghz, 3),
            'multipath_factor': round(multipath_factor, 3),
            'range_factor': round(range_factor, 3),
            'overall_impact': round(range_factor * multipath_factor, 3)
        }
    
    def calculate_atmospheric_ducting(self, weather: Dict) -> Dict:
        """Calculate atmospheric ducting effects on RF propagation"""
        pressure = weather['pressure']
        humidity = weather['humidity']
        temperature = weather['temperature']
        
        # Atmospheric ducting can extend RF range significantly
        # Occurs with specific pressure/temperature/humidity gradients
        
        # Standard atmosphere baseline
        standard_pressure = 1013.25
        pressure_gradient = (pressure - standard_pressure) / standard_pressure
        
        # Temperature inversion conditions
        temp_factor = 1.0 - (abs(temperature - 18) / 50.0)  # Optimal around 18°C
        
        # Humidity gradient effect
        humidity_gradient = (humidity - 60) / 100.0  # Optimal around 60%
        
        # Calculate ducting probability and strength
        ducting_conditions = (
            abs(pressure_gradient) * 0.4 +
            temp_factor * 0.3 +
            abs(humidity_gradient) * 0.3
        )
        
        ducting_strength = max(0, min(ducting_conditions, 1.0))
        
        # Ducting can extend range by 20-50% under ideal conditions
        range_extension = 1.0 + (ducting_strength * 0.35)
        
        return {
            'ducting_probability': round(ducting_strength, 3),
            'range_extension': round(range_extension, 3),
            'pressure_factor': round(pressure_gradient, 3),
            'optimal_conditions': ducting_strength > 0.6
        }
    
    def get_comprehensive_rf_environment(self) -> Dict:
        """Get complete environmental RF analysis"""
        weather = self.fetch_weather_data()
        
        wind_impact = self.calculate_wind_rf_impact(weather)
        humidity_impact = self.calculate_humidity_rf_impact(weather)
        ducting_impact = self.calculate_atmospheric_ducting(weather)
        
        # Calculate overall environmental RF factor
        overall_factor = (
            wind_impact['overall_impact'] * 0.3 +
            humidity_impact['overall_impact'] * 0.4 +
            ducting_impact['range_extension'] * 0.3
        )
        
        return {
            'timestamp': weather['timestamp'],
            'location': weather['location'],
            'weather_conditions': weather,
            'wind_rf_impact': wind_impact,
            'humidity_rf_impact': humidity_impact,
            'atmospheric_ducting': ducting_impact,
            'overall_rf_factor': round(overall_factor, 3),
            'range_modifier': round(overall_factor, 3),
            'optimal_directions': self.get_optimal_rf_directions(wind_impact, ducting_impact)
        }
    
    def get_optimal_rf_directions(self, wind_impact: Dict, ducting_impact: Dict) -> Dict:
        """Determine optimal RF transmission directions based on environmental factors"""
        zone_factors = wind_impact['zone_factors']
        
        # Find best and worst directions
        best_zone = max(zone_factors.items(), key=lambda x: x[1])
        worst_zone = min(zone_factors.items(), key=lambda x: x[1])
        
        return {
            'best_direction': int(best_zone[0].split('_')[1]),
            'best_enhancement': best_zone[1],
            'worst_direction': int(worst_zone[0].split('_')[1]),
            'worst_degradation': worst_zone[1],
            'ducting_active': ducting_impact['optimal_conditions']
        }

# Example usage and testing
if __name__ == "__main__":
    print("🌪️ Environmental RF Factors Module Test")
    print("=" * 50)
    
    env_rf = EnvironmentalRFFactors()
    
    # Get comprehensive environmental analysis
    rf_env = env_rf.get_comprehensive_rf_environment()
    
    print(f"📍 Location: {rf_env['location']}")
    print(f"⏰ Time: {rf_env['timestamp']}")
    print()
    
    weather = rf_env['weather_conditions']
    print("🌤️ Weather Conditions:")
    print(f"   Wind: {weather['wind_speed']} m/s @ {weather['wind_direction']}°")
    print(f"   Humidity: {weather['humidity']}%")
    print(f"   Temperature: {weather['temperature']}°C")
    print(f"   Pressure: {weather['pressure']} hPa")
    print()
    
    print("📡 RF Impact Analysis:")
    print(f"   Overall RF Factor: {rf_env['overall_rf_factor']}")
    print(f"   Range Modifier: {rf_env['range_modifier']}")
    print()
    
    optimal = rf_env['optimal_directions']
    print("🎯 Optimal RF Directions:")
    print(f"   Best Direction: {optimal['best_direction']}° (enhancement: {optimal['best_enhancement']})")
    print(f"   Worst Direction: {optimal['worst_direction']}° (factor: {optimal['worst_degradation']})")
    print(f"   Atmospheric Ducting: {'ACTIVE' if optimal['ducting_active'] else 'INACTIVE'}")
    
    if 'simulated' in weather:
        print("\n⚠️  Using simulated weather data (no API key provided)")
