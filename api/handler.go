package api

import (
	"encoding/json"
	"fmt"
	"net/http"

	"github.com/gorilla/mux"
	"github.com/YOUR-USERNAME/YOUR-REPO/chaincode" // Import your chaincode package
)

// APIHandler represents the API handler struct
type APIHandler struct {
	SmartContract *chaincode.SmartContract
}

// Init initializes the API routes and handlers
func (ah *APIHandler) Init() *mux.Router {
	r := mux.NewRouter()
	r.HandleFunc("/accounts", ah.GetAllAccounts).Methods("GET")
	r.HandleFunc("/accounts/{id}", ah.GetAccountByID).Methods("GET")
	r.HandleFunc("/accounts", ah.CreateAccount).Methods("POST")
	r.HandleFunc("/accounts/{id}", ah.UpdateAccount).Methods("PUT")
	r.HandleFunc("/accounts/{id}", ah.DeleteAccount).Methods("DELETE")
	r.HandleFunc("/transfer", ah.TransferFunds).Methods("POST")
	return r
}

// GetAllAccounts handles the GET request to retrieve all accounts
func (ah *APIHandler) GetAllAccounts(w http.ResponseWriter, r *http.Request) {
	accounts, err := ah.SmartContract.GetAllAccounts()
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	jsonResponse(w, accounts)
}

// GetAccountByID handles the GET request to retrieve an account by ID
func (ah *APIHandler) GetAccountByID(w http.ResponseWriter, r *http.Request) {
	params := mux.Vars(r)
	id := params["id"]

	account, err := ah.SmartContract.ReadAccount(id)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	if account == nil {
		http.NotFound(w, r)
		return
	}

	jsonResponse(w, account)
}

// CreateAccount handles the POST request to create a new account
func (ah *APIHandler) CreateAccount(w http.ResponseWriter, r *http.Request) {
	var account chaincode.Account
	err := json.NewDecoder(r.Body).Decode(&account)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	err = ah.SmartContract.CreateAccount(account.ID, account.Owner, account.Balance)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusCreated)
	jsonResponse(w, account)
}

// UpdateAccount handles the PUT request to update an existing account
func (ah *APIHandler) UpdateAccount(w http.ResponseWriter, r *http.Request) {
	var account chaincode.Account
	err := json.NewDecoder(r.Body).Decode(&account)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	params := mux.Vars(r)
	id := params["id"]

	err = ah.SmartContract.UpdateAccount(id, account.Owner, account.Balance)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	jsonResponse(w, account)
}

// DeleteAccount handles the DELETE request to delete an account
func (ah *APIHandler) DeleteAccount(w http.ResponseWriter, r *http.Request) {
	params := mux.Vars(r)
	id := params["id"]

	err := ah.SmartContract.DeleteAccount(id)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusNoContent)
}

// TransferFunds handles the POST request to transfer funds between accounts
func (ah *APIHandler) TransferFunds(w http.ResponseWriter, r *http.Request) {
	type transferRequest struct {
		FromID string  `json:"fromID"`
		ToID   string  `json:"toID"`
		Amount float64 `json:"amount"`
	}

	var request transferRequest
	err := json.NewDecoder(r.Body).Decode(&request)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	err = ah.SmartContract.TransferFunds(request.FromID, request.ToID, request.Amount)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusOK)
}

// Helper function to send JSON response
func jsonResponse(w http.ResponseWriter, data interface{}) {
	w.Header().Set("Content-Type", "application/json")
	err := json.NewEncoder(w).Encode(data)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
	}
}
