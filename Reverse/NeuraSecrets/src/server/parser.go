package main

import (
	"bufio"
	"os"
	"strconv"
	"strings"
)

type InstructionParams struct {
	Opcode string
	NbArgs int
}

var (
	Instructions = map[string]InstructionParams{
		"add":           {Opcode: "A", NbArgs: 2},
		"mov":           {Opcode: "B", NbArgs: 2},
		"inc":           {Opcode: "C", NbArgs: 1},
		"cmp":           {Opcode: "D", NbArgs: 2},
		"push":          {Opcode: "E", NbArgs: 1},
		"pop":           {Opcode: "F", NbArgs: 1},
		"sleep":         {Opcode: "G", NbArgs: 1},
		"gethttp":       {Opcode: "H", NbArgs: 1},
		"execshellcode": {Opcode: "I", NbArgs: 1},
		"shell":         {Opcode: "J", NbArgs: 1},
		"posthttp":      {Opcode: "K", NbArgs: 1},
		"readfile":      {Opcode: "L", NbArgs: 1},
		"jmp":           {Opcode: "M", NbArgs: 1},
		"genkeys":       {Opcode: "N", NbArgs: 0},
		"gensecret":     {Opcode: "O", NbArgs: 0},
		"readstdin":     {Opcode: "P", NbArgs: 0},
		"enc":           {Opcode: "Q", NbArgs: 0},
		"dec":           {Opcode: "R", NbArgs: 0},
		"ik":            {Opcode: "S", NbArgs: 0},
		"je":            {Opcode: "T", NbArgs: 1},
		"jne":           {Opcode: "U", NbArgs: 1},
		"movr":          {Opcode: "V", NbArgs: 2},
		"md5":           {Opcode: "W", NbArgs: 0},
		"print":         {Opcode: "X", NbArgs: 0},
		"exit":          {Opcode: "Y", NbArgs: 1},
		"decfile":       {Opcode: "Z", NbArgs: 0},
	}
)

func parseInstruction(s string) Instruction {
	instrSplit := strings.Split(s, " ")
	opcode := Instructions[instrSplit[0]].Opcode
	rawArgs := instrSplit[1:]

	instruction := Instruction{Opcode: opcode}

	switch nbArgs := Instructions[instrSplit[0]].NbArgs; nbArgs {
	case 0:
		instruction.Args = []any{}
	case 1:
		// If there is spaces in the solo arg, it produces multiple args for an instruction that requires only one
		// So its a string
		if len(rawArgs) > 1 {
			arg := strings.Join(instrSplit[1:], " ")
			instruction.Args = []any{arg}
		} else {
			// To determine the type of the operande, (int | string)
			i, err := strconv.Atoi(rawArgs[0])
			if err != nil {
				instruction.Args = []any{rawArgs[0]}
			} else {
				instruction.Args = []any{i}
			}
		}
	case 2:
		args := []any{}
		for _, x := range rawArgs {
			i, err := strconv.Atoi(x)
			if err != nil {
				args = append(args, x)
			} else {
				args = append(args, i)
			}
		}
		instruction.Args = args
	}
	return instruction
}

func Parse(fileName string) (Shellcode, error) {
	var shellcode Shellcode

	file, err := os.Open(fileName)
	if err != nil {
		return shellcode, err
	}

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		if len(line) == 0 {
			continue
		}
		if line[0] == '#' {
			continue
		}
		instruction := parseInstruction(line)
		shellcode = append(shellcode, instruction)
	}

	return shellcode, nil
}
