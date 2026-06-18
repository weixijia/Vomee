# One-time hardware step for Path B (the only thing I can't do from code)

Everything in software is built and ready (`tools/`, `configFiles/`). The DCA1000
control half is already proven live. To switch the radar from "mmWave-Studio mode"
to "pure-Python mode", the IWR1843 must run the **`xwr18xx_mmw_demo`** firmware in
**functional mode** and be driven over the CLI UART (COM4).

## Decision tree

### Step 1 — close mmWave Studio
Release the radar + the UDP stream.

### Step 2 — set the board to FUNCTIONAL mode, then power-cycle
On the IWR1843BOOST set **SOP[2:0] = 001** → **SOP0 ON, SOP1 OFF, SOP2 OFF**
(jumpers/switches marked SOP0/SOP1/SOP2). Then unplug/replug the 5 V (power-cycle).
> Note: mmWave Studio drives SOP over the FTDI (`SOPControl(2)` in the Lua); for
> pure-Python use we rely on the physical SOP pins instead.

### Step 3 — is mmw_demo already flashed? (probe, read-only)
With Studio closed and the board power-cycled in functional mode:
```
cd mmwave_pure_python/tools
python probe_uart.py COM4
```
- **See a version banner / `Done` / `mmwDemo:` prompt** → mmw_demo is flashed.
  **Skip to Step 5.**
- **Blank / no response** → either not in functional mode (recheck SOP0) or
  mmw_demo isn't flashed → do Step 4.

### Step 4 — flash mmw_demo (only if Step 3 was blank)
Needs the **TI mmWave SDK 3.x for xwr18xx** (provides
`…/packages/ti/demo/xwr18xx/mmw/xwr18xx_mmw_demo.bin`). If you don't have the SDK,
download "MMWAVE-SDK" (xwr18xx, 3.5/3.6) from TI.
1. Put the board in **flashing/UART-boot mode** (per the IWR1843BOOST EVM user
   guide — verify the exact SOP switch positions in UniFlash's on-screen guide).
2. In **UniFlash**, pick IWR1843, select `xwr18xx_mmw_demo.bin` for the
   **METAIMAGE1 / Application** slot, flash.
3. Set back to **functional mode (Step 2)**, power-cycle, re-run Step 3.

### Step 5 — pure-Python trigger + Vomee
```
cd mmwave_pure_python/tools
python trigger_all.py --com COM4 --cfg ../configFiles/vomee_1843.cfg --json ../configFiles/cf.json
```
Then launch Vomee (`python main.py`). RA/RD heatmaps should appear with **mmWave
Studio NOT running**.

## What to watch for (data-identical check)
- The `.cfg` is a 1:1 translation of `skeleton.lua` → same chirp profile → same data.
- `lvdsStreamCfg -1 0 1 0` keeps the stream **header-less raw ADC** = matches today.
- RISK: mmw_demo also runs on-chip detection each frame; 255 loops @ 100 ms is heavy
  and the demo *may* report a processing-time violation. If frames don't stream,
  we lighten on-chip load (already minimized `guiMonitor`/`cfarFovCfg`) or adjust.
  The ADC chirp profile stays identical either way.
```
