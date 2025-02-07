import re
import subprocess
import os
import argparse
from pathlib import Path
from typing import Optional

# Special keys that should not be converted (in lowercase)
SPECIAL_KEYS = {key.lower() for key in {
    'Return', 'Space', 'Tab', 'Escape', 'Print', 'Delete', 'BackSpace', 
    'Left', 'Right', 'Up', 'Down', 
    *[f'F{i}' for i in range(1, 13)],  # F1-F12
    'Mod1', 'Mod4', 'Shift', 'Control', 'Ctrl', 'Alt'
}}

def get_keycode(key: str) -> Optional[str]:
    """
    Get keycode using xmodmap.
    
    Args:
        key: Key symbol to look up
        
    Returns:
        Keycode or None if not found/error
    """
    try:
        # Use xmodmap to get the keycode
        cmd = f"xmodmap -pke | grep -i ' {key} '"
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.stdout:
            # Parse each line to find exact match
            for line in result.stdout.splitlines():
                parts = line.split('=')
                if len(parts) == 2:
                    keycode = parts[0].split()[1]
                    # Check symbols for exact match
                    symbols = [s.strip() for s in parts[1].split()]
                    if key in symbols:
                        return keycode
    except Exception as e:
        print(f"Error getting keycode for key {key}: {e}")
    return None

def get_output_dir(input_dir: Path) -> Path:
    """
    Create a unique output directory.
    
    Args:
        input_dir: Path to input directory
        
    Returns:
        Path to output directory
    """
    base_name = f"{input_dir.name}.fixed"
    output_dir = input_dir.parent / base_name
    
    if not output_dir.exists():
        return output_dir
    
    counter = 1
    while True:
        new_dir = input_dir.parent / f"{base_name}_{counter}"
        if not new_dir.exists():
            return new_dir
        counter += 1

def process_config_file(input_path: Path, output_path: Path) -> None:
    """
    Process config file, converting bindsym to bindcode where needed.
    
    Args:
        input_path: Path to input file
        output_path: Path to output file
    """
    content = input_path.read_text(encoding='utf-8')

    # Find all bindsym lines with their full command
    pattern = r'(bindsym\s+[^e].*?)(?=\n|$)'
    matches = re.finditer(pattern, content)

    new_content = content
    for match in matches:
        full_line = match.group(1).strip()
        # Split into binding and command
        parts = full_line.split(None, 1)
        if len(parts) != 2:
            continue
            
        bind_word, rest = parts
        key_parts = rest.split(None, 1)
        if len(key_parts) != 2:
            continue
            
        bind_keys, command = key_parts
        key_combinations = bind_keys.split('+')
        new_parts = []
        needs_conversion = False
        
        # Process each part of the key combination
        for part in parts:
            part = part.strip()
            # Check if this part is a special key or variable
            is_special = any(
                special.lower() == part.lower() or 
                part.startswith('$') 
                for special in SPECIAL_KEYS
            )
            
            if not is_special and len(part) == 1:
                if keycode := get_keycode(part):
                    new_parts.append(keycode)
                    needs_conversion = True
                else:
                    new_parts.append(part)
            else:
                new_parts.append(part)
        
        if needs_conversion:
            old_bind = full_line
            new_bind = f"bindcode {'+'.join(new_parts)} {command}"
            new_content = new_content.replace(old_bind, new_bind)

    # Create parent directories if they don't exist
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(new_content, encoding='utf-8')

def main():
    parser = argparse.ArgumentParser(
        description='Convert bindsym to bindcode in Sway config files'
    )
    parser.add_argument(
        'input_dir',
        type=str,
        help='Path to directory with config files'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Print detailed progress information'
    )
    
    args = parser.parse_args()
    input_dir = Path(args.input_dir)
    
    if not input_dir.is_dir():
        print(f"Error: {input_dir} is not a directory")
        return
    
    output_dir = get_output_dir(input_dir)
    if args.verbose:
        print(f"Creating output directory: {output_dir}")
    
    # Process all files in directory
    for input_path in input_dir.iterdir():
        if input_path.is_file():
            output_path = output_dir / input_path.name
            if args.verbose:
                print(f"Processing file: {input_path} -> {output_path}")
            process_config_file(input_path, output_path)
    
    print(f"Done! Processed files are in: {output_dir}")

if __name__ == '__main__':
    main()
