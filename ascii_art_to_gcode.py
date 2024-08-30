# read each line of the ascii art file and convert it to gcode
def ascii_to_gcode(ascii_art_file):
    with open(ascii_art_file, 'r') as f:
        ascii_art = f.readlines()
    gcode = """;simage:0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
"""
    for i, line in enumerate(ascii_art):
        gcode += f"M10086 ;{line}"
    return gcode

# save the gcode to a file
def save_gcode(gcode, gcode_file):
    with open(gcode_file, 'w') as f:
        f.write(gcode)
        
# convert the ascii art to gcode
ascii_art_file = 'ascii_art.txt'
gcode_file = 'ascii_art.gcode'

gcode = ascii_to_gcode(ascii_art_file)
save_gcode(gcode, gcode_file)