import argparse, sys, logging

from src.system import GameBoy

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')
#end

def _create_arg_parser():
    parser = argparse.ArgumentParser(prog="Yoji", description="A Python GameBoy Emulator that's still in its infancy")
    parser.add_argument("rom_file", help="The ROM file to load and run")
    parser.add_argument("--bios-image", "--bios", required=False, help="A compatible GameBoy BIOS to boot the system")
    parser.add_argument("-v", "--verbose", help="increase output verbosity", action="store_true")
    parser.add_argument('--debug', nargs='?', type=str2bool, default=False, const=True, help="Enable full debugging capabilities")
    parser.add_argument('--debug-video', nargs='?', type=str2bool, default=False, const=True, help="Open window debugging")
    return parser
#end

def main():
    parser = _create_arg_parser()
    parsed_args = parser.parse_args()

    if parsed_args.verbose:
        logging.basicConfig(level=logging.DEBUG)
    
    # Load optional BIOS data
    bios_data = None
    if parsed_args.bios_image:
        with open(parsed_args.bios_image, 'rb') as bios:
            bios_data = bytearray(bios.read())

    # Create the system
    system = GameBoy()
    system.ConfigureBIOS(bios_data)
    system.SetGameRomFromFile(parsed_args.rom_file)

    if parsed_args.debug:
        logging.basicConfig(level=logging.DEBUG)
        system.Debug = True
    
    system.Run()
#end

if __name__ == "__main__":
    main()