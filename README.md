Text based pong game controlled by an arduino with attached potentiometers an push-buttons

The arduino is connected to the computer using an USB cable (Serial interface). Commands from the potentiometers and pushbuttons are sent to the computer using the Pong protocol

The Pong protocol consists of:
&lt;player&gt;'¤'&lt;action&gt;'¤'&lt;argument&gt;'\n'
&lt;player&gt; might be '0' or '1'
&lt;action&gt; might be 'padl' or 'fire'
&lt;argument&gt; in case of &lt;action&gt;='padl' - a digit 0-1023
&lt;argument&gt; in case of &lt;action&gt;='fire' - 'up' or 'dn'
 
