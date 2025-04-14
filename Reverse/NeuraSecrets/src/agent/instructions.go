package main

import (
	"bufio"
	"bytes"
	"crypto/ecdh"
	"crypto/rand"
	"encoding/json"
	"errors"
	"fmt"
	"io"
	"net/http"
	"os"
	"os/exec"
	"slices"
	"strings"
	"time"
)

type InstructionFunction struct {
	Name   string
	Opcode string
	Func   func(*Process, []any) error
}

func (p *Process) LoadInstructions() {

	p.InstructionsFunctions = []InstructionFunction{
		{Opcode: "A", Func: Add},
		{Opcode: "B", Func: Mov},
		{Opcode: "C", Func: Inc},
		{Opcode: "D", Func: CmpReg},
		{Opcode: "E", Func: Push},
		{Opcode: "F", Func: Pop},
		{Opcode: "G", Func: Sleep},
		{Opcode: "H", Func: GetHTTP},
		{Opcode: "I", Func: ExecuteShellcode},
		{Opcode: "J", Func: ExecuteCommand},
		{Opcode: "K", Func: PostHTTP},
		{Opcode: "L", Func: ReadFile},
		{Opcode: "M", Func: Jump},
		{Opcode: "N", Func: GenKeys},
		{Opcode: "O", Func: GenSecret},
		{Opcode: "P", Func: ReadStdin},
		{Opcode: "Q", Func: Enc},
		{Opcode: "R", Func: Dec},
		{Opcode: "S", Func: InitKeys},
		{Opcode: "T", Func: JumpIfEquals},
		{Opcode: "U", Func: JumpIfNotEquals},
		{Opcode: "V", Func: MovReg},
		{Opcode: "W", Func: doMD5},
		{Opcode: "X", Func: Print},
		{Opcode: "Y", Func: Exit},
		{Opcode: "Z", Func: DecryptFile},
	}
}

// Adds, name is self explanatory
// Arg one should be a register name [rax, rbx, rcx, rdx] (string)
// Arg two, either a number or a register number (int)
func Add(p *Process, args []any) error {
	if len(args) != 2 {
		return errors.New("")
	}
	r1Id := p.FindReg(args[0].(string))
	arg1 := args[1]
	switch t := arg1.(type) {
	case string:
		r2Id := p.FindReg(t)
		p.Registers[r1Id] = p.Registers[r1Id].(int64) + p.Registers[r2Id].(int64)
	case json.Number:
		v, err := arg1.(json.Number).Int64()
		if err != nil {
			return err
		}
		p.Registers[r1Id] = p.Registers[r1Id].(int64) + v
	}

	p.Ip += 1
	return nil
}

// Mov value in register
func Mov(p *Process, args []any) error {
	rId := p.FindReg(args[0].(string))

	v, err := args[1].(json.Number).Int64()
	if err != nil {
		return err
	}

	p.Registers[rId] = v
	p.Ip += 1
	return nil
}

func MovReg(p *Process, args []any) error {
	r1Id := args[0].(string)
	r2Id := args[1].(string)

	r1 := p.FindReg(r1Id)
	r2 := p.FindReg(r2Id)

	p.Registers[r1] = p.Registers[r2]
	p.Ip += 1
	return nil
}

func Inc(p *Process, args []any) error {
	rId := p.FindReg(args[0].(string))
	p.Registers[rId] = p.Registers[rId].(int64) + 1
	p.Ip += 1
	return nil
}

// Takes a register and push it's value on the stack
func Push(p *Process, args []any) error {
	rId := p.FindReg(args[0].(string))
	p.Stack = append(p.Stack, p.Registers[rId])
	p.Ip += 1
	return nil
}

func Pop(p *Process, args []any) error {
	rId := p.FindReg(args[0].(string))
	value, stack := p.Stack[len(p.Stack)-1], p.Stack[:len(p.Stack)-1]
	p.Stack = stack

	p.Registers[rId] = value

	p.Ip += 1
	return nil
}

// Changes the opcode of a function for the current process
// Arg1 : The current function opcode
// Arg2 : The new opcode
// If provided an already attributed opcode, swaps the function opcode
func ChangeOpcode(p *Process, args []any) error {
	opcode1 := args[0].(string)
	opcode2 := args[0].(string)

	func1Idx := slices.IndexFunc(
		p.InstructionsFunctions,
		func(i InstructionFunction) bool { return i.Opcode == opcode1 },
	)
	func2Idx := slices.IndexFunc(
		p.InstructionsFunctions,
		func(i InstructionFunction) bool { return i.Opcode == opcode2 },
	)

	if func1Idx == -1 {
		return errors.New("")
	}

	func1 := p.InstructionsFunctions[func1Idx]
	// if no function has already the new opcode
	if func2Idx == -1 {
		func1.Opcode = opcode2
		p.InstructionsFunctions[func1Idx] = func1
	} else {
		func2 := p.InstructionsFunctions[func2Idx]
		func1.Opcode = opcode2
		func2.Opcode = opcode1

		p.InstructionsFunctions[func1Idx] = func1
		p.InstructionsFunctions[func2Idx] = func2
	}
	p.Ip += 1
	return nil
}

func Sleep(p *Process, args []any) error {
	if len(args) != 1 {
		return errors.New("")
	}
	v, err := args[0].(json.Number).Int64()
	if err != nil {
		return err
	}
	duration := int(v)

	time.Sleep(time.Duration(duration) * time.Second)
	p.Ip += 1
	return nil
}

// GetHTTP
// Perform http.Get and store result on the stack
func GetHTTP(p *Process, args []any) error {
	url := args[0].(string)
	res, err := http.Get(url)
	if err != nil {
		return err
	}

	resBody, err := io.ReadAll(res.Body)
	if err != nil {
		return err
	}

	p.Registers[1] = resBody

	p.Ip += 1
	return nil
}

// Take the shellcode addr on the stack from RAX, convert it in Shellcode type and execute it
// Get back the shellcode result and put it on the stack
// Takes one argument, the number of arguments of the starting shellcode
func ExecuteShellcode(p *Process, args []any) error {
	shellcodeBytes := p.Registers[5].([]byte)
	shellcodeArgs := []any{}

	var nbArgs int = 0
	nbArgsJ, ok := args[0].(json.Number)
	if !ok {
		nbArgs = args[0].(int)
	} else {
		nbArgs64, _ := nbArgsJ.Int64()
		nbArgs = int(nbArgs64)
	}
	if nbArgs > 0 {
		for i := 0; i < int(nbArgs); i++ {
			var a any
			var stack []any
			if len(p.Stack) == 1 {
				a, stack = p.Stack[0], []any{}
			} else {
				a, stack = p.Stack[len(p.Stack)-1], p.Stack[:len(p.Stack)-1]
			}
			p.Stack = stack
			shellcodeArgs = append(shellcodeArgs, a)
		}
	}

	var shellcode Shellcode
	shellcodeReader := bytes.NewReader(shellcodeBytes)

	decoder := json.NewDecoder(shellcodeReader)
	decoder.UseNumber()
	decoder.Decode(&shellcode)

	subProcessResult, err := RunShellcode(shellcode, shellcodeArgs)
	// if no error, set rax at 1, else 0
	if err != nil {
		p.Registers[1] = int64(0)
	}
	p.Registers[1] = int64(1)
	p.Registers[5] = subProcessResult
	p.Ip += 1
	return nil
}

// First args is the command to execute
// Returns the result on the stack
func ExecuteCommand(p *Process, args []any) error {

	command := args[0].(string)
	cmd := exec.Command(command)
	stdout, err := cmd.Output()
	if err != nil {
		return err
	}

	p.Registers[1] = stdout
	p.Ip += 1
	return nil
}

// Takes the value on rax and send it to the specified endpoint
func PostHTTP(p *Process, args []any) error {

	endpoint := args[0].(string)
	value := p.Registers[5].([]byte)

	r, err := http.NewRequest(http.MethodPost, endpoint, bytes.NewBuffer(value))
	if err != nil {
		return err
	}

	client := http.Client{}
	_, err = client.Do(r)
	if err != nil {
		return err
	}
	p.Ip += 1
	return nil
}

// Read the file given on argument
// Stores the result on the stack
func ReadFile(p *Process, args []any) error {
	fileName := args[0].(string)
	if _, err := os.Stat(fileName); errors.Is(err, os.ErrNotExist) {
		p.Ip += 1
		return err
	}

	file, err := os.ReadFile(fileName)
	if err != nil {
		p.Ip += 1
		return err
	}

	p.Registers[1] = file
	p.Ip += 1
	return nil
}

// Generate client keys, and put the client on rax
func GenKeys(p *Process, args []any) error {
	clientCurve := ecdh.P256()
	clientPrivKey, err := clientCurve.GenerateKey(rand.Reader)
	if err != nil {
		return err
	}
	p.Keys.Pub = clientPrivKey.PublicKey()
	p.Keys.Priv = clientPrivKey

	p.Registers[1] = p.Keys.Pub.Bytes()

	p.Ip += 1
	return nil
}

