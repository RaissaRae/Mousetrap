# Mousetrap

First year semster one, we had to create an automated mouse trap system built using an Orange Pi, featuring distance sensing, automated door closure, alarm system, and LCD display monitoring. Here is the [youtube video](https://youtu.be/rfWOx5mEeh0).

### Features
- Automated door closure using stepper motor
- Ultrasonic distance measurement for detection
- LCD display showing system status and catch count
- Alarm light system with relay control
- Manual control via button
- uBeac integration for IoT monitoring
- Real-time status updates

### Hardware components
- Automated door closure using stepper motor
- Ultrasonic distance measurement for detection
- LCD display showing system status and catch count
- Alarm light system with relay control
- Manual control via button
- uBeac integration for IoT monitoring
- Real-time status updates

### Dependencies

- wiringpi
- spidev
- requests
- json
- time
- datetime

### Usage

1. The system starts in "Armed" mode
2. When a mouse is detected (distance < 10cm) or button is pressed:
   - Door automatically closes using stepper motor
   - Alarm light activates
   - LCD updates status to "Triggered"
   - Catch count increases
3. System can be reset using the button after 3 alarm cycles
