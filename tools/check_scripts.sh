#!/usr/bin/env bash
# Compile-check every GDScript in scripts/ and tests/ with the pinned Godot (prints only failures).
G="${GODOT:-/c/Program Files (x86)/Steam/steamapps/common/Godot Engine/godot.windows.opt.tools.64.exe}"
cd "$(dirname "$0")/.."
fail=0
for f in $(find scripts tests -name "*.gd" | sort); do
  out=$("$G" --headless --path . --check-only --script "res://$f" 2>&1 | grep -E "SCRIPT ERROR|Parse Error|Compile Error" | grep -v "Failed to compile depended" | grep -vE "Identifier not found: (Settings|Devices|DialogueDB|GameState|SaveService|AudioDirector)$")
  if [ -n "$out" ]; then echo "== $f"; echo "$out" | head -6; fail=1; fi
done
exit $fail