// Takes the secret public key on rdi
func GenSecret(p *Process, args []any) error {
	serverPubkeyBytes := p.Registers[1]

	curve := ecdh.P256()
	serverPub, err := curve.NewPublicKey(serverPubkeyBytes.([]byte))
	if err != nil {
		return err
	}

	clientSecret, err := p.Keys.Priv.ECDH(serverPub)
	if err != nil {
		return err
	}
	p.Keys.Secret = clientSecret
	p.Ip += 1
	return nil
}

// Get subprocess on rdi
func InitKeys(p *Process, args []any) error {
	subProcess := p.Registers[5].(Process)
	p.Keys = subProcess.Keys
	p.Ip += 1
	return nil
}

// Change p.Ip to make a jump into the shellcode
// If the offset is wrong, returns an error
func Jump(p *Process, args []any) error {
	offset, err := args[0].(json.Number).Int64()
	if err != nil {
		return err
	}
	newIp := p.Ip + offset
	if newIp < 0 {
		return errors.New("")
	}
	p.Ip = newIp
	return nil
}

func JumpIfNotEquals(p *Process, args []any) error {
	if p.Flags["ZF"] == 0 {
		Jump(p, args)
	} else {
		p.Ip += 1
	}
	return nil
}

func JumpIfEquals(p *Process, args []any) error {
	if p.Flags["ZF"] == 1 {
		Jump(p, args)
	} else {
		p.Ip += 1
	}
	return nil
}

// Compare two registers
func CmpReg(p *Process, args []any) error {
	r1Id := p.FindReg(args[0].(string))
	r2Id := p.FindReg(args[1].(string))
	switch p.Registers[r1Id].(type) {
	case int64:
		v2, ok := p.Registers[r2Id].(int64)
		if !ok {
			p.Registers[1] = int64(-1)
			return nil
		}
		v1 := p.Registers[r1Id].(int64)
		if v1 == v2 {
			p.Flags["ZF"] = 1
			p.Flags["CF"] = 0

		} else if v1 < v2 {
			p.Flags["ZF"] = 0
			p.Flags["CF"] = 1
		} else {
			p.Flags["ZF"] = 0
			p.Flags["CF"] = 0
		}
	case []byte:
		v2, ok := p.Registers[r2Id].([]byte)
		if !ok {
			p.Registers[1] = int64(-1)
			return nil
		}
		v1 := p.Registers[r1Id].([]byte)
		res := bytes.Compare(v1, v2)
		if res == 0 {
			p.Flags["ZF"] = 1
			p.Flags["CF"] = 0
		} else if res < 0 {
			p.Flags["ZF"] = 0
			p.Flags["CF"] = 1
		} else {
			p.Flags["ZF"] = 0
			p.Flags["CF"] = 0
		}
	}

	p.Ip += 1
	return nil
}

// Takes the first value on the rdi and encrypt it and replace it
func Enc(p *Process, args []any) error {
	value := p.Registers[5].([]byte)

	enc, err := EncryptData(value, p.Keys.Secret)
	if err != nil {
		return err
	}

	p.Registers[1] = enc
	p.Ip += 1
	return nil
}

// Read the value to decrypt from rdi
// return it on rax
func Dec(p *Process, args []any) error {
	value := p.Registers[5].([]byte)

	dec, err := DecryptData(value, p.Keys.Secret)
	if err != nil {
		return err
	}

	p.Registers[1] = dec
	p.Ip += 1
	return nil
}

// Read value on stdin and return it in rax
func ReadStdin(p *Process, args []any) error {
	reader := bufio.NewReader(os.Stdin)
	fmt.Print("Enter your key: ")
	key, _ := reader.ReadString('\n')
	key = strings.Trim(key, "\n")

	p.Registers[1] = []byte(key)
	p.Ip += 1
	return nil
}

func doMD5(p *Process, args []any) error {
	plain := p.Registers[5].([]byte)
	hash := MD5(plain)

	p.Registers[1] = hash
	p.Ip += 1
	return nil
}

func Print(p *Process, args []any) error {
	v := p.Registers[5]
	switch v.(type) {
	case string:
		fmt.Println(v.(string))
	case []byte:
		fmt.Println(string(v.([]byte)))
	}
	p.Ip += 1
	return nil
}

func Exit(p *Process, args []any) error {
	a, _ := args[0].(json.Number).Int64()
	if a == 0 {
		os.Exit(0)
		return nil
	}
	p.Ip += 1
	return errors.New("")
}

func DecryptFile(p *Process, args []any) error {
	data := p.Registers[5].([]byte)
	key := p.Registers[6].([]byte)

	dec, err := DecryptData(data, []byte(key))
	if err != nil {
		p.Ip += 1
		return err
	}

	p.Registers[1] = dec
	p.Ip += 1
	return nil
}
