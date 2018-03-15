import r2pipe
import sys
import svg

def main():
    _file = sys.argv[1]
    offset = sys.argv[2]
    r = r2pipe.open(_file)

    print "[*] Openinig debugger"

    r.cmd("doo")
    r.cmd("db %s" % offset)
    r.cmd("dc")

    print "[*] Reading registers"
    regs = r.cmdj("drj")

    if not 'rip' in regs.keys():
        print "[!] Bad architecture!! Aborting"
        quit()

    # For now just 64 bits
    i = svg.Image()
    curr_off = regs['rsp'] - 8
    while (curr_off < regs['rbp'] + 16):
        # Read qword
        if curr_off == regs['rbp']:
            i.add_register(i.curr_memory_cell(), 'RBP')
        elif curr_off == regs['rsp']:
            i.add_register(i.curr_memory_cell(), 'RSP')
        mem = r.cmdj('pxqj 8 @ %s' % curr_off)[0]
        mem_str = '0x{0:08x}_{1:08x}'.format((mem & 0xffffffff00000000) >> 32,
                                             mem & 0xffffffff)
        i.add_memory_cell(mem_str)

        print '[*] Reading address: 0x{0:016x}'.format(curr_off)

        curr_off += 8

    print "[*] Reading assembly lines"
    # Write code
    prev_instructions = [x['opcode'] for x in r.cmdj("pdj -3")]
    next_instructions = [x['opcode'] for x in r.cmdj("pdj 3")]

    for x in prev_instructions:
        i.add_code_line(x)

    i.set_pc(i.curr_code_line())

    for x in next_instructions:
        i.add_code_line(x)

    i.save()

    print "[+] DONE, you can now open 'fig.svg' with your web browser"

if __name__ == '__main__':
    try:
        if len(sys.argv) < 3:
            print "Usage: python env.py binary 0xaddress"
        else:
            print "It just works with x86, 64 bits binaries"
            main()
    except KeyboardInterrupt:
        # TODO
        pass
