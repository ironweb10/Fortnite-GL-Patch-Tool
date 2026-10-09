# Fortnite GL Patch Tool

This is a one-click fix for Fortnite UE4 4.19 (Android arm64) on GPUs using OpenGL ES over ANGLE (such as the Samsung Xclipse / Galaxy A57). The tool uses only the standard Python 3.8+ library, meaning no pip, no Java, and no additional downloads are needed. 

## What It Fixes

* **libUE4.so**: Applies 28 patches based on code signatures to bypass fatal errors when ANGLE cannot link or create GL programs. It protects pointer reads using code caves in free padding and a writable zero-page, and works with versions 5.41 and 6.01.
* **classes.dex**: Fixes issues in stripped "base" APKs where missing classes cause a `NoClassDefFoundError` upon launch. It does this by making `DownloadConfigRules()` return true instantly when `GameActivity$RequestConfigRulesFileTask` is missing.
* **UE4CommandLine.txt**: Injects `-ExecCmds="r.ProgramBinaryCache.Enable 0"` into the command line. It also injects `-nomcp` if no `-AUTH_` flags are detected.
* **Signing**: Includes a custom Android v2 signature scheme written entirely in Python. The script generates a key on its first run and stores it in the "tools" folder. This key is reused for future runs, allowing you to update the APK without uninstalling it first.

## How to Use

1. Place the original `.apk` in the SAME folder as this script.
2. Run the command: `python fortnite_gl_autopatch.py`.
3. Type the name of the APK, or simply press Enter if there is only one APK in the directory. The script will process the file and output `<name>_fixed.apk` which is already patched, aligned, and signed.
4. Uninstall the original Fortnite app, as the new signature will not match the original.
5. Install the generated `_fixed.apk`.

## Advanced Usage

You can bypass the interactive prompts by passing the file name directly:
* `python fortnite_gl_autopatch.py game.apk` (automatically patches the specified APK).
* `python fortnite_gl_autopatch.py libUE4.so` (patches only the library file instead of a full APK).

**Available command-line options:**
* `--dry-run`
* `--no-sign`
* `--out PATH`
* `--nomcp` or `--no-nomcp`
* `--no-execcmds`
* `--no-dex-fix`
* `--zp extend|gap`
* `--require-all`
* `--signer builtin|uber`
* `--install`
* `--force`
* `--verify APK`

## 🤝 Contributing & Anti-Plagiarism Policy

**Pull Requests are highly encouraged!** 
If you want to help improve this code, optimize the patching process, or fix bugs, please feel free to fork the repository and submit a Pull Request. Your contributions to the community are greatly appreciated.

🚫 **ZERO TOLERANCE FOR CODE THEFT** 🚫
You are strictly prohibited from taking this code, slightly modifying it (or not modifying it at all), and re-uploading it as your own original creation. 

* **Do not steal this script.**
* **Do not claim this work as yours.**
* If you use parts of this script in your own public project, you **must** provide clear, visible credit to this original repository. 

### License
This project is provided for educational and preservation purposes. While you are free to use it to fix your own legally obtained games and submit improvements back to this repository, the underlying code remains the intellectual property of its original author. Copying and rebranding this tool without permission is strictly forbidden.
