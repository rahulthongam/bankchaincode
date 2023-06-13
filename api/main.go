package main

import (
	"log"
	"net/http"

	"github.com/gorilla/mux"
	"github.com/rahulthongam/bankchaincode/chaincode" // Import your chaincode package
	"github.com/rahulthongam/bankchaincode/api" // Import your API package
)

func main() {
	// Create an instance of the smart contract
	smartContract := new(chaincode.SmartContract)

	// Initialize the API handler with the smart contract instance
	apiHandler := api.APIHandler{
		SmartContract: smartContract,
	}

	// Initialize the API routes and handlers
	router := apiHandler.Init()

	// Start the server
	log.Println("Server listening on port 8080...")
	log.Fatal(http.ListenAndServe(":8080", router))
}
