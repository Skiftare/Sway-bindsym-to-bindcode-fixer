# Sway-bindsym-to-bindcode-fixer
This script will help you convert all bindsym references to bindcode in Sway so that keyboard shortcuts work correctly, regardless of the active language.

Overview

This script automates the conversion of bindsym keybindings to bindcode keybindings in Sway configuration files. This is particularly useful when dealing with issues where keybindings do not work properly with non-Latin keyboard layouts.

Features

Converts bindsym to bindcode where applicable.

Preserves special keys (e.g., Return, Space, Shift, Ctrl) without conversion.

Supports verbose mode for detailed output.

Automatically creates a unique output directory to prevent overwriting original files.

Requirements

Python 3.x

Linux environment with xmodmap installed

Usage

Command-Line Arguments

python script.py <input_dir> [--verbose | -v]

Arguments:

input_dir (required): Path to the directory containing Sway configuration files.

--verbose or -v (optional): Enables detailed progress information.

Example

python script.py /home/user/.config/sway/config.d/ -v

This command will process all files in the specified directory and output the modified files into a new directory, e.g., config.d.fixed.

How It Works

Identify Bindings:

Searches for lines starting with bindsym (excluding those starting with binde).

Key Parsing:

Splits keybindings into individual parts (e.g., Ctrl+Alt+T becomes Ctrl, Alt, T).

Keycode Conversion:

Converts single-character keys to keycodes using xmodmap.

Leaves special keys (like Shift, Ctrl, function keys) unchanged.

Output Directory:

Creates a new directory with the suffix .fixed to store converted files.

File Writing:

Writes modified content to new files, maintaining the original directory structure.


Parameters:

input_path - Path to the input config file.

output_path - Path where the modified file will be saved.

main()

Handles argument parsing, directory traversal, and file processing.

Error Handling

If xmodmap encounters an error or the keycode cannot be retrieved, the script logs the issue and skips that key.

Ensures the output directory is created even if it doesn't exist.

Known Limitations

Requires xmodmap, which may not be available in all environments.

May not correctly handle complex keybinding cases with advanced modifiers or nested commands.

License

This script is provided "as-is" without any warranty. Use at your own risk.

