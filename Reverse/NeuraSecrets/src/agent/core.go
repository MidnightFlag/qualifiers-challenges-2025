package main

import (
	"crypto/ecdh"
	"errors"
)

type Process struct {
	Registers             map[int64]any
	Sp                    int64
	Ip                    int64
	Stack                 []any
	InstructionsFunctions []InstructionFunction
	Flags                 map[string]int64
	Keys                  struct {
		Pub    *ecdh.PublicKey
		Priv   *ecdh.PrivateKey
		Secret []byte
	}
}

type Shellcode []Instruction

type Instruction struct {
	Opcode string
	Args   []any
}

func (p *Process) Pop() (any, []any) {
	p.Sp -= 1
	return p.Stack[len(p.Stack)-1], p.Stack[:len(p.Stack)-1]
}

// Resolves the reg index, if not found return -1
func (p *Process) FindReg(s string) int64 {
	regs := map[string]int64{
		"rax": 1,
		"rbx": 2,
		"rcx": 3,
		"rdx": 4,
		"rdi": 5,
		"rsi": 6,
	}
	reg, ok := regs[s]
	if ok {
		return reg
	}
	return -1
}

func (p *Process) Init(args []any) {

	// Init Registers
	p.Registers = make(map[int64]any)
	p.Registers[1] = int(0) // RAX
	p.Registers[2] = int(0) // RBX
	p.Registers[3] = int(0) // RCX
	p.Registers[4] = int(0) // RDX
	p.Registers[5] = int(0) // RDI

	// Init Pointers
	p.Sp = 0
	p.Ip = 0

	// Load the process instructions
	p.LoadInstructions()

	// init stack
	p.Stack = []any{}
	if len(args) > 0 {
		p.Stack = append(p.Stack, args...)
	}

	// init flags
	p.Flags = make(map[string]int64)
	p.Flags["CF"] = 0
	p.Flags["ZF"] = 0
}

// Runs the shellcode and return the result process
func RunShellcode(shellcode Shellcode, shellcodeArgs []any) (*Process, error) {

	p := &Process{}
	p.Init(shellcodeArgs)

	for p.Ip < int64(len(shellcode)) {
		instrSc := shellcode[p.Ip]

		instrSlice := Filter(
			p.InstructionsFunctions,
			func(i InstructionFunction) bool { return i.Opcode == instrSc.Opcode },
		)

		if len(instrSlice) != 1 {
			return nil, errors.New("core: No instruction found")
		}
		instr := instrSlice[0]

		instr.Func(p, instrSc.Args) // On donne tout a la methode et elle fera le parsing
	}
	return p, nil
}
