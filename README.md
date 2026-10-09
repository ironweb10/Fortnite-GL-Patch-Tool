# Fortnite GL Autopatch v2.0

This is a one-click fix for Fortnite UE4 4.19 (Android arm64) on GPUs using OpenGL ES over ANGLE (such as the Samsung Xclipse / Galaxy A57)[cite: 1]. The tool uses only the standard Python 3.8+ library, meaning no pip, no Java, and no additional downloads are needed[cite: 1]. 

## What It Fixes

* **libUE4.so**: Applies 28 patches based on code signatures to bypass fatal errors when ANGLE cannot link or create GL programs[cite: 1]. It protects pointer reads using code caves in free padding and a writable zero-page, and works with versions 5.41 and 6.01[cite: 1].
* **classes.dex**: Fixes issues in stripped "base" APKs where missing classes cause a `NoClassDefFoundError` upon launch[cite: 1]. It does this by making `DownloadConfigRules()` return true instantly when `GameActivity$RequestConfigRulesFileTask` is missing[cite: 1].
* **UE4CommandLine.txt**: Injects `-ExecCmds="r.ProgramBinaryCache.Enable 0"` into the command line[cite: 1]. It also injects `-nomcp` if no `-AUTH_` flags are detected[cite: 1].
* **Signing**: Includes a custom Android v2 signature scheme written entirely in Python[cite: 1]. The script generates a key on its first run and stores it in the "tools" folder[cite: 1]. This key is reused for future runs, allowing you to update the APK without uninstalling it first[cite: 1].

## How to Use

1. Place the original `.apk` in the SAME folder as this script[cite: 1].
2. Run the command: `python fortnite_gl_autopatch.py`[cite: 1].
3. Type the name of the APK, or simply press Enter if there is only one APK in the directory[cite: 1]. The script will process the file and output `<name>_fixed.apk` which is already patched, aligned, and signed[cite: 1].
4. Uninstall the original Fortnite app, as the new signature will not match the original[cite: 1].
5. Install the generated `_fixed.apk`[cite: 1].

## Advanced Usage

You can bypass the interactive prompts by passing the file name directly:
* `python fortnite_gl_autopatch.py game.apk` (automatically patches the specified APK)[cite: 1].
* `python fortnite_gl_autopatch.py libUE4.so` (patches only the library file instead of a full APK)[cite: 1].

**Available command-line options:**[cite: 1]
* `--dry-run`[cite: 1]
* `--no-sign`[cite: 1]
* `--out PATH`[cite: 1]
* `--nomcp` or `--no-nomcp`[cite: 1]
* `--no-execcmds`[cite: 1]
* `--no-dex-fix`[cite: 1]
* `--zp extend|gap`[cite: 1]
* `--require-all`[cite: 1]
* `--signer builtin|uber`[cite: 1]
* `--install`[cite: 1]
* `--force`[cite: 1]
* `--verify APK`[cite: 1]
