#!/usr/bin/env python3
import os
import shutil
from pathlib import Path

def prompt(prompt_text, default=None):
    if default:
        resp = input(f"{prompt_text} [{default}]: ").strip()
        return resp if resp else default
    return input(f"{prompt_text}: ").strip()

def main():
    print("Unvanquished Maps Starter")
    print("=========================\n")

    base_dir = prompt("Path to the target directory where to create the map")
    if not base_dir:
        print("Error: empty target directory path.")
        return
    base_path = Path(base_dir).resolve()
    base_path.mkdir(parents=True, exist_ok=True)

    short_name = prompt("Short name of the map (format short, without spaces, ex: my_map)").replace(" ", "_")
    if not short_name:
        print("Error: invalid short name.")
        return

    long_name = prompt("Long name of the map (format long)")
    if not long_name:
        print("Error: invalid long name.")
        return

    authors_raw = prompt("The or the authors (separated by commas)")
    authors = [a.strip() for a in authors_raw.split(",") if a.strip()]
    if not authors:
        authors = ["Unknown"]

    map_type = prompt("Type (default 'tremulous')", default="tremulous")
    if not map_type:
        map_type = "tremulous"

    map_dir = f"map-{short_name}_1.0.dpkdir"
    target_root = base_path / map_dir
    target_root.mkdir(parents=True, exist_ok=True)

    (target_root / "DEPS").write_text("tex-all\n", encoding="utf-8")

    # MAPS
    (target_root / "maps").mkdir(parents=True, exist_ok=True)
    default_map_path = os.path.join(os.path.dirname(__file__), "defaults", "default-map")
    shutil.copy(os.path.join(default_map_path, "mapname.map"), target_root / "maps" / f"{short_name}.map")
    shutil.copy(os.path.join(default_map_path, "mapname.bsp"), target_root / "maps" / f"{short_name}.bsp")
    (target_root / "maps" / short_name).mkdir(parents=True, exist_ok=True)
    shutil.copy(os.path.join(default_map_path, "mapname", "lm_0000.tga"), target_root / "maps" / short_name / "lm_0000.tga")
    shutil.copy(os.path.join(default_map_path, "mapname", "lm_0001.tga"), target_root / "maps" / short_name / "lm_0001.tga")

    # META
    meta_dir = target_root / "meta" / short_name
    arena_path = meta_dir / f"{short_name}.arena"
    meta_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(os.path.join(os.path.dirname(__file__), "defaults", "default-meta", "mapname.png"), meta_dir / f"{short_name}.png")

    # MINIMAPS
    (target_root / "minimaps").mkdir(parents=True, exist_ok=True)
    default_minimap_path = os.path.join(os.path.dirname(__file__), "defaults", "default-minimap")
    (target_root / "minimaps" / f"{short_name}.minimap").write_text(
        f"""
{{
	backgroundColor 0.0 0.0 0.0 0.333
	zone {{
		bounds 0 0 0 0 0 0
		image "minimaps/{short_name}" -1128.000000 -760.000000 360.000000 728.000000
	}}
}}""",
        encoding="utf-8"
    )
    shutil.copy(os.path.join(default_minimap_path, "mapname.tga"), target_root / "minimaps" / f"{short_name}.tga")


    # README
    (target_root / "README.MD").write_text(
        f"""# {long_name}

Welcome to your new Unvanquished map project!

## Getting Started

If you're new to mapping, check out the official Unvanquished mapping guide:
https://wiki.unvanquished.net/wiki/Mapping

## Project Structure

A basic map structure has been created for your map: {long_name}

## Start the map
Start the map ingame with the following command:
```
/devmap {short_name}
```


Note : a Licence file has been created for the meta picture. This meta picture has been created with Unvanquished's assets. If you change the meta picture, you should update the Licence file.

Enjoy!
""", encoding="utf-8")

    #LICENSE
    (target_root / "LICENSE.MD").write_text(
"""
The meta file is made with Unvanquished's assets wich are under the creative commons attribution-sharealike 2.5 license.
See https://github.com/Unvanquished/Unvanquished/blob/master/COPYING.txt for more information about the Unvanquished licenses.
""", encoding="utf-8")

    # SCRIPTS
    (target_root / "scripts").mkdir(parents=True, exist_ok=True)

    # TEXTURES
    textures_dir = target_root / "textures" / short_name
    textures_dir.mkdir(parents=True, exist_ok=True)

    lines = [
        "{",
        f'    map "{short_name}"',
        f'    longname "{long_name}"',
        f'    type "{map_type}"',
    ]
    for author in authors:
        lines.append(f'    author "{author}"')
    lines.append("}")

    arena_text = "\n".join(lines) + "\n"
    arena_path.write_text(arena_text, encoding="utf-8")

    print("\nFiles and directories created successfully :")
    print(target_root.resolve())

if __name__ == "__main__":
    main()

