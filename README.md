# Splitwise_API
Application is developed using Django Rest Framework.

The  main components are:  
Request -> URLs/Routers -> Serializers ->views -> Models  

![image](https://github.com/byRahulJain/Splitwise_API/assets/42427031/a2fccb96-5888-4325-b0c3-0b4fe200c5a5)

                                  
## Models :
The main models are:  
UserProfile - Stores user information  
Expense - Stores information about an expense like amount, type etc.  Links to User model  
ExpenseParticipant - Stores details of participation for each user in an expense.  Links to Expense and User model.  

## Views
The main views are:
ExpenseViewSet - Provides CRUD endpoints for Expense  
ExpenseParticipantViewSet - Read only viewset for ExpenseParticipant  
user_balances - Returns net balances for a user  
all_user_balances - Returns net balances for all users  

## API Contract
The API endpoints are:

### Expenses
GET /expenses/ - Get list of expenses  
POST /expenses/ - Create new expense  
&nbsp;&nbsp;&nbsp;&nbsp;Request Body:  
&nbsp;&nbsp;&nbsp;&nbsp;For exact : ``` 
{
  "added_by": "u1",
  "amount": 1250,
  "type": "Ex",
  "participants": [
    {"username": "u2", "amount": 370},
    {"username": "u3", "amount": 880}
  ]
} ```

GET /expenses/:id/ - Get expense by id  
PUT /expenses/:id/ - Update expense  
DELETE /expenses/:id/ - Delete expense  

### Expense Participants
GET /participants/ - Get all participants  
GET /participants/:id/ - Get participant by id  

### User Balances
GET /balances/:username/ - Get balances for user  
GET /balances/ - Get balances for all users  
