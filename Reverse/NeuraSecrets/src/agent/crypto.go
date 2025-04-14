package main

import (
	"encoding/binary"
)

const (
	// Constants for MD5 transform routine.
	s11, s12, s13, s14 = 7, 12, 17, 22
	s21, s22, s23, s24 = 5, 9, 14, 20
	s31, s32, s33, s34 = 4, 11, 16, 23
	s41, s42, s43, s44 = 6, 10, 15, 21
)

// F, G, H, I are non-linear functions used in MD5 rounds.
func F(x, y, z uint32) uint32 { return (x & y) | (^x & z) }
func G(x, y, z uint32) uint32 { return (x & z) | (y & ^z) }
func H(x, y, z uint32) uint32 { return x ^ y ^ z }
func I(x, y, z uint32) uint32 { return y ^ (x | ^z) }

// RotateLeft rotates `x` left by `n` bits.
func RotateLeft(x, n uint32) uint32 {
	return (x << n) | (x >> (32 - n))
}

// MD5Block processes a single 512-bit block.
func MD5Block(block []byte, a, b, c, d uint32) (uint32, uint32, uint32, uint32) {
	var x [16]uint32
	for i := range x {
		x[i] = binary.LittleEndian.Uint32(block[i*4:])
	}

	aa, bb, cc, dd := a, b, c, d

	// Round 1
	a = b + RotateLeft(a+F(b, c, d)+x[0]+0xd76aa478, s11)
	d = a + RotateLeft(d+F(a, b, c)+x[1]+0xe8c7b756, s12)
	c = d + RotateLeft(c+F(d, a, b)+x[2]+0x242070db, s13)
	b = c + RotateLeft(b+F(c, d, a)+x[3]+0xc1bdceee, s14)

	a = b + RotateLeft(a+F(b, c, d)+x[4]+0xf57c0faf, s11)
	d = a + RotateLeft(d+F(a, b, c)+x[5]+0x4787c62a, s12)
	c = d + RotateLeft(c+F(d, a, b)+x[6]+0xa8304613, s13)
	b = c + RotateLeft(b+F(c, d, a)+x[7]+0xfd469501, s14)

	a = b + RotateLeft(a+F(b, c, d)+x[8]+0x698098d8, s11)
	d = a + RotateLeft(d+F(a, b, c)+x[9]+0x8b44f7af, s12)
	c = d + RotateLeft(c+F(d, a, b)+x[10]+0xffff5bb1, s13)
	b = c + RotateLeft(b+F(c, d, a)+x[11]+0x895cd7be, s14)

	a = b + RotateLeft(a+F(b, c, d)+x[12]+0x6b901122, s11)
	d = a + RotateLeft(d+F(a, b, c)+x[13]+0xfd987193, s12)
	c = d + RotateLeft(c+F(d, a, b)+x[14]+0xa679438e, s13)
	b = c + RotateLeft(b+F(c, d, a)+x[15]+0x49b40821, s14)

	// Round 2
	a = b + RotateLeft(a+G(b, c, d)+x[1]+0xf61e2562, s21)
	d = a + RotateLeft(d+G(a, b, c)+x[6]+0xc040b340, s22)
	c = d + RotateLeft(c+G(d, a, b)+x[11]+0x265e5a51, s23)
	b = c + RotateLeft(b+G(c, d, a)+x[0]+0xe9b6c7aa, s24)

	a = b + RotateLeft(a+G(b, c, d)+x[5]+0xd62f105d, s21)
	d = a + RotateLeft(d+G(a, b, c)+x[10]+0x02441453, s22)
	c = d + RotateLeft(c+G(d, a, b)+x[15]+0xd8a1e681, s23)
	b = c + RotateLeft(b+G(c, d, a)+x[4]+0xe7d3fbc8, s24)

	a = b + RotateLeft(a+G(b, c, d)+x[9]+0x21e1cde6, s21)
	d = a + RotateLeft(d+G(a, b, c)+x[14]+0xc33707d6, s22)
	c = d + RotateLeft(c+G(d, a, b)+x[3]+0xf4d50d87, s23)
	b = c + RotateLeft(b+G(c, d, a)+x[8]+0x455a14ed, s24)

	a = b + RotateLeft(a+G(b, c, d)+x[13]+0xa9e3e905, s21)
	d = a + RotateLeft(d+G(a, b, c)+x[2]+0xfcefa3f8, s22)
	c = d + RotateLeft(c+G(d, a, b)+x[7]+0x676f02d9, s23)
	b = c + RotateLeft(b+G(c, d, a)+x[12]+0x8d2a4c8a, s24)

	// Round 3
	a = b + RotateLeft(a+H(b, c, d)+x[5]+0xfffa3942, s31)
	d = a + RotateLeft(d+H(a, b, c)+x[8]+0x8771f681, s32)
	c = d + RotateLeft(c+H(d, a, b)+x[11]+0x6d9d6122, s33)
	b = c + RotateLeft(b+H(c, d, a)+x[14]+0xfde5380c, s34)

	a = b + RotateLeft(a+H(b, c, d)+x[1]+0xa4beea44, s31)
	d = a + RotateLeft(d+H(a, b, c)+x[4]+0x4bdecfa9, s32)
	c = d + RotateLeft(c+H(d, a, b)+x[7]+0xf6bb4b60, s33)
	b = c + RotateLeft(b+H(c, d, a)+x[10]+0xbebfbc70, s34)

	a = b + RotateLeft(a+H(b, c, d)+x[13]+0x289b7ec6, s31)
	d = a + RotateLeft(d+H(a, b, c)+x[0]+0xeaa127fa, s32)
	c = d + RotateLeft(c+H(d, a, b)+x[3]+0xd4ef3085, s33)
	b = c + RotateLeft(b+H(c, d, a)+x[6]+0x04881d05, s34)

	a = b + RotateLeft(a+H(b, c, d)+x[9]+0xd9d4d039, s31)
	d = a + RotateLeft(d+H(a, b, c)+x[12]+0xe6db99e5, s32)
	c = d + RotateLeft(c+H(d, a, b)+x[15]+0x1fa27cf8, s33)
	b = c + RotateLeft(b+H(c, d, a)+x[2]+0xc4ac5665, s34)

	// Round 4
	a = b + RotateLeft(a+I(b, c, d)+x[0]+0xf4292244, s41)
	d = a + RotateLeft(d+I(a, b, c)+x[7]+0x432aff97, s42)
	c = d + RotateLeft(c+I(d, a, b)+x[14]+0xab9423a7, s43)
	b = c + RotateLeft(b+I(c, d, a)+x[5]+0xfc93a039, s44)

	a = b + RotateLeft(a+I(b, c, d)+x[12]+0x655b59c3, s41)
	d = a + RotateLeft(d+I(a, b, c)+x[3]+0x8f0ccc92, s42)
	c = d + RotateLeft(c+I(d, a, b)+x[10]+0xffeff47d, s43)
	b = c + RotateLeft(b+I(c, d, a)+x[1]+0x85845dd1, s44)

	a = b + RotateLeft(a+I(b, c, d)+x[8]+0x6fa87e4f, s41)
	d = a + RotateLeft(d+I(a, b, c)+x[15]+0xfe2ce6e0, s42)
	c = d + RotateLeft(c+I(d, a, b)+x[6]+0xa3014314, s43)
	b = c + RotateLeft(b+I(c, d, a)+x[13]+0x4e0811a1, s44)

	a = b + RotateLeft(a+I(b, c, d)+x[4]+0xf7537e82, s41)
	d = a + RotateLeft(d+I(a, b, c)+x[11]+0xbd3af235, s42)
	c = d + RotateLeft(c+I(d, a, b)+x[2]+0x2ad7d2bb, s43)
	b = c + RotateLeft(b+I(c, d, a)+x[9]+0xeb86d391, s44)

	// Update the state with the result of this block.
	a += aa
	b += bb
	c += cc
	d += dd

	return a, b, c, d
}

// MD5 is the main function to compute an MD5 hash.
func MD5(message []byte) []byte {
	// Initialize MD5 buffers
	var a, b, c, d uint32 = 0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476

	// Padding the message
	msgLen := uint64(len(message) * 8)
	message = append(message, 0x80)
	for len(message)%64 != 56 {
		message = append(message, 0x00)
	}

	// Append length (in bits)
	var lenBytes [8]byte
	binary.LittleEndian.PutUint64(lenBytes[:], msgLen)
	message = append(message, lenBytes[:]...)

	// Process the message in 512-bit (64-byte) chunks.
	for i := 0; i < len(message); i += 64 {
		a, b, c, d = MD5Block(message[i:i+64], a, b, c, d)
	}

	// Produce the final digest as a 16-byte array.
	var digest [16]byte
	binary.LittleEndian.PutUint32(digest[0:], a)
	binary.LittleEndian.PutUint32(digest[4:], b)
	binary.LittleEndian.PutUint32(digest[8:], c)
	binary.LittleEndian.PutUint32(digest[12:], d)

	return digest[:]
}
