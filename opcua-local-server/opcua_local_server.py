import asyncio
import logging
import random
import time
from datetime import datetime
from typing import Dict, Any

from opcua import Server, ua
from opcua.common.node import Node


class IndustrialControlSystem:
    """Mock Industrial Control System with sensors, actuators, and control methods."""
    
    def __init__(self, server: Server):
        self.server = server
        self.running = False
        
        # System state
        self.system_state = {
            # Sensor readings
            'temperature': 25.0,
            'pressure': 1013.25,
            'flow_rate': 150.0,
            'tank_level': 75.0,
            'vibration': 0.5,
            'ph_level': 7.2,
            'humidity': 45.0,
            'motor_speed': 1500.0,
            
            # Actuator states
            'pump_enabled': False,
            'valve_position': 50.0,
            'heater_power': 0.0,
            'fan_speed': 0.0,
            'conveyor_speed': 0.0,
            'alarm_active': False,
            
            # System status
            'system_mode': 'MANUAL',  # MANUAL, AUTO, MAINTENANCE
            'emergency_stop': False,
            'production_rate': 0.0,
            'total_production': 0.0,
        }
        
        # Node references for efficient updates
        self.nodes = {}
        
    def setup_address_space(self):
        """Setup the OPC UA address space with industrial control structure."""
        
        # Get the root object node
        objects = self.server.get_objects_node()
        
        # Create main industrial system folder
        industrial_system = objects.add_folder(2, "IndustrialControlSystem")
        
        # Create sensor folder and variables
        sensors_folder = industrial_system.add_folder(2, "Sensors")
        self._create_sensor_variables(sensors_folder)
        
        # Create actuator folder and variables
        actuators_folder = industrial_system.add_folder(2, "Actuators")
        self._create_actuator_variables(actuators_folder)
        
        # Create system status folder
        system_folder = industrial_system.add_folder(2, "SystemStatus")
        self._create_system_variables(system_folder)
        
        # Create methods folder and add control methods
        methods_folder = industrial_system.add_folder(2, "Methods")
        self._create_control_methods(methods_folder)
        
        logging.info("Address space setup completed")
    
    def _create_sensor_variables(self, parent_folder: Node):
        """Create sensor variables with proper data types and descriptions."""
        
        # Temperature sensor
        temp_node = parent_folder.add_variable(2, "Temperature", self.system_state['temperature'])
        temp_node.set_writable(False)
        self.nodes['temperature'] = temp_node
        
        # Pressure sensor
        pressure_node = parent_folder.add_variable(2, "Pressure", self.system_state['pressure'])
        pressure_node.set_writable(False)
        self.nodes['pressure'] = pressure_node
        
        # Flow rate sensor
        flow_node = parent_folder.add_variable(2, "FlowRate", self.system_state['flow_rate'])
        flow_node.set_writable(False)
        self.nodes['flow_rate'] = flow_node
        
        # Tank level sensor
        level_node = parent_folder.add_variable(2, "TankLevel", self.system_state['tank_level'])
        level_node.set_writable(False)
        self.nodes['tank_level'] = level_node
        
        # Vibration sensor
        vibration_node = parent_folder.add_variable(2, "Vibration", self.system_state['vibration'])
        vibration_node.set_writable(False)
        self.nodes['vibration'] = vibration_node
        
        # pH sensor
        ph_node = parent_folder.add_variable(2, "PhLevel", self.system_state['ph_level'])
        ph_node.set_writable(False)
        self.nodes['ph_level'] = ph_node
        
        # Humidity sensor
        humidity_node = parent_folder.add_variable(2, "Humidity", self.system_state['humidity'])
        humidity_node.set_writable(False)
        self.nodes['humidity'] = humidity_node
        
        # Motor speed sensor
        motor_speed_node = parent_folder.add_variable(2, "MotorSpeed", self.system_state['motor_speed'])
        motor_speed_node.set_writable(False)
        self.nodes['motor_speed'] = motor_speed_node
    
    def _create_actuator_variables(self, parent_folder: Node):
        """Create actuator variables that can be controlled."""
        
        # Pump control
        pump_node = parent_folder.add_variable(2, "PumpEnabled", self.system_state['pump_enabled'])
        pump_node.set_writable(True)
        self.nodes['pump_enabled'] = pump_node
        
        # Valve position control
        valve_node = parent_folder.add_variable(2, "ValvePosition", self.system_state['valve_position'])
        valve_node.set_writable(True)
        self.nodes['valve_position'] = valve_node
        
        # Heater power control
        heater_node = parent_folder.add_variable(2, "HeaterPower", self.system_state['heater_power'])
        heater_node.set_writable(True)
        self.nodes['heater_power'] = heater_node
        
        # Fan speed control
        fan_node = parent_folder.add_variable(2, "FanSpeed", self.system_state['fan_speed'])
        fan_node.set_writable(True)
        self.nodes['fan_speed'] = fan_node
        
        # Conveyor speed control
        conveyor_node = parent_folder.add_variable(2, "ConveyorSpeed", self.system_state['conveyor_speed'])
        conveyor_node.set_writable(True)
        self.nodes['conveyor_speed'] = conveyor_node
        
        # Alarm control
        alarm_node = parent_folder.add_variable(2, "AlarmActive", self.system_state['alarm_active'])
        alarm_node.set_writable(True)
        self.nodes['alarm_active'] = alarm_node
    
    def _create_system_variables(self, parent_folder: Node):
        """Create system status variables."""
        
        # System mode
        mode_node = parent_folder.add_variable(2, "SystemMode", self.system_state['system_mode'])
        mode_node.set_writable(True)
        self.nodes['system_mode'] = mode_node
        
        # Emergency stop
        estop_node = parent_folder.add_variable(2, "EmergencyStop", self.system_state['emergency_stop'])
        estop_node.set_writable(True)
        self.nodes['emergency_stop'] = estop_node
        
        # Production rate
        prod_rate_node = parent_folder.add_variable(2, "ProductionRate", self.system_state['production_rate'])
        prod_rate_node.set_writable(False)
        self.nodes['production_rate'] = prod_rate_node
        
        # Total production
        total_prod_node = parent_folder.add_variable(2, "TotalProduction", self.system_state['total_production'])
        total_prod_node.set_writable(False)
        self.nodes['total_production'] = total_prod_node
        
        # Command variables for control (alternative to methods)
        start_prod_cmd = parent_folder.add_variable(2, "StartProductionCommand", 0.0)
        start_prod_cmd.set_writable(True)
        self.nodes['start_production_command'] = start_prod_cmd
        
        stop_prod_cmd = parent_folder.add_variable(2, "StopProductionCommand", False)
        stop_prod_cmd.set_writable(True)
        self.nodes['stop_production_command'] = stop_prod_cmd
        
        emergency_cmd = parent_folder.add_variable(2, "EmergencyStopCommand", False)
        emergency_cmd.set_writable(True)
        self.nodes['emergency_stop_command'] = emergency_cmd
        
        reset_cmd = parent_folder.add_variable(2, "ResetSystemCommand", False)
        reset_cmd.set_writable(True)
        self.nodes['reset_system_command'] = reset_cmd
    
    def _create_control_methods(self, parent_folder: Node):
        """Create OPC UA methods for system control."""
        
        # Start production method
        start_method = parent_folder.add_method(
            2, "StartProduction", self.start_production_callback
        )
        
        # Stop production method
        stop_method = parent_folder.add_method(
            2, "StopProduction", self.stop_production_callback
        )
        
        # Emergency stop method
        emergency_method = parent_folder.add_method(
            2, "EmergencyStop", self.emergency_stop_callback
        )
        
        # Reset system method
        reset_method = parent_folder.add_method(
            2, "ResetSystem", self.reset_system_callback
        )
        
        # Calibrate sensors method
        calibrate_method = parent_folder.add_method(
            2, "CalibrateSensors", self.calibrate_sensors_callback
        )
    
    # Method callbacks
    def start_production_callback(self, parent, *args):
        """Start production with specified rate."""
        rate = float(args[0]) if args else 10.0
        logging.info(f"Starting production with rate: {rate}")
        self.system_state['production_rate'] = rate
        self.system_state['system_mode'] = 'AUTO'
        self.system_state['pump_enabled'] = True
        self.system_state['conveyor_speed'] = min(rate * 2, 100.0)  # Scale speed with rate
        return True
    
    def stop_production_callback(self, parent, *args):
        """Stop production."""
        logging.info("Stopping production")
        self.system_state['production_rate'] = 0.0
        self.system_state['system_mode'] = 'MANUAL'
        self.system_state['pump_enabled'] = False
        self.system_state['conveyor_speed'] = 0.0
        return True
    
    def emergency_stop_callback(self, parent, *args):
        """Trigger emergency stop."""
        logging.warning("EMERGENCY STOP TRIGGERED!")
        self.system_state['emergency_stop'] = True
        self.system_state['system_mode'] = 'MAINTENANCE'
        self.system_state['production_rate'] = 0.0
        self.system_state['pump_enabled'] = False
        self.system_state['conveyor_speed'] = 0.0
        self.system_state['heater_power'] = 0.0
        self.system_state['fan_speed'] = 0.0
        self.system_state['alarm_active'] = True
        return True
    
    def reset_system_callback(self, parent, *args):
        """Reset system to initial state."""
        logging.info("Resetting system")
        self.system_state['emergency_stop'] = False
        self.system_state['system_mode'] = 'MANUAL'
        self.system_state['alarm_active'] = False
        self.system_state['total_production'] = 0.0
        return True
    
    def calibrate_sensors_callback(self, parent, *args):
        """Calibrate specified sensor."""
        sensor_name = str(args[0]) if args else "unknown"
        logging.info(f"Calibrating sensor: {sensor_name}")
        # Simulate calibration by adding small random offset
        if sensor_name in self.system_state:
            # Add some calibration effect
            pass
        return True
    
    def simulate_process(self):
        """Simulate industrial process behavior."""
        while self.running:
            try:
                # Process command variables first
                self._process_commands()
                
                # Update sensor readings based on system state
                self._update_sensors()
                
                # Update actuator effects
                self._process_actuator_effects()
                
                # Update production metrics
                self._update_production()
                
                # Update all OPC UA nodes
                self._update_opcua_nodes()
                
                time.sleep(1.0)  # Update every second
                
            except Exception as e:
                logging.error(f"Error in process simulation: {e}")
                time.sleep(1.0)
    
    def _process_commands(self):
        """Process command variables and execute corresponding actions."""
        try:
            # Check start production command
            start_cmd = self.nodes['start_production_command'].get_value()
            if start_cmd > 0:
                rate = float(start_cmd)
                logging.info(f"Starting production with rate: {rate}")
                self.system_state['production_rate'] = rate
                self.system_state['system_mode'] = 'AUTO'
                self.system_state['pump_enabled'] = True
                self.system_state['conveyor_speed'] = min(rate * 2, 100.0)
                # Reset command
                self.nodes['start_production_command'].set_value(0.0)
            
            # Check stop production command
            stop_cmd = self.nodes['stop_production_command'].get_value()
            if stop_cmd:
                logging.info("Stopping production")
                self.system_state['production_rate'] = 0.0
                self.system_state['system_mode'] = 'MANUAL'
                self.system_state['pump_enabled'] = False
                self.system_state['conveyor_speed'] = 0.0
                # Reset command
                self.nodes['stop_production_command'].set_value(False)
            
            # Check emergency stop command
            emergency_cmd = self.nodes['emergency_stop_command'].get_value()
            if emergency_cmd:
                logging.warning("EMERGENCY STOP TRIGGERED!")
                self.system_state['emergency_stop'] = True
                self.system_state['system_mode'] = 'MAINTENANCE'
                self.system_state['production_rate'] = 0.0
                self.system_state['pump_enabled'] = False
                self.system_state['conveyor_speed'] = 0.0
                self.system_state['heater_power'] = 0.0
                self.system_state['fan_speed'] = 0.0
                self.system_state['alarm_active'] = True
                # Reset command
                self.nodes['emergency_stop_command'].set_value(False)
            
            # Check reset system command
            reset_cmd = self.nodes['reset_system_command'].get_value()
            if reset_cmd:
                logging.info("Resetting system")
                self.system_state['emergency_stop'] = False
                self.system_state['system_mode'] = 'MANUAL'
                self.system_state['alarm_active'] = False
                self.system_state['total_production'] = 0.0
                # Reset command
                self.nodes['reset_system_command'].set_value(False)
                
        except Exception as e:
            logging.error(f"Error processing commands: {e}")
    
    def _update_sensors(self):
        """Update sensor readings with realistic variations."""
        
        # Temperature influenced by heater
        base_temp = 25.0 + (self.system_state['heater_power'] * 0.5)
        self.system_state['temperature'] = base_temp + random.uniform(-2.0, 2.0)
        
        # Pressure influenced by pump and valve
        base_pressure = 1013.25
        if self.system_state['pump_enabled']:
            base_pressure += 50.0
        base_pressure -= (self.system_state['valve_position'] - 50.0) * 0.5
        self.system_state['pressure'] = base_pressure + random.uniform(-5.0, 5.0)
        
        # Flow rate influenced by pump and valve
        if self.system_state['pump_enabled']:
            base_flow = 150.0 * (self.system_state['valve_position'] / 100.0)
        else:
            base_flow = 0.0
        self.system_state['flow_rate'] = max(0, base_flow + random.uniform(-10.0, 10.0))
        
        # Tank level influenced by flow rate and production
        level_change = (self.system_state['flow_rate'] - self.system_state['production_rate']) * 0.01
        self.system_state['tank_level'] = max(0, min(100, 
            self.system_state['tank_level'] + level_change + random.uniform(-0.5, 0.5)))
        
        # Vibration influenced by motor and conveyor speed
        base_vibration = (self.system_state['motor_speed'] / 1500.0) * 0.3
        base_vibration += (self.system_state['conveyor_speed'] / 100.0) * 0.2
        self.system_state['vibration'] = base_vibration + random.uniform(-0.1, 0.1)
        
        # pH level with slow drift
        self.system_state['ph_level'] += random.uniform(-0.05, 0.05)
        self.system_state['ph_level'] = max(6.0, min(8.0, self.system_state['ph_level']))
        
        # Humidity influenced by temperature
        base_humidity = 45.0 - (self.system_state['temperature'] - 25.0) * 2.0
        self.system_state['humidity'] = max(20, min(80, base_humidity + random.uniform(-3.0, 3.0)))
        
        # Motor speed influenced by production rate
        if self.system_state['production_rate'] > 0:
            self.system_state['motor_speed'] = 1500.0 + (self.system_state['production_rate'] * 10.0) + random.uniform(-50.0, 50.0)
        else:
            self.system_state['motor_speed'] = random.uniform(-10.0, 10.0)
    
    def _process_actuator_effects(self):
        """Process effects of actuator changes."""
        
        # Check for alarm conditions
        if (self.system_state['temperature'] > 80.0 or 
            self.system_state['pressure'] > 1200.0 or
            self.system_state['tank_level'] < 10.0 or
            self.system_state['vibration'] > 2.0):
            self.system_state['alarm_active'] = True
            
        # Auto-safety: stop system if emergency conditions
        if (self.system_state['temperature'] > 100.0 or 
            self.system_state['pressure'] > 1300.0):
            self.system_state['emergency_stop'] = True
            self.system_state['system_mode'] = 'MAINTENANCE'
    
    def _update_production(self):
        """Update production metrics."""
        if (self.system_state['system_mode'] == 'AUTO' and 
            not self.system_state['emergency_stop'] and
            self.system_state['production_rate'] > 0):
            # Add to total production (rate is per hour, we update per second)
            self.system_state['total_production'] += self.system_state['production_rate'] / 3600.0
    
    def _update_opcua_nodes(self):
        """Update all OPC UA node values."""
        for key, node in self.nodes.items():
            if key in self.system_state:
                try:
                    node.set_value(self.system_state[key])
                except Exception as e:
                    logging.error(f"Error updating node {key}: {e}")
    
    def start_simulation(self):
        """Start the process simulation."""
        self.running = True
        
    def stop_simulation(self):
        """Stop the process simulation."""
        self.running = False


