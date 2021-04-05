from src.system import GameBoy

def run():
    system = GameBoy()
    
# Load optional BIOS data
with open("../roms/test_bios.bin", 'rb') as bios:
    bios_data = bytearray(bios.read())
    system.ConfigureBIOS(bios_data)

# Create the system
system.SetGameRomFromFile("../roms/test_rom.gb")
system.Run()
#end main

if __name__ == "__main__":
    run()