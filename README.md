Text based pong game controlled by an arduino with attached potentiometers an push-buttons

The arduino is connected to the computer using an USB cable (Serial interface). Commands from the potentiometers and pushbuttons are sent to the computer using the Pong protocol

The Pong protocol consists of:
<player>'¤'<action>'¤'<argument>'\n'
<player> might be '0' or '1'
<action> might be 'padl' or 'fire'
<argument> in case of <action>='padl' - a digit 0-1023
<argument> in case of <action>='fire' - 'up' or 'dn'
 
