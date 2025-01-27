import subprocess
import re
from argparse import ArgumentParser

def process_repl_session(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w') as outfile:
        lines = infile.readlines()
        in_repl = False
        last_input = None
        for line in lines:
            # Detect the start of the REPL session
            if not in_repl and re.match(r'>>> ', line):
                in_repl = True

            # Process REPL inputs
            if in_repl:
                if line.startswith('>>> '):
                    # Extract the input
                    last_input = line[4:].strip()
                    # Skip quit() or exit() commands
                    if not (last_input == 'quit()' or last_input == 'exit()'):
                        outfile.write(last_input + '\n')
                elif line.startswith('... '):
                    # Handle multi-line inputs
                    last_input = line[4:].strip()
                    # Skip quit() or exit() commands
                    if not (last_input == 'quit()' or last_input == 'exit()'):
                        outfile.write(last_input + '\n')
                elif line.startswith('Traceback (most recent call last):'):
                    # Comment out the last input line if it caused an error
                    outfile.seek(outfile.tell() - len(last_input) - 1)  # Move cursor back
                    outfile.write('# ' + last_input + '\n')  # Comment out the line

def main():
    # Parse command-line arguments
    parser = ArgumentParser(description="Python REPL wrapper to save inputs to a .py file.")
    parser.add_argument('output', nargs='?', default='repl_session.py',
                        help="Output filename for the .py file (default: repl_session.py)")
    parser.add_argument('-o', '--output', dest='output_flag', type=str,
                        help="Output filename for the .py file (alternative to positional argument)")
    args = parser.parse_args()

    # Determine the output filename
    output_file = args.output_flag if args.output_flag else args.output

    # Start a script session to record the REPL
    script_file = 'repl_session.txt'
    print(f"Script started, output log file is '{script_file}'")

    # Use `script` to launch the Python REPL directly
    subprocess.run(['script', '-f', script_file, '-c', 'python3'])

    # Process the recorded session to create a .py file
    process_repl_session(script_file, output_file)

    print(f"REPL session saved to {output_file}")

if __name__ == '__main__':
    main()
