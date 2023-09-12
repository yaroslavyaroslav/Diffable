# Diffable

This is a file comparison plugin for Sublime Text 4, it relies on its internal [Incremental Diff](http://www.sublimetext.com/docs/incremental_diff.html) feature.

Enjoy!

### Installation
Please install Sublime [Package Control]("https://sublime.wbond.net/installation") first. Then inside *Package Control: Install Package*, type *Diffable* and then click to confirm.

### Usage
It's as easy as just:
1. Install the plugin.
2. Open two tabs in a row either way.
3. Hit bindings bellow or run it by Sublime Text Command Pallet.
4. Bonus: By hitting `super+k` followed by `super+/`, you'll get side by side diff view provided by Sublime Text.

1. To compare and show the diffs, press **super + k** followed by **super + d**.
2. To clear the marked lines, press press **super + k** followed by **super + c**.

### Settings
#### The default key binding for Mac is

```
{ "keys": ["super+k", "super+d"], "command": "diffable" }
{ "keys": ["super+k", "super+c"], "command": "diffable", "args": {"action": "clear"} }
```

#### The default key binding for Windows / Linux is

```
{ "keys": ["ctrl+k", "ctrl+d"], "command": "diffable" }
{ "keys": ["ctrl+k", "ctrl+c"], "command": "diffable", "args": {"action": "clear"} }
```


## Thanks

This plugin is a refactored and updated verion of https://github.com/zsong/diffy which is seems depricated long ago.