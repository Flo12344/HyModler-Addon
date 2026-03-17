# HyModler
![Static Badge](https://img.shields.io/badge/Blender-4.+-g?logo=blender)\
HyModler is a Blender addon for supporting import and export of Hytale Blockymodel and Blockyanim as well as supporting modeling of it.

## Why?
The main reasons are modifiers(currently not supported) and bone constraints (through baking and keyframes reduction), the best would be to get geometry nodes to be usable in some capacity\
And also because of a let's say "skill issue" on my side I'm way more used to blender interface and shortcuts <.<

## Supported Features

- Modeling using the UI panel
- UV editing using the UI panel + snapping
- Texturing
- Attachment
- Bone animation
- Bone constraint
- Import
- Export
- Ignore object on export

## Future Features Goal

- Group animation (Main priority)
- Empty parent compact for first child
- Group to rig (for model imported)
- Modifiers support
- geometry nodes support
- Auto Rig parenting
- Better UV edit
- Better Size and Stretch edit
- Animated UV
- Animated Visibility

## How to Use

- Installation: Edit > Preferences > Add-ons > (Top-Right) Install from disk

- Object:
    - Use the N-Panel to add hymodler objects
- Modeling:
    - Classic "S" scale affect the stretch the others (G and R) works normally
    - Edit the values in HyModler on the N-Panel (in Object mode only)
- UV:
    - To rotate/flip use the tools in the N-Panel
    - To Move only use Face mode and disable "Sticky Selection Mode" (Try to only move UV using snapping the export rounds the UV positions)
- Animation:
    - (Currently) Animate using only Armatures
    - You should be able to use any bone constraint
- Modifier:
    - Not supported at the moment

## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

## License

[GPL-3.0-or-later](https://spdx.org/licenses/GPL-3.0-or-later.html)
