# STEPLA-1 8-bit Hardwired CPU

A complete 8-bit Harvard architecture CPU designed 
and simulated in Logisim-Evolution, built entirely 
from individual logic gates down to the gate level.

**Version:** 2.4.2  
**Status:** Under Development

---

## What Is STEPLA-1?

STEPLA-1 is a fully functional 8-bit CPU where every 
component; registers, decoders, ALU, control unit 
is built from individual 74-series logic gates. 
No black box components. Every signal path is visible, 
traceable, and documented.

Unlike EEPROM-based designs, STEPLA-1 uses a fully 
**hardwired control unit**  a gate-level AND/OR matrix 
where every control signal is a physical gate whose 
inputs you can probe with a multimeter. This makes the 
machine transparent in a way that microcode-based 
designs cannot be.

---

## Key Features

**Architecture**
- 8-bit Harvard architecture
- 4-bit opcode space, 16 instructions
- 4 general purpose registers (RA-RD)
- Separate instruction and data RAM (256 bytes each)
- Bootstrap Control Unit (BCU) for cold-boot ROM → RAM transfer

**Control Unit**
- Fully hardwired PLA-inspired gate matrix
- Hierarchical decode: opcode decoder + step decoder + AND matrix
- No EEPROM, no microcode pure combinational logic
- Every control signal traceable to individual gates

**Performance**
- Variable cycle instructions: 3 to 5 clock cycles
- Early-exit conditional branching (25% latency reduction)
- Synchronous load-to-one reset (33% efficiency gain over v2.3)
- Calculated IPC: 0.200-0.333, weighted average 0.263
- Target clock: 4 MHz on physical breadboard
- Effective throughput: ~1 MIPS at target frequency

**Instruction Set**
| Opcode | Instruction | Cycles | Description |
|--------|-------------|--------|-------------|
| 0x0 | NOP | 3 | No operation |
| 0x1 | HLT | 3 | Halt execution |
| 0x2 | ADD | 5 | Add registers |
| 0x3 | SUB | 5 | Subtract registers |
| 0x4 | MOV | 3 | Register to register |
| 0x5 | MOVI | 4 | Load immediate |
| 0x6 | STRD | 4 | Store to data RAM |
| 0x7 | OUT | 3 | Output register |
| 0x8 | JMP | 4 | Unconditional jump |
| 0x9 | JZ | 3/5 | Jump if zero |
| 0xA | JC | 3/5 | Jump if carry |
| 0xB | LDIM | 5 | Load immediate address |
| 0xC | LDD | 4 | Load from data RAM |
| 0xD | GETPC | 3 | Get program counter |
| 0xE | JP | 3 | Jump to register |
| 0xF | STIM | 5 | Store immediate address |

---

## Why STEPLA-1 Is Different

Most educational CPU projects use one of two approaches:
- **EEPROM microcode** (Ben Eater's SAP-1): Simple to implement, 
  opaque in operation
- **HDL simulation** (VHDL/Verilog): Powerful but abstracted 
  from physical reality

STEPLA-1 takes a third path: **discrete gate simulation that 
maps directly to physical components**. Every Logisim gate 
corresponds to a real 74-series IC you can buy at an 
electronics market. The simulation IS the schematic.

**Comparison with SAP-1:**

| Feature | SAP-1 | STEPLA-1 |
|---------|-------|----------|
| Instructions | 5 | 16 |
| Registers | 2 (fixed purpose) | 4 (general purpose) |
| RAM | 16 bytes | 256 bytes |
| Control unit | EEPROM microcode | Hardwired gates |
| Conditional jumps | None | JZ, JC with early exit |
| Bootstrap loader | None | Hardware BCU |
| Target clock | ~1 MHz | 4 MHz |
| Effective throughput | ~0.17 MIPS | ~1 MIPS |

---

## Repository Structure
```
STEPLA-1/
├── simulation/
│   ├── STEPLA-1.circ          # Main Logisim-Evolution file
│   ├── control_unit.circ      # Control unit subcircuit
│   ├── register_file.circ     # Register selector subcircuit
│   └── BCU.circ               # Bootstrap control unit
├── programs/
│   ├── fibonacci.asm          # Fibonacci sequence demo
│   └── counter.asm            # Basic counter program
├── docs/
│   └── STEPLA-1_Spec_v2.4.2.pdf  # Full specification
└── README.md
```

---

## Getting Started

### Requirements
- [Logisim-Evolution](https://github.com/logisim-evolution/logisim-evolution) 
  v3.8.0 or later

### Running the Simulation
1. Clone this repository
2. Open `simulations/8bitcomp.circ` in Logisim-Evolution
3. Load `programs/fibonacci.asm` into the ROM
4. Toggle switch to 1 and press reset button.
5. Run the clock at desired frequency.

### Loading a Program
Programs are loaded via the Bootstrap Control Unit automatically.
On simulation start the BCU copies the instruction ROM contents
to instruction RAM before releasing control to the CPU.
See Section 8 of the specification for BCU operation details.

---

## Documentation

The full **43-page specification** covers:

- Control unit theory and PLA architecture
- Complete ISA with encoding rules
- Every instruction's T-state microoperation sequence  
- Clock phase synchronization and dual-edge design
- BCU boot protocol and T0 null state
- Signal conditioning for physical breadboard build
- Timing analysis with real component datasheets
- Known limitations and v3.0 roadmap

📄 **[Read the Full Specification](/STEPLA-1 Control Unit Design Specifictation Manual v2.4.2.pdf)**

---

## Physical Build

STEPLA-1 is designed for physical construction using 74HCT series logic:

**Key components:**
- Logic: 74HCT08, 74HCT32, 74HCT14, 74HCT86
- Registers: 74HCT377, 74HCT175, 74HCT74
- Decode: 74HCT154, 74HCT138, 74HCT139
- Counter: 74HCT163
- ALU: 74HCT283 (×2 cascaded)
- Memory: AS6C62256 SRAM, AT28C64B EEPROM
- Bus: 74HCT244, 74HCT245

Target clock speed: **4 MHz** (verified via timing analysis,
critical path: 101ns, half-cycle budget: 125ns at 4 MHz)

---

## Roadmap

**v2.5.0 (planned)**
- Overflow flag (VF) and Negative flag (NF)
- Signed arithmetic support
- JV and JN conditional jump instructions
- Proteus ISIS simulation with real component models

**v3.0.0 (planned)**
- 16-bit instruction word
- 16-register general purpose file
- Hardware stack (PUSH/POP/CALL/RET)
- Dual asynchronous control units
- Pre-fetch buffer approaching 1.0 CPI

---

## Acknowledgments

This project builds on the work of:
- **Ben Eater** — whose 8-bit breadboard computer 
  series demonstrated that CPU design can be made 
  completely transparent
- **Leon Nicolas** — whose cascaded RAM implementation 
  in Logisim provided the structural insight that 
  led to STEPLA-1's hardwired control matrix
- **Albert Paul Malvino** — Digital Computer Electronics
- **Patterson and Hennessy** — Computer Organization and Design
- **Charles Petzold** — Code: The Hidden Language of 
  Computer Hardware and Software

---

## Contributing

Contributions welcome. Areas of particular interest:
- Physical breadboard build documentation
- Additional assembly programs
- Assembler implementation
- Proteus simulation port
- v3.0 architecture discussion

Please open an issue before submitting large changes.

---

## License

This project is open source.
[MIT License](LICENSE)

---
