package main

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/ecdh"
	"crypto/rand"
	"errors"
	"fmt"
	"io"
)

func GenKeys() error {
	curve := ecdh.P256()

	privKey, err := curve.GenerateKey(rand.Reader)
	if err != nil {
		return err
	}
	ServerPrivKey = privKey
	ServerPubKey = ServerPrivKey.PublicKey()

	return nil
}

func ComputeSecret(clientPubKeyBytes []byte) ([]byte, error) {
	curve := ecdh.P256()

	clientPubKey, err := curve.NewPublicKey(clientPubKeyBytes)
	if err != nil {
		return nil, err
	}
	secret, err := ServerPrivKey.ECDH(clientPubKey)
	if err != nil {
		fmt.Println(err)
		return nil, err
	}
	return secret, nil
}

func EncryptData(plain, key []byte) ([]byte, error) {
	c, err := aes.NewCipher(key)
	if err != nil {
		return nil, err
	}
	gcm, err := cipher.NewGCM(c)
	if err != nil {
		return nil, err
	}
	// always make sure that the nonce is different at each encryption for a given key
	nonce := make([]byte, gcm.NonceSize())
	if _, err = io.ReadFull(rand.Reader, nonce); err != nil {
		return nil, err
	}
	return gcm.Seal(nonce, nonce, plain, nil), nil
}

func DecryptData(enc, key []byte) ([]byte, error) {

	c, err := aes.NewCipher(key)
	if err != nil {
		return nil, err
	}
	gcm, err := cipher.NewGCM(c)
	if err != nil {
		return nil, err
	}
	nonceSize := gcm.NonceSize()
	if len(enc) < nonceSize {
		return nil, errors.New("Wrong cipher size")
	}

	nonce, ciphertext := enc[:nonceSize], enc[nonceSize:]
	plain, err := gcm.Open(nil, nonce, ciphertext, nil)
	if err != nil {
		return nil, err
	}

	return plain, err
}
