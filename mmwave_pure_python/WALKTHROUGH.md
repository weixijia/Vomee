# Careful walkthrough — switching to pure-Python (read first, touch nothing yet)

## Where we are
- Software is **built and the DCA1000 half is proven live**. Nothing left to write
  to get a first capture.
- Your machine has **mmWave Studio + CCS** but **no mmWave SDK, no
  `xwr18xx_mmw_demo.bin`, no UniFlash**. So a one-time TI download *may* be needed —
  but only if the board's flash doesn't already hold mmw_demo. **We check first.**

## The plan, in safe order (no downloads until proven necessary)

### Phase 0 — hardware CONFIRMED by user
**AWR1843BOOST (red) + DCA1000EVM (green), 60-pin connector, NO carrier.**
AWR1843 = same xwr18xx silicon as IWR1843 → mmw_demo / `.cfg` / DCA1000 all identical.
The "AR-DevPack" FT4232H (COM6-9) is the DCA1000EVM's own FTDI (Studio's SPI/SOP path).

Boot mode is set by **SOP jumpers on the red AWR1843BOOST** (3 two-pin headers labeled
**SOP0 / SOP1 / SOP2**, see "Figure 13" in the AWR1843BOOST EVM user guide SPRUIM4).
Jumper installed = that SOP bit = 1.
| Mode | SOP2 | SOP1 | SOP0 | jumpers installed |
|------|------|------|------|-------------------|
| **Functional** (run mmw_demo) `001` | off | off | **on** | SOP0 only |
| **Flashing** (UniFlash) `101`       | **on** | off | **on** | SOP0 + SOP2 |
| Studio raw-capture (debug `011` / software SOPControl) | off | on | on | (Studio drives via DCA1000 FTDI) |

There is also an **NRST button = SW2**: after changing jumpers + power, press it once.

#### CONFIRMED on this board (user-reported): SOP is a 3x slide switch, **LEFT = ON, RIGHT = OFF**.
- Current (working with Studio) = SOP0 ON / SOP1 ON / SOP2 OFF = **011 (debug / raw-capture)** ✓ matches research.
- Functional (mmw_demo) = **001** = SOP0 ON / SOP1 OFF / SOP2 OFF.
- **Only change needed: flip SOP1 from LEFT(ON) to RIGHT(OFF).** Result = LEFT, RIGHT, RIGHT.
- Flashing (UniFlash) later = **101** = SOP0 ON / SOP1 OFF / SOP2 ON = LEFT, RIGHT, LEFT.

### Phase 1 — try the board AS-IS (mmw_demo may already be flashed)
1. **Close mmWave Studio** (frees the radar + the UDP stream).
2. Set the board to **functional mode** (`SOP[2:0]=001`) — confirmed in Phase 0.
3. **Power-cycle** the radar (unplug/replug the 5 V barrel jack).
4. Probe (read-only, safe):
   ```
   cd C:\Users\Chuang Yu\Documents\vomee\mmwave_pure_python\tools
   python probe_uart.py COM4
   ```
   - **Banner / `Done` / `mmwDemo:`** → mmw_demo IS flashed. **Skip Phase 2.**
   - **Blank** → not in functional mode (recheck SOP) or mmw_demo not flashed → Phase 2.

### Phase 2 — only if Phase 1 was blank: get + flash mmw_demo (one-time)
1. Download **MMWAVE-SDK for xwr18xx** (v3.6.x) from TI → install → the binary lands at
   `…/ti/mmwave_sdk_<ver>/packages/ti/demo/xwr18xx/mmw/xwr18xx_mmw_demo.bin`.
2. Download **UniFlash** (standalone) from TI.
3. Set board to **flashing/UART-boot mode** (UniFlash shows the exact SOP positions for
   the IWR1843; on ICBOOST it's the SOP switch set to the "SOP5/flash" combo).
4. UniFlash → device **IWR1843** → load `xwr18xx_mmw_demo.bin` into the
   **Meta Image 1 / Application** slot → **Flash**.
5. Set back to **functional mode** (Phase 1 step 2), power-cycle, re-run the probe.

### Phase 3 — first pure-Python capture
```
cd C:\Users\Chuang Yu\Documents\vomee\mmwave_pure_python\tools
python trigger_all.py --com COM4 --cfg ../configFiles/vomee_1843.cfg --json ../configFiles/cf.json
```
Watch for `config_fpga -> success`, `stream_start -> success`, and `>>> sensorStart`.
Then launch your capture (`capture_single.py` or Vomee `main.py`) — RA/RD should appear
**with mmWave Studio closed**.

### Phase 4 — verify data is identical
- Capture a short `raw.bin` both ways (Studio vs pure-Python) on a static scene and
  compare frame size + RA/RD. The `.cfg` is a 1:1 translation, so they should match.
- If frames stall: mmw_demo's on-chip processing may be too heavy at 255 loops/100 ms.
  We then trim on-chip load (the chirp profile / data stay identical).

## Reverting to today's setup
Nothing here is destructive except the optional flash. To go back to Studio: set SOP to
the Studio/development position and run your Lua as before. (Flashing mmw_demo does NOT
block Studio — Studio RAM-loads its own firmware regardless.)
