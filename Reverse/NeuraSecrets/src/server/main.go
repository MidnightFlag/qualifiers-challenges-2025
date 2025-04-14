package main

import (
	"bytes"
	"crypto/ecdh"
	"crypto/md5"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"sync"
)

type Shellcode []Instruction

type Instruction struct {
	Opcode string
	Args   []any
}

func generateShellcode(fileName string) []byte {
	// url := "http://localhost:8080/res"
	shellcode, err := Parse("shellcodes/" + fileName)
	if err != nil {
		panic(err)
	}
	buf := new(bytes.Buffer)
	json.NewEncoder(buf).Encode(shellcode)

	return buf.Bytes()
}

var (
	ServerPubKey      *ecdh.PublicKey
	ServerPrivKey     *ecdh.PrivateKey
	SharedSecret      []byte
	ClientPubKeyBytes []byte
	finalKey          = "key_gymclasshero"
	clientSecrets     sync.Map
)

func main() {
	err := GenKeys()
	if err != nil {
		fmt.Println(err)
	}

	file, err := os.ReadFile("flag.txt")
	if err != nil {
		panic(err)
	}

	enc, err := EncryptData(file, []byte(finalKey))
	if err != nil {
		panic(err)
	}

	fileEnc, err := os.Create("flag.txt.enc")
	if err != nil {
		panic(err)
	}

	_, err = fileEnc.Write(enc)
	if err != nil {
		panic(err)
	}

	server := http.NewServeMux()

	server.HandleFunc("GET /shellcode/main", func(w http.ResponseWriter, r *http.Request) {
		fmt.Println("Agent fetched shellcode.ma")
		w.Write(generateShellcode("shellcode.ma"))
	})
	server.HandleFunc("GET /shellcode/check", func(w http.ResponseWriter, r *http.Request) {
		fmt.Println("Agent fetched check.ma")
		shellcodePlain := generateShellcode("check-key.ma")

		secret, _ := clientSecrets.Load(r.RemoteAddr)

		shellcodeEnc, err := EncryptData(shellcodePlain, secret.([]byte))
		if err != nil {
			panic(err)
		}
		w.Write(shellcodeEnc)
	})

	server.HandleFunc("POST /res", func(w http.ResponseWriter, r *http.Request) {
		fmt.Println("Shellcode response endpoint")

		bodyBytes, err := io.ReadAll(r.Body)
		if err != nil {
			fmt.Println(err)
		}

		secret, _ := clientSecrets.Load(r.RemoteAddr)

		valueDec, err := DecryptData(bodyBytes, secret.([]byte))
		if err != nil {
			return
		}
		fmt.Println(string(valueDec))
		w.Write([]byte("Shellcode response endpoint"))
	})

	server.HandleFunc("GET /pub", func(w http.ResponseWriter, r *http.Request) {
		w.Write(ServerPubKey.Bytes())
	})

	server.HandleFunc("POST /pub", func(w http.ResponseWriter, r *http.Request) {
		clientKey, err := io.ReadAll(r.Body)
		if err != nil {
			fmt.Println(err)
		}

		secret, err := ComputeSecret(clientKey)
		if err != nil {
			w.WriteHeader(401)
			return
		}
		fmt.Println("Successfully generated shared secret")

		ip := r.RemoteAddr
		clientSecrets.Store(ip, secret)
	})

	server.HandleFunc("GET /key", func(w http.ResponseWriter, r *http.Request) {
		keyMD5 := md5.Sum([]byte(finalKey))
		secret, _ := clientSecrets.Load(r.RemoteAddr)
		keyEnc, err := EncryptData(keyMD5[:], secret.([]byte))
		if err != nil {
			fmt.Println(err)
			return
		}
		w.Write(keyEnc)
	})

	http.ListenAndServe(":10000", server)
}
