# Test Plan — bringing up pure-Python triggering on live hardware

## Why we can't just run it now
Your radar is **currently streaming because mmWave Studio configured it** by
loading its own image into the IWR1843's RAM over the FTDI (mmwavelink/SPI). The
pure-Python path (pyRadar/OpenRadar) instead drives the **mmWave SDK out-of-box
demo firmware (`xwr18xx_mmw_demo`)** over the CLI UART (COM4). Those are two
different, mutually-exclusive radar boot modes. So testing requires changing the
radar's boot mode — a physical action on the board.

## Prerequisites (one-time, user/physical)
1. **Firmware**: `xwr18xx_mmw_demo` must be flashed to the IWR1843 (UniFlash).
   - It may already be on flash (it's the out-of-box demo). mmWave Studio bypasses
     it by RAM-loading, so flashing it does NOT break your Studio workflow.
2. **Boot mode**: set the IWR1843BOOST to **Functional mode, SOP[2:0] = 001**
   (SOP0 ON / jumper on, SOP1 & SOP2 OFF), then power-cycle. This is what lets the
   flashed demo run and accept CLI commands on COM4.
3. Close mmWave Studio (release the radar + the UDP stream).

## Test sequence (software, all pure Python — no C build)
Run from `downloads/pyRadar` with a `.cfg` whose params match Vomee `config.py`
(255 chirps area, 256 samples, 2TX/4RX) AND has LVDS streaming enabled:
`adcbufCfg -1 0 1 1 1` + `lvdsStreamCfg -1 0 1 0`; cf.json `lvdsMode=2` (1843=2 lane).

- **T1 — DCA1000 link only (non-destructive smoke test).**
  `DCA1000().sys_alive_check()` + `read_fpga_version()`. Confirms we can talk to the
  FPGA on UDP 4096 with no radar reconfig. *This is the one test that might be safe
  to run even now — it only queries the FPGA.* (TBD: confirm it won't disturb an
  active Studio capture; default assumption = run only after Studio is closed.)
- **T2 — UART handshake.** Open COM4 @115200, send `sensorStop`/version query, read
  the mmw_demo banner. Confirms demo firmware + correct CLI port.
- **T3 — Full trigger via pyRadar `captureAll.py`** (numframes small, e.g. 10).
  Verify a `raw_data_*.bin` is written and decodes (testDecode.ipynb).
- **T4 — Integrate into Vomee.** New `core/mmwave_trigger.py` (pure python, extracted
  control only) called by `main.py` before the capture thread starts; confirm RA/RD
  heatmaps appear with **mmWave Studio NOT running**.

## Fallback if firmware/SOP path is undesirable
If you must keep the exact mmWave Studio RF behavior and not re-flash, the only
pure-software route is replicating mmwavelink-over-SPI through the FTDI (pyftdi or
TI MMWAVE-DFP). pyRadar implements this **only for AWR2243**, not IWR1843 — so this
is a larger custom effort (port the DFP SPI sequence). Documented as Path A.
