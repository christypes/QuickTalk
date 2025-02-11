package main

import (
	"fmt"
	"log"
	"net"
	"sync"
)

const (
	host     = "0.0.0.0"
	port     = "5000"
	buf_size = 1024
)

var (
	clients sync.Map
	// clientLock = sync.Mutex{}
)

func main() {
	// 1. Initializes the server with specified port.
	listener, err := net.Listen("tcp", ":"+port) // 0.0.0.0 by default (= all available interfaces)
	if err != nil {
		log.Fatalf("Error starting server: %v", err)
	}
	defer listener.Close()
	fmt.Println("The server is ready to receive")

	for {
		conn, err := listener.Accept()
		if err != nil {
			log.Printf("Error accepting connection: %v", err)
			continue
		}
		go handleClient(conn)
	}
}

func handleClient(conn net.Conn) {
	defer conn.Close()
	remoteAddr := conn.RemoteAddr().String()
	fmt.Printf("Connection with %s opened\n", remoteAddr)

	// 2. Add client to the list of active sessions
	clients.Store(conn, true) // CK: Internally locks/unlocks
	conn.Write([]byte("Hello! Welcome to QuickChat!\n"))

	buf := make([]byte, buf_size)
	for {
		n, err := conn.Read(buf)
		if err != nil {
			fmt.Printf("Client %s disconnected\n", conn.RemoteAddr().String())
			break
		}
		message := string(buf[:n])
		fmt.Printf("Message from %s: %s\n", conn.RemoteAddr().String(), message)
		broadcast(message, conn)
	}

	// 3. Remove from active connection when client closes the chat.
	clients.Delete(conn)
	fmt.Printf("Connection with %s closed\n", remoteAddr)
}

func broadcast(message string, sender net.Conn) {
	clients.Range(func(key, value interface{}) bool {
		client := key.(net.Conn) // var.T type assertion, panics if not true
		if client != sender {
			_, err := client.Write([]byte(message))
			if err != nil {
				log.Printf("Client %s unreachable, removing...", client.RemoteAddr().String())
				client.Close()
				clients.Delete(client)
			}
		}
		return true
	})
}
