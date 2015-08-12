# veri_ports
Verilog editing automation (mostly creating instantiation templates, lists of ports, etc.)

How to use it:
Copy module instantiation Verilog code or port declaration code to the text window. Now you can convert them between each other with "inst. -> ports" and "ports -> inst." buttons.

The program recognizes Xilinx IP-cores instantiation templates where a comment is added in each line of .veo files, containing the port's type, direction and width. Like this:

.xgmii_rxc(xgmii_rxc),		//input wire [3:0] xgmii_rxc

In case of such comment present the generated port declaration will be of corresponding type, width and direction. The program will generate such comments for instantiation templates too.

You can clear the text windows with "Clear" button and copy it's content to the clipboard with "Copy".


All following buttons can work with single line (the one with the blinking cursor in the text window) or with a selection (if you select some text in the text window).


"revert" reverses port/ports direction. Doesn't affect inout ports.
"make local" deletes any input/output/inout text from line/selection.

"wire" changes port type to wire.
"reg" changes port type to reg.

"bus" makes a port a bus or changes bus width. You should at first write the desired width in the small text windows to the right of the button (1 bit is a valid width - produces [0:0]), then move the pointer to the desired line or select multiple lines and press the "bus" button.

"single" deletes any bus width declarations from line/lines.
