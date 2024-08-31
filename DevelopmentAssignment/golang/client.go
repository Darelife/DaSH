package main

import (
	"bufio"
	"encoding/json"
	"fmt"
	"math/rand"
	"net"
	"os"
	"time"
)

type Output struct {
	Prompt    string  `json:"Prompt"`
	Message   string  `json:"Message"`
	TimeSent  float64 `json:"TimeSent"`
	TimeRecvd float64 `json:"TimeRecvd"`
	Source    string  `json:"Source"`
}

func main() {
	port := 6969
	server := "localhost" // Adjust as needed
	clientID := rand.Intn(1000) + 1
	output := []Output{}

	// Connect to server
	conn, err := net.Dial("tcp", fmt.Sprintf("%s:%d", server, port))
	if err != nil {
		fmt.Println("Error connecting to server:", err)
		return
	}
	defer conn.Close()

	// Open input file
	file, err := os.Open("input.txt")
	if err != nil {
		fmt.Println("Error opening input file:", err)
		return
	}
	defer file.Close()

	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		message := scanner.Text()
		formattedMessage := fmt.Sprintf("%d: %s", clientID, message)

		start := time.Now().UnixNano() / int64(time.Millisecond)
		_, err := fmt.Fprintf(conn, "%s\n", formattedMessage)
		if err != nil {
			fmt.Println("Error sending message:", err)
			return
		}

		buffer := make([]byte, 1024)
		n, err := conn.Read(buffer)
		if err != nil {
			fmt.Println("Error reading response:", err)
			return
		}

		response := string(buffer[:n])
		fmt.Printf("\033[36mServer: %s\033[0m\n", response)

		end := time.Now().UnixNano() / int64(time.Millisecond)
		output = append(output, Output{
			Prompt:    message,
			Message:   response,
			TimeSent:  float64(start),
			TimeRecvd: float64(end),
			Source:    "AdultGPT",
		})
	}

	// Handle scanner errors
	if err := scanner.Err(); err != nil {
		fmt.Println("Error reading from file:", err)
	}

	// Write output to JSON file
	outputFile, err := os.Create("output.json")
	if err != nil {
		fmt.Println("Error creating output file:", err)
		return
	}
	defer outputFile.Close()

	encoder := json.NewEncoder(outputFile)
	encoder.SetIndent("", "  ")
	if err := encoder.Encode(output); err != nil {
		fmt.Println("Error writing JSON to file:", err)
	}

	// Send exit message
	formattedMessage := fmt.Sprintf("%d: exit", clientID)
	_, err = fmt.Fprintf(conn, "%s\n", formattedMessage)
	if err != nil {
		fmt.Println("Error sending exit message:", err)
		return
	}
}