def main():
    """Main function to run the OPC UA server."""
    
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Create and configure the server
    server = Server()
    
    # Set server endpoint
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")
    
    # Set server name and namespace
    server.set_server_name("Industrial Control System OPC UA Server")
    
    # Setup security policy (optional)
    server.set_security_policy([
        ua.SecurityPolicyType.NoSecurity,
        ua.SecurityPolicyType.Basic256Sha256_SignAndEncrypt,
        ua.SecurityPolicyType.Basic256Sha256_Sign
    ])
    
    # Create the industrial control system
    industrial_system = IndustrialControlSystem(server)
    
    try:
        # Setup the address space
        industrial_system.setup_address_space()
        
        # Start the server
        server.start()
        logging.info("OPC UA Server started at opc.tcp://0.0.0.0:4840/freeopcua/server/")
        logging.info("Server is running and ready for connections")
        
        # Start process simulation in a separate thread
        industrial_system.start_simulation()
        
        import threading
        simulation_thread = threading.Thread(target=industrial_system.simulate_process)
        simulation_thread.daemon = True
        simulation_thread.start()
        
        try:
            # Keep the server running
            logging.info("Server running. Press Ctrl+C to stop...")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logging.info("Shutting down server...")
            industrial_system.stop_simulation()
            
    except Exception as e:
        logging.error(f"Server error: {e}")
        raise
    finally:
        try:
            if server is not None:
                server.stop()
        except Exception as e:
            logging.error(f"Error stopping server: {e}")


if __name__ == "__main__":
    main()
