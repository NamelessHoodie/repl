import sys
import ast
import code
from argparse import ArgumentParser

_outpath_default_ = 'repl_session.py'

class ReplRecorder(code.InteractiveConsole):
    def __init__(self, output_file = _outpath_default_, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.output_file = output_file
        self.current_block = []
        self.had_error = False

    def push(self, line):
        self.current_block.append(line)
        more_needed = super().push(line)
        
        if not more_needed:
            code_str = '\n'.join(self.current_block)
            try:
                processed_code = self._process_code(code_str)
                has_quit = any(line.strip().lower() in ('quit()', 'exit()') 
                             for line in self.current_block)

                if not has_quit:
                    if self.had_error:
                        processed_code = f'# {processed_code}'
                    self.output_file.write(processed_code + '\n')
                    self.output_file.flush()
            except SyntaxError:
                # Fallback for invalid syntax
                self.output_file.write(code_str + '\n')
            
            self.current_block = []
            self.had_error = False
            
        return more_needed

    def _process_code(self, code_str):
        try:
            # Parse the entire code block
            tree = ast.parse(code_str)
            modified_statements = []
            
            for node in tree.body:
                # Handle each statement individually
                if isinstance(node, ast.Expr):
                    # Wrap expressions in print(repr(...))
                    modified_statements.append(
                        f'print(repr({ast.unparse(node)}))'
                    )
                else:
                    # Keep other statements as-is
                    modified_statements.append(ast.unparse(node))
            
            return '; '.join(modified_statements)
        except SyntaxError:
            # If parsing fails, return the original code
            return code_str

    def showsyntaxerror(self, filename=None):
        self.had_error = True
        super().showsyntaxerror(filename)

    def showtraceback(self):
        self.had_error = True
        super().showtraceback()

def interact(output_file_name=_outpath_default_):
    try:
        with open(output_file_name, 'w') as output_file:
            print(f"Starting REPL session. Output will be saved to '{output_file_name}'")
            recorder = ReplRecorder(output_file)
            recorder.interact()
    except KeyboardInterrupt:
        print("\nREPL session interrupted. Exiting.")
    finally:
        print(f"REPL session saved to {output_file_name}")
    
def main():
    parser = ArgumentParser(description="Python REPL wrapper to save inputs to a .py file.")
    parser.add_argument('output', nargs='?', default=_outpath_default_,
                      help=f"Output filename (default: {_outpath_default_})")
    parser.add_argument('-o', '--output', dest='output_flag', type=str,
                      help="Output filename (alternative)")
    args = parser.parse_args()

    output_file_name = args.output_flag or args.output

    interact(args.output_flag or args.output)

if __name__ == '__main__':
    main()
