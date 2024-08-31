package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"net"
	"net/http"
	"os"
	"strings"
	"sync"

	"github.com/joho/godotenv"
)

type EnvManager struct {
	EnvPath string
}

func (em *EnvManager) LoadEnv() {
	if err := godotenv.Load(em.EnvPath); err != nil {
		log.Fatalf("Error loading .env file")
	}
}

func (em *EnvManager) GetAPIKey() string {
	return os.Getenv("API_KEY")
}

type ChatGPTClient struct {
	APIKey  string
	URL     string
	Headers map[string]string
}

func NewChatGPTClient(apiKey string) *ChatGPTClient {
	return &ChatGPTClient{
		APIKey: apiKey,
		URL:    "https://adult-gpt.p.rapidapi.com/adultgpt",
		Headers: map[string]string{
			"x-rapidapi-key":  apiKey,
			"x-rapidapi-host": "adult-gpt.p.rapidapi.com",
			"Content-Type":    "application/json",
		},
	}
}

func (client *ChatGPTClient) GetResponse(message string, model string, maxTokens int, temperature float64, topK int, topP float64) (string, error) {
	payload := map[string]interface{}{
		"messages":    []map[string]string{{"role": "user", "content": message}},
		"genere":      "ai-gf-2",
		"bot_name":    "",
		"temperature": temperature,
		"top_k":       topK,
		"top_p":       topP,
		"max_tokens":  maxTokens,
	}

	jsonPayload, err := json.Marshal(payload)
	if err != nil {
		return "", err
	}

	req, err := http.NewRequest("POST", client.URL, strings.NewReader(string(jsonPayload)))
	if err != nil {
		return "", err
	}

	for key, value := range client.Headers {
		req.Header.Set(key, value)
	}

	httpClient := &http.Client{}
	resp, err := httpClient.Do(req)
	if err != nil {
		return "", err
	}
	defer resp.Body.Close()

	body, err := ioutil.ReadAll(resp.Body)
	if err != nil {
		return "", err
	}

	var result map[string]interface{}
	if err := json.Unmarshal(body, &result); err != nil {
		return "", err
	}

	return result["result"].(string), nil
}

type ChatServer struct {
	Host           string
	Port           string
	Clients        map[net.Conn]string
	EnvManager     *EnvManager
	APIKey         string
	ChatClient     *ChatGPTClient
	ServerListener net.Listener
	Mutex          sync.Mutex
}

func NewChatServer(host string, port string) *ChatServer {
	return &ChatServer{
		Host:       host,
		Port:       port,
		Clients:    make(map[net.Conn]string),
		EnvManager: &EnvManager{EnvPath: ".env"},
	}
}

func (server *ChatServer) HandleClient(conn net.Conn) {
	defer func() {
		server.Mutex.Lock()
		defer server.Mutex.Unlock()
		conn.Close()
		delete(server.Clients, conn)
	}()

	for {
		data := make([]byte, 1024)
		n, err := conn.Read(data)
		if err != nil {
			log.Println("Error reading from client:", err)
			return
		}
		if n == 0 {
			return
		}

		message := string(data[:n])
		if strings.Contains(message, ": ") {
			parts := strings.SplitN(message, ": ", 2)
			clientID := parts[0]
			clientMessage := parts[1]

			if clientMessage == "exit" || clientMessage == "" {
				server.Close()
				return
			}

			fmt.Printf("\033[35m%s: %s\033[0m\n", clientID, clientMessage)
			response, err := server.ChatClient.GetResponse(clientMessage, "gpt-4o", 100, 0.9, 2, 0.9)
			if err != nil {
				fmt.Println("Error getting response:", err)
				return
			}
			fmt.Printf("\033[36mServer: %s\033[0m\n", response)
			conn.Write([]byte(response))
		}
	}
}

func (server *ChatServer) Start() {
	server.EnvManager.LoadEnv()
	server.APIKey = server.EnvManager.GetAPIKey()
	server.ChatClient = NewChatGPTClient(server.APIKey)

	listener, err := net.Listen("tcp", fmt.Sprintf("%s:%s", server.Host, server.Port))
	if err != nil {
		log.Fatal("Error starting server:", err)
	}
	defer listener.Close()
	server.ServerListener = listener

	fmt.Println("Server started, waiting for connections...")
	for {
		conn, err := server.ServerListener.Accept()
		if err != nil {
			log.Println("Error accepting connection:", err)
			continue
		}

		server.Mutex.Lock()
		server.Clients[conn] = conn.RemoteAddr().String()
		server.Mutex.Unlock()

		go server.HandleClient(conn)
	}
}

func (server *ChatServer) Close() {
	server.ServerListener.Close()
}

func main() {
	server := NewChatServer("0.0.0.0", "6969")
	server.Start()
}
