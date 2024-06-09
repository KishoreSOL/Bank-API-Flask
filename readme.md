# Money Management API

## Overview
The Money Management API is a RESTful service built with Flask and MongoDB, allowing users to manage their finances. Users can register, add funds, transfer money, check balances, take loans, and repay loans.

## Key Features
- **User Registration**
- **Add Funds**
- **Transfer Funds**
- **Check Balance**
- **Take Loan**
- **Repay Loan**

## API Endpoints

### 1. Register
- **Endpoint**: `/register`
- **Method**: POST
- **Body**:
  ```json
  {
      "username": "your_username",
      "password": "your_password"
  }
  ```
- **Response**:
  ```json
  {
      "status": 200,
      "msg": "You successfully signed up for the API"
  }
  ```

### 2. Add Funds
- **Endpoint**: `/add`
- **Method**: POST
- **Body**:
  ```json
  {
      "username": "your_username",
      "password": "your_password",
      "amount": amount_to_add
  }
  ```
- **Response**:
  ```json
  {
      "status": 200,
      "msg": "Amount Added Successfully"
  }
  ```

### 3. Transfer Funds
- **Endpoint**: `/transfer`
- **Method**: POST
- **Body**:
  ```json
  {
      "username": "your_username",
      "password": "your_password",
      "to": "recipient_username",
      "amount": amount_to_transfer
  }
  ```
- **Response**:
  ```json
  {
      "status": 200,
      "msg": "Amount Transferred Successfully"
  }
  ```

### 4. Check Balance
- **Endpoint**: `/balance`
- **Method**: POST
- **Body**:
  ```json
  {
      "username": "your_username",
      "password": "your_password"
  }
  ```
- **Response**:
  ```json
  {
      "Username": "your_username",
      "Own": current_balance,
      "Debt": current_debt
  }
  ```

### 5. Take a Loan
- **Endpoint**: `/takeloan`
- **Method**: POST
- **Body**:
  ```json
  {
      "username": "your_username",
      "password": "your_password",
      "amount": loan_amount
  }
  ```
- **Response**:
  ```json
  {
      "status": 200,
      "msg": "Loan Added to Your Account"
  }
  ```

### 6. Repay Loan
- **Endpoint**: `/payloan`
- **Method**: POST
- **Body**:
  ```json
  {
      "username": "your_username",
      "password": "your_password",
      "amount": repayment_amount
  }
  ```
- **Response**:
  ```json
  {
      "status": 200,
      "msg": "Loan Repaid"
  }
  ```

## How to Run

1. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

2. **Start the API**:
   ```sh
   python app.py
   ```
   Access the API at `http://0.0.0.0:5000`.

## Notes
- Ensure MongoDB is running and accessible at `mongodb://db:27017`.
- Initialize the "BANK" account with sufficient funds for transaction fees.

## License
Licensed under the MIT License.

---

This README provides a concise overview of the Money Management API, covering its main features and usage instructions.