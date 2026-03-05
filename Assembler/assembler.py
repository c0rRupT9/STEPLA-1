import sys
import re

REGS = {'RA': 0, 'RB': 1, 'RC': 2, 'RD': 3}
ISA = {
    'NOP': 0x0, 'HLT': 0x1, 'ADD': 0x2, 'SUB': 0x3,
    'MOV': 0x4, 'MOVI': 0x5, 'STRD': 0x6, 'OUT': 0x7,
    'JMP': 0x8, 'JZ': 0x9, 'JC': 0xA, 'LDIM': 0xB,
    'LDD': 0xC, 'GETPC': 0xD, 'JP': 0xE, 'STIM': 0xF
}

def lex(content):
    lines = content.splitlines()
    for line_num, line in enumerate(lines, 1):
        line = re.sub(r';.*', '', line) # Strip comments
        tokens = re.findall(r'[a-zA-Z0-9_.]+|[:|,|\[|\]]', line)
        for t in tokens:
            if t == ',': yield (t, 'COMMA', line_num)
            elif t == ':': yield (t, 'COLON', line_num)
            elif t == '[': yield (t, 'LBRACK', line_num)
            elif t == ']': yield (t, 'RBRACK', line_num)
            elif re.match(r'^(0x[0-9a-fA-F]+|0b[01]+|[0-9]+)$', t):
                yield (t, 'NUM', line_num)
            else:
                yield (t, 'STR', line_num)

def parse(content):
    tokens = list(lex(content))
    mem = []
    labels = {}
    constants = {}
    fwd = [] 
    
    # Symbols and Definitions Pass
    scan_idx = 0
    temp_mem_ptr = 0
    while scan_idx < len(tokens):
        text, ttype, line = tokens[scan_idx]
        
        if text.upper() == '.DEFINE':
            name = tokens[scan_idx + 1][0]
            val = tokens[scan_idx + 2][0]
            constants[name] = int(val, 0)
            scan_idx += 3
        elif text.upper() in ISA:
            cmd = text.upper()
            # Instructions that take an immediate value (2nd byte)
            if cmd in ['MOVI', 'JMP', 'JZ', 'JC', 'LDIM', 'STIM']:
                temp_mem_ptr += 2
            else:
                temp_mem_ptr += 1
            scan_idx += 1
        elif scan_idx + 1 < len(tokens) and tokens[scan_idx + 1][1] == 'COLON':
            labels[text] = temp_mem_ptr
            scan_idx += 2
        else:
            scan_idx += 1

    # Translation Pass
    idx = 0
    while idx < len(tokens):
        text, ttype, line = tokens[idx]
        
        if ttype in ['COLON', 'LBRACK', 'RBRACK'] or (ttype == 'STR' and idx + 1 < len(tokens) and tokens[idx+1][1] == 'COLON'):
            idx += 1; continue
        if text.upper() == '.DEFINE':
            idx += 3; continue

        cmd = text.upper()
        if cmd in ISA:
            opcode = ISA[cmd]
            idx += 1
            
            def get_op():
                nonlocal idx
                while idx < len(tokens) and tokens[idx][1] in ['COMMA', 'LBRACK', 'RBRACK']:
                    idx += 1
                if idx >= len(tokens):
                    raise ValueError(f"Line {line}: {cmd} missing operand.")
                op_text, op_type, op_line = tokens[idx]
                idx += 1
                return op_text

            try:
                if cmd in ['NOP', 'HLT']:
                    mem.append(opcode << 4)
                
                elif cmd in ['ADD', 'SUB', 'MOV', 'STRD', 'LDD']:
                    rd_str, rs_str = get_op().upper(), get_op().upper()
                    rd = REGS[rd_str] if rd_str in REGS else (constants[rd_str] if rd_str in constants else int(rd_str, 0))
                    rs = REGS[rs_str] if rs_str in REGS else (constants[rs_str] if rs_str in constants else int(rs_str, 0))
                    mem.append((opcode << 4) | ((rd & 0x3) << 2) | (rs & 0x3))
                
                # Handling LDIM, STIM, and MOVI as 2-byte Immediate instructions
                elif cmd in ['MOVI', 'LDIM', 'STIM']:
                    rd_str = get_op().upper()
                    mem.append((opcode << 4) | (REGS[rd_str] << 2)) # Bits 3 and 2 used for register
                    val_str = get_op()
                    val = constants[val_str] if val_str in constants else int(val_str, 0)
                    mem.append(val & 0xFF)
                
                elif cmd in ['OUT', 'GETPC', 'JP']:
                    r = get_op().upper()
                    mem.append((opcode << 4) | (REGS[r] << 2))
                
                elif cmd in ['JMP', 'JZ', 'JC']:
                    mem.append(opcode << 4)
                    target = get_op()
                    if target in labels: mem.append(labels[target])
                    elif target in constants: mem.append(constants[target])
                    else:
                        try: mem.append(int(target, 0))
                        except: fwd.append((target, len(mem), line)); mem.append(0)
            except (KeyError, ValueError) as e:
                raise ValueError(f"Line {line}: Logic Error - {e}")
        else:
            idx += 1

    for name, pos, line in fwd:
        if name in labels: mem[pos] = labels[name]
        else: raise ValueError(f"Line {line}: Undefined Label '{name}'")
    
    return labels, constants, mem

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python assembler.py test.asm")
    else:
        with open(sys.argv[1], 'r') as f:
            content = f.read()
        
        labels, constants, mem = parse(content)
        
        print("--- SYMBOLS ---")
        for k, v in constants.items(): print(f"CONST {k} = {v} (0x{v:02X})")
        for k, v in labels.items(): print(f"LABEL {k} = {v} (0x{v:02X})")
        
        # Append 'ff' to the memory list before generating hex string
        mem.append(0xFF)
        
        hex_out = "v2.0 raw\n" + ' '.join(format(m, '02x') for m in mem)
        print("\n--- HEX OUTPUT ---")
        print(hex_out)
        
        output_filename = sys.argv[1].rsplit('.', 1)[0] + ".hex"
        with open(output_filename, 'w') as f:
            f.write(hex_out)
        print(f"\nSuccess: {output_filename}")