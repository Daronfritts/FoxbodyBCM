## Wiper / Multifunction Switch Research

Status: Research

Goal:
Replace the factory Foxbody multifunction switch with a newer Ford switch that provides:
- Mist
- Variable intermittent
- Low
- High
- Washer
- Comfortable ergonomics
- Good aftermarket availability
- Easy mechanical adaptation to Fox steering column
- Simple electrical interface to BCM

Research candidate switches:
- 1998–2011 Ford Ranger
- 1999–2004 Ford Mustang
- 1998–2011 Ford Crown Victoria
- 2004–2008 Ford F-150f

## Fuel Management System

Status: Deferred

Future Features

Fuel Menu
- Tank Filled
- Half Tank Added
- Quarter Tank Added
- Custom Gallons
- Cancel

Future Ideas
- Fuel cost tracking
- Cost per mile
- Average MPG
- Instant MPG
- Distance to Empty
- Fuel used
- Lifetime fuel usage
- Trip fuel usage
- Fill-up history
- Fuel log
- Automatic fill-up detection
- GPS gas station detection (future)

## BCM Backup Power / Emergency Access

Status: Research

Topics:
- Dedicated BCM backup battery
- LiFePO₄ vs AGM
- Automatic charging and isolation
- Emergency door unlock with dead main battery
- Hidden emergency switch
- Hidden jump terminals
- Supercapacitor option
- Battery monitoring and health reporting


# Foxbody BCM - Sensor List
Version: 1.0
Status: Planning

---

# Required Sensors (Version 1)

These sensors are required for the initial BCM release.

| Sensor | Purpose | Recommended Type | Notes |
|---------|---------|------------------|------|
| Cabin Temperature | Hot car protection | DS18B20 Digital | Hidden near headliner/rearview mirror |
| Ambient Temperature | Outside temperature display | DS18B20 Digital | Front grille/core support |
| Ambient Light | Auto lighting | BH1750 I²C | Dash or windshield |
| Rain Sensor | Auto windows / future auto wipers | Automotive Optical Rain Sensor | Windshield mounted |
| Hood Switch | Security / diagnostics | Plunger Microswitch | Hidden under hood |
| Driver Door Switch | Interior lights / security | Factory Switch | Existing |
| Passenger Door Switch | Interior lights / security | Factory Switch | Existing |
| Hatch Switch | Interior lights / security | Factory Switch | Existing |
| Brake Switch | Push button start / cruise | Factory Switch | Existing |
| Clutch Switch | Push button start | Factory Switch | Existing |
| Parking Brake Switch | Warning / service mode | Factory Switch | Existing |
| Reverse Signal | Reverse detection | Factory Signal | Existing |
| Ignition Sense | BCM power state | 12V Input Circuit | Existing |
| Battery Voltage | Charging system monitoring | Voltage Divider + ADC | Continuous monitoring |
| Fuel Level | Fuel gauge & logging | Factory Sender | Existing |

---

# Recommended Sensors

These greatly improve diagnostics and reliability.

| Sensor | Purpose | Recommended Type |
|---------|---------|------------------|
| Oil Pressure | Engine protection | 0-150 PSI Pressure Transducer |
| Fuel Pressure | Diagnostics | 0-100 PSI Pressure Transducer |
| Cabin Humidity | Comfort / Defrost | SHT31 Digital |
| Battery Current | Charging diagnostics | Hall Effect Current Sensor |
| Driver Window Current | Auto stop / Pinch detection | Hall Effect Current Sensor |
| Passenger Window Current | Auto stop / Pinch detection | Hall Effect Current Sensor |
| Cooling Fan Current | Detect failed fan | Hall Effect Current Sensor |

---

# Data Supplied by MicroSquirt

These do NOT require additional sensors.

- RPM
- MAP
- TPS
- AFR
- Intake Air Temperature
- Coolant Temperature
- Battery Voltage
- Injector Pulse Width
- Injector Duty Cycle
- Ignition Advance
- Engine Runtime
- Any future ECU channels

---

# Future Expansion Sensors

Not required for Version 1.

- GPS Receiver
- Tire Pressure Monitoring (TPMS)
- Accelerometer
- Gyroscope
- Compass
- Cabin Air Quality Sensor
- Carbon Monoxide Sensor
- Smoke Detector
- Ride Height Sensors
- Air Suspension Pressure Sensors
- Front Camera
- Rear Camera
- Ultrasonic Parking Sensors

---

# Factory Inputs Used

Existing vehicle switches reused by BCM.

- Driver Door
- Passenger Door
- Hatch
- Brake Pedal
- Clutch Pedal
- Parking Brake
- Reverse Lights
- Ignition
- Fuel Sender

---

# BCM Calculated Values

No sensor required.

- Trip Distance
- Fuel Economy
- Distance To Empty
- Average Speed
- Maximum Speed
- Maximum RPM
- Maximum Coolant Temperature
- Average Battery Voltage
- Trip Time
- Maintenance Intervals
- Battery Health
- Window Position
- Door Lock Status
- Fan Runtime
- Engine Runtime
- Cabin Heat Soak
- Event History

---

# Future Research

- Current sensing for all motors
- Window pinch protection
- Dual cabin temperature sensors
- Backup battery monitoring
- Emergency power system
- TPMS integration
- Dashcam integration
- OBD-II compatibility (future expansion)

---

# Estimated Sensor Count

Factory Sensors Used:
- 9

New Sensors:
- 10-12

MicroSquirt Data Channels:
- 10+

Approximate Physical Sensors Installed:
20-25
