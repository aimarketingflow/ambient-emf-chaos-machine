#!/usr/bin/env python3
"""
Threat Intelligence Module for EMF Chaos Engine
Deep analysis of suspicious networks: FSD_EMS and SneakyLinc
"""

import subprocess
import json
import time
import re
from typing import Dict, List, Optional
from datetime import datetime
import requests
from dataclasses import dataclass

@dataclass
class ThreatProfile:
    """Data structure for threat analysis"""
    network_name: str
    threat_level: str
    analysis_timestamp: str
    signal_patterns: Dict
    security_assessment: Dict
    behavioral_patterns: List
    intelligence_notes: List
    risk_indicators: List

class ThreatIntelligenceAnalyzer:
    """
    Advanced threat intelligence and analysis for suspicious networks
    """
    
    def __init__(self):
        self.threat_database = {
            'FSD_EMS': {
                'full_name': 'FSD Emergency Management System',
                'category': 'Government/Emergency Services',
                'threat_level': 'MEDIUM-HIGH',
                'known_indicators': [
                    'Enterprise-grade security (WPA2-Enterprise)',
                    'Government/Emergency naming convention',
                    'Consistent close-range presence',
                    'Professional network configuration'
                ],
                'analysis_focus': [
                    'Signal strength patterns',
                    'Security protocol analysis',
                    'Operational timing patterns',
                    'Geographic correlation'
                ]
            },
            'SNEAKYLINC': {
                'full_name': 'SneakyLinc/SneakyLync Stealth Network',
                'category': 'Unknown Stealth Operations',
                'threat_level': 'HIGH',
                'known_indicators': [
                    'Intentionally suspicious naming',
                    'WPA3 advanced security',
                    'Variable spelling (LinC/LynC)',
                    'Close-range stealth operations'
                ],
                'analysis_focus': [
                    'Stealth behavior patterns',
                    'Security evasion techniques',
                    'Operational methodology',
                    'Communication patterns'
                ]
            }
        }
        
        self.intelligence_history = []
        self.behavioral_patterns = {}
        
    def analyze_network_intelligence(self, network_name: str, detection_data: Dict) -> ThreatProfile:
        """Perform deep intelligence analysis on detected network"""
        
        network_key = network_name.upper()
        base_intel = self.threat_database.get(network_key, {})
        
        # Signal pattern analysis
        signal_patterns = self.analyze_signal_patterns(detection_data)
        
        # Security assessment
        security_assessment = self.analyze_security_profile(detection_data)
        
        # Behavioral pattern analysis
        behavioral_patterns = self.analyze_behavioral_patterns(network_name, detection_data)
        
        # Risk indicator analysis
        risk_indicators = self.assess_risk_indicators(network_name, detection_data)
        
        # Intelligence notes compilation
        intelligence_notes = self.compile_intelligence_notes(network_name, detection_data, base_intel)
        
        # Create threat profile
        threat_profile = ThreatProfile(
            network_name=network_name,
            threat_level=base_intel.get('threat_level', 'UNKNOWN'),
            analysis_timestamp=datetime.now().isoformat(),
            signal_patterns=signal_patterns,
            security_assessment=security_assessment,
            behavioral_patterns=behavioral_patterns,
            intelligence_notes=intelligence_notes,
            risk_indicators=risk_indicators
        )
        
        # Store in intelligence history
        self.intelligence_history.append(threat_profile)
        
        return threat_profile
    
    def analyze_signal_patterns(self, detection_data: Dict) -> Dict:
        """Analyze RF signal patterns and characteristics"""
        
        network = detection_data.get('network', {})
        rssi = network.get('rssi', 0)
        channel = network.get('channel', 'Unknown')
        
        # Signal strength analysis
        if rssi > -40:
            proximity = 'VERY_CLOSE'
            proximity_risk = 'HIGH'
        elif rssi > -55:
            proximity = 'CLOSE'
            proximity_risk = 'MEDIUM'
        else:
            proximity = 'DISTANT'
            proximity_risk = 'LOW'
        
        # Channel analysis
        channel_analysis = self.analyze_channel_usage(channel)
        
        return {
            'rssi': rssi,
            'proximity': proximity,
            'proximity_risk': proximity_risk,
            'channel': channel,
            'channel_analysis': channel_analysis,
            'signal_quality': 'STRONG' if rssi > -50 else 'MODERATE' if rssi > -65 else 'WEAK'
        }
    
    def analyze_channel_usage(self, channel: str) -> Dict:
        """Analyze WiFi channel usage patterns"""
        
        try:
            channel_num = int(channel)
        except:
            return {'analysis': 'Unknown channel format', 'risk': 'UNKNOWN'}
        
        # 2.4 GHz band analysis
        if channel_num in [1, 6, 11]:
            return {
                'band': '2.4GHz',
                'analysis': 'Standard non-overlapping channel',
                'risk': 'LOW',
                'notes': 'Common consumer/business usage'
            }
        elif 1 <= channel_num <= 14:
            return {
                'band': '2.4GHz',
                'analysis': 'Overlapping channel usage',
                'risk': 'MEDIUM',
                'notes': 'May indicate interference avoidance or stealth'
            }
        
        # 5 GHz band analysis
        elif 36 <= channel_num <= 165:
            return {
                'band': '5GHz',
                'analysis': 'Professional/enterprise channel',
                'risk': 'MEDIUM',
                'notes': 'Higher-end equipment, professional deployment'
            }
        
        return {
            'band': 'UNKNOWN',
            'analysis': 'Non-standard channel',
            'risk': 'HIGH',
            'notes': 'Unusual channel selection may indicate specialized equipment'
        }
    
    def analyze_security_profile(self, detection_data: Dict) -> Dict:
        """Analyze network security configuration"""
        
        network = detection_data.get('network', {})
        security = network.get('security', 'Unknown')
        
        # Security protocol analysis
        if 'WPA3' in security:
            security_level = 'VERY_HIGH'
            security_notes = 'Latest WPA3 encryption - professional/advanced deployment'
            threat_indicator = 'HIGH - Advanced security suggests serious operations'
        elif 'WPA2-Enterprise' in security:
            security_level = 'HIGH'
            security_notes = 'Enterprise-grade authentication - corporate/government'
            threat_indicator = 'MEDIUM-HIGH - Enterprise deployment'
        elif 'WPA2' in security:
            security_level = 'MEDIUM'
            security_notes = 'Standard WPA2 encryption - consumer/business'
            threat_indicator = 'LOW-MEDIUM - Standard security'
        else:
            security_level = 'LOW'
            security_notes = 'Weak or no encryption'
            threat_indicator = 'UNKNOWN - Unusual security configuration'
        
        return {
            'protocol': security,
            'security_level': security_level,
            'security_notes': security_notes,
            'threat_indicator': threat_indicator,
            'enterprise_grade': 'Enterprise' in security or 'WPA3' in security
        }
    
    def analyze_behavioral_patterns(self, network_name: str, detection_data: Dict) -> List:
        """Analyze network behavioral patterns over time"""
        
        patterns = []
        
        # Track detection frequency
        network_key = network_name.upper()
        if network_key not in self.behavioral_patterns:
            self.behavioral_patterns[network_key] = {
                'detections': [],
                'signal_history': [],
                'first_seen': datetime.now().isoformat()
            }
        
        # Add current detection
        self.behavioral_patterns[network_key]['detections'].append({
            'timestamp': datetime.now().isoformat(),
            'rssi': detection_data.get('network', {}).get('rssi', 0),
            'channel': detection_data.get('network', {}).get('channel', 'Unknown')
        })
        
        detection_count = len(self.behavioral_patterns[network_key]['detections'])
        
        # Behavioral analysis
        if detection_count == 1:
            patterns.append("First detection - establishing baseline")
        elif detection_count > 1:
            patterns.append(f"Multiple detections ({detection_count}) - persistent presence")
            
            # Signal strength consistency analysis
            rssi_values = [d['rssi'] for d in self.behavioral_patterns[network_key]['detections']]
            rssi_variance = max(rssi_values) - min(rssi_values)
            
            if rssi_variance < 10:
                patterns.append("Consistent signal strength - stationary or fixed position")
            else:
                patterns.append("Variable signal strength - mobile or power management")
        
        # Network-specific behavioral analysis
        if network_name.upper() == 'FSD_EMS':
            patterns.extend([
                "Government/Emergency naming convention",
                "Enterprise security deployment",
                "Potential emergency services infrastructure"
            ])
        elif 'SNEAKY' in network_name.upper():
            patterns.extend([
                "Intentionally suspicious naming",
                "Advanced WPA3 security",
                "Possible stealth/covert operations"
            ])
        
        return patterns
    
    def assess_risk_indicators(self, network_name: str, detection_data: Dict) -> List:
        """Assess risk indicators for the network"""
        
        risk_indicators = []
        
        network = detection_data.get('network', {})
        rssi = network.get('rssi', 0)
        security = network.get('security', '')
        
        # Proximity-based risk
        if rssi > -40:
            risk_indicators.append("VERY CLOSE PROXIMITY - Immediate area surveillance capability")
        elif rssi > -55:
            risk_indicators.append("CLOSE PROXIMITY - Local area monitoring capability")
        
        # Security-based risk
        if 'WPA3' in security:
            risk_indicators.append("ADVANCED SECURITY - Professional/serious operations")
        if 'Enterprise' in security:
            risk_indicators.append("ENTERPRISE DEPLOYMENT - Corporate/government infrastructure")
        
        # Name-based risk
        if 'EMS' in network_name.upper():
            risk_indicators.append("EMERGENCY SERVICES - Potential government/first responder network")
        if 'SNEAKY' in network_name.upper():
            risk_indicators.append("INTENTIONAL STEALTH - Deliberately suspicious naming")
        
        # Pattern-based risk
        network_key = network_name.upper()
        if network_key in self.behavioral_patterns:
            detection_count = len(self.behavioral_patterns[network_key]['detections'])
            if detection_count > 2:
                risk_indicators.append(f"PERSISTENT PRESENCE - {detection_count} detections")
        
        return risk_indicators
    
    def compile_intelligence_notes(self, network_name: str, detection_data: Dict, base_intel: Dict) -> List:
        """Compile comprehensive intelligence notes"""
        
        notes = []
        
        # Base intelligence
        if base_intel:
            notes.append(f"CATEGORY: {base_intel.get('category', 'Unknown')}")
            notes.append(f"THREAT LEVEL: {base_intel.get('threat_level', 'Unknown')}")
            
            known_indicators = base_intel.get('known_indicators', [])
            for indicator in known_indicators:
                notes.append(f"INDICATOR: {indicator}")
        
        # Current detection analysis
        network = detection_data.get('network', {})
        notes.append(f"CURRENT SIGNAL: {network.get('rssi', 0)} dBm")
        notes.append(f"CHANNEL: {network.get('channel', 'Unknown')}")
        notes.append(f"SECURITY: {network.get('security', 'Unknown')}")
        
        # Threat assessment
        threat_assessment = detection_data.get('threat_assessment', {})
        if threat_assessment:
            notes.append(f"ASSESSMENT: {threat_assessment.get('assessment', 'Unknown')}")
        
        # Pattern matching
        pattern_matched = detection_data.get('pattern_matched', '')
        match_type = detection_data.get('match_type', '')
        if pattern_matched:
            notes.append(f"PATTERN MATCH: '{pattern_matched}' ({match_type})")
        
        # Timestamp
        notes.append(f"DETECTION TIME: {detection_data.get('detection_time', 'Unknown')}")
        
        return notes
    
    def generate_intelligence_report(self, threat_profile: ThreatProfile) -> str:
        """Generate comprehensive intelligence report"""
        
        report = []
        report.append("🎯 EMF CHAOS ENGINE - THREAT INTELLIGENCE REPORT")
        report.append("=" * 60)
        report.append(f"📡 Network: {threat_profile.network_name}")
        report.append(f"⚠️  Threat Level: {threat_profile.threat_level}")
        report.append(f"📅 Analysis Time: {threat_profile.analysis_timestamp}")
        report.append("")
        
        # Signal Analysis
        report.append("📶 SIGNAL PATTERN ANALYSIS:")
        signal = threat_profile.signal_patterns
        report.append(f"   RSSI: {signal['rssi']} dBm ({signal['proximity']})")
        report.append(f"   Channel: {signal['channel']} ({signal['channel_analysis']['band']})")
        report.append(f"   Signal Quality: {signal['signal_quality']}")
        report.append(f"   Proximity Risk: {signal['proximity_risk']}")
        report.append("")
        
        # Security Analysis
        report.append("🔒 SECURITY ASSESSMENT:")
        security = threat_profile.security_assessment
        report.append(f"   Protocol: {security['protocol']}")
        report.append(f"   Security Level: {security['security_level']}")
        report.append(f"   Enterprise Grade: {security['enterprise_grade']}")
        report.append(f"   Threat Indicator: {security['threat_indicator']}")
        report.append("")
        
        # Behavioral Patterns
        if threat_profile.behavioral_patterns:
            report.append("🔍 BEHAVIORAL PATTERNS:")
            for pattern in threat_profile.behavioral_patterns:
                report.append(f"   • {pattern}")
            report.append("")
        
        # Risk Indicators
        if threat_profile.risk_indicators:
            report.append("🚨 RISK INDICATORS:")
            for risk in threat_profile.risk_indicators:
                report.append(f"   ⚠️  {risk}")
            report.append("")
        
        # Intelligence Notes
        if threat_profile.intelligence_notes:
            report.append("📋 INTELLIGENCE NOTES:")
            for note in threat_profile.intelligence_notes:
                report.append(f"   • {note}")
            report.append("")
        
        report.append("🌪️ EMF Chaos Engine - Threat Intelligence Division")
        report.append("⚡ Advanced RF Analysis & Network Intelligence")
        
        return "\n".join(report)
    
    def analyze_all_detected_threats(self, network_hunter_data: Dict) -> Dict:
        """Analyze all detected threats from Network Hunter data"""
        
        threat_profiles = {}
        
        detected_targets = network_hunter_data.get('detected_targets', {})
        
        for target_name, detections in detected_targets.items():
            for detection in detections:
                # Create unique key for each detection
                network_ssid = detection['network']['ssid']
                detection_key = f"{target_name}_{network_ssid}"
                
                # Analyze threat
                threat_profile = self.analyze_network_intelligence(network_ssid, detection)
                threat_profiles[detection_key] = threat_profile
        
        return threat_profiles

# Example usage and testing
if __name__ == "__main__":
    print("🎯 Threat Intelligence Analyzer - EMF Chaos Engine")
    print("=" * 60)
    
    analyzer = ThreatIntelligenceAnalyzer()
    
    # Simulate detection data for testing
    test_detections = {
        'detected_targets': {
            'FSD_EMS': [{
                'network': {
                    'ssid': 'FSD_EMS',
                    'rssi': -44,
                    'channel': '40',
                    'security': 'WPA2-Enterprise'
                },
                'detection_time': datetime.now().isoformat(),
                'threat_assessment': {
                    'assessment': 'MEDIUM threat at CLOSE range with MEDIUM security'
                },
                'pattern_matched': 'FSD_EMS',
                'match_type': 'exact'
            }],
            'SNEAKY': [{
                'network': {
                    'ssid': 'SneakyLinc',
                    'rssi': -49,
                    'channel': '11',
                    'security': 'WPA3'
                },
                'detection_time': datetime.now().isoformat(),
                'threat_assessment': {
                    'assessment': 'HIGH threat at CLOSE range with HIGH security'
                },
                'pattern_matched': 'SNEAKYLINC',
                'match_type': 'exact'
            }]
        }
    }
    
    # Analyze all threats
    threat_profiles = analyzer.analyze_all_detected_threats(test_detections)
    
    # Generate reports
    for detection_key, threat_profile in threat_profiles.items():
        print(f"\n{analyzer.generate_intelligence_report(threat_profile)}")
        print("\n" + "=" * 60)
    
    print(f"\n🎯 Analysis Complete - {len(threat_profiles)} threat profiles generated")
    print("⚡ EMF Chaos Engine Threat Intelligence Division - OPERATIONAL")
