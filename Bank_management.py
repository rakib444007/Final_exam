from abc import ABC,abstractmethod


class Bank:

    def __init__(self,name) -> None:
        self.name = name
        self.__Bankamount = 1000000
        
    def get_bank_balance(self):
        return self.__Bankamount
    def get_loan(self,amount):
        if amount > 0:
            
            self.__Bankamount -= amount
            return amount


class User(ABC):

    def __init__(self,name,email,address,acc_type) -> None:
        self.name = name
        self.email = email
        self.address  = address
        self.acc_type = acc_type
        self.acc_number = None

    @abstractmethod
    def deposit(self):
        pass
    @abstractmethod
    def withdraw(self):
        pass
    


    
class Account(User):

    def __init__(self, name, email, address, acc_type) -> None:
        super().__init__(name, email, address, acc_type)
        self.transactions  = []
        self.loan = 0
        self.total_loan_count = 0
        self.is_bankrupt = False
        self.acc_number = name + email
        self.__balance = 0
        
    @property
    def balance(self):
        return self.__balance
    def get_transactions(self):
        if self.is_bankrupt == True:
            print('The bank is bankrupt!')
            return
        return self.transactions
    
    def get_balance(self):
        if self.is_bankrupt == True:
            print('The bank is bankrupt!')
            return
        return f'your balance is : {self.__balance}'
    
    def deposit(self,amount):
        if self.is_bankrupt == True:
            print('The bank is bankrupt!')
            return
        if amount > 0:

            self.__balance += amount
            self.transactions.append(f'deposit: {amount}')
            return f'{amount} amount deposit successfully'
        else:
            return 'Your amount is less than zero'
    def withdraw(self,amount):
        if self.is_bankrupt == True:
            print('The bank is bankrupt!')
            return
        if amount > self.__balance:
            print('Withdrawal amount exceeded!\n')
        else:

            self.__balance -= amount
            self.transactions.append(f'withdraw : {amount}')
            print('\n')
            print(f'Your withdraw  amount is : {amount}')
            print(f'Now your current balance is :{self.__balance}\n')

    def transfer_amount(self,nebers_acc_number,amount,admin):#take admin object and nebers_acc
        if self.is_bankrupt == True:
            print('The bank is bankrupt!\n')
            return
        if amount > self.__balance:
            print('Withdrawal amount exceeded!\n')
            return
        
        
        if nebers_acc_number  in admin.accounts:
            admin.accounts[nebers_acc_number].deposit(amount)
            self.__balance -= amount
            self.transactions.append(f'TransferedAmount: {amount}')
            print(f'Transferred {amount} to {nebers_acc_number} successfully\n')
            
        else:
            print('Account does not exist!!\n')

    def get_loan(self,amount,admin,bank):
        if self.is_bankrupt == True:
            print('The bank is bankrupt!\n')
            return
        if amount < 0:
            print('Amount less than zero!')
            return 
        if  self.total_loan_count >= 2:
            print('You can not get a Lone. Because Loan limit Exceeded!!\n')
            return
        else:
            self.__balance += admin.give_loan(amount,bank)
            self.total_loan_count += 1
            self.loan += amount
            self.transactions.append(f'LonaTake: {amount}')
            print(f'Loan {amount} taken successfully\n')




class Admin:

    def __init__(self,name,password):
        self.name = name
        self.password = password
        self.accounts = {} #{"account_number":account_object}
        self.loan_feature = True


    def create_new_account(self,name,email,address,account_type): #give a user object
        acc = Account(name=name,email=email,address=address,acc_type=account_type)
        self.accounts[acc.acc_number] = acc
        print('\n')
        print('Account create successfully\n')
        
        
    
    def delete_account(self,acc_number): #give a account number
        if acc_number in self.accounts:
            del self.accounts[acc_number]
            print(f'{acc_number} number account deleted successfully\n')
        else:
            print('\n')
            print('Account does not exist!\n')


    def show_acc_list(self):
        if not self.accounts:
            print('Account list is empty!\n')
            return
        
        for key,value in self.accounts.items():
            print('-----------------------------------------------------')
            print(f'AccountNumber: {key}\nName: {value.name}\nEmail: {value.email}\nAddress: {value.address}\nAccount_type: {value.acc_type}')
            print('-----------------------------------------------------')     
        print('\n')      

    def  total_available_balance(self,bank):
        balance = sum(account.balance for account in self.accounts.values())
        print(f'Total available balance is : {balance + bank.get_bank_balance()}\n')
    

    def total_loan_amount(self):
        loan = sum(account.loan for account in self.accounts.values())
        print(f'Total loan amount is : {loan}\n')

    def give_loan(self,amount,bank):
        if self.loan_feature == True and amount > 0:
            taka = bank.get_loan(amount=amount)
            return taka


Brac = Bank('Brac Bank')
admin = Admin('admin','123')


def admin_section():
    #admin password is : '123' and admin name is : 'admin'
    name = str(input('Enter admin name: '))
    password = str(input('Enter admin password:'))
     
    if password in admin.password and name in admin.name:
        print('-------------------------------')
        print('Welcome admin')
        print('-------------------------------')  
        while True:
            
            print('1. Create a new account. ')
            print('2. Show account list.')
            print('3. Show total available balance. ')
            print('4. Show total loan amount. ')
            print('5. Delete account. ')
            print('6. Exit.')

            op = int(input('Enter your choise: '))
            if op == 1:
                name = input('Enter your name: ')
                email = input('Enter your email: ')
                address = input('Enter your address: ')
                acc_type = input('Enter your account type: ')
                admin.create_new_account(name,email,address,acc_type)
            
            elif op == 2:
                admin.show_acc_list()
            elif op == 3:
                admin.total_available_balance(Brac)
            elif op == 4:
                admin.total_loan_amount()
            elif op == 5:
                acc_number = str(input('Enter account number: '))
                admin.delete_account(acc_number=acc_number)

            elif op == 6:
                break
            else:
                print('Invalid choise.Try again !!')
    else:
        print('Wrong name or password.You can try again!!')

 
def user_section():

    acc_number =str(input('Enter your account number : '))

    if acc_number in admin.accounts:
        user = admin.accounts[acc_number]
        print('\n')
        while True:

            print('1. Deposit money. ')
            print('2. Withdraw money.')
            print('3. Show transaction history.')
            print('4. Show account balance.')
            print('5. Transfer amount.')
            print('6. Take loan.')
            print('7. Exit')

            op = int(input('Enter your choise: '))
           
            
            if op == 1:
                amount = int(input('Enter your amount: '))
                print(user.deposit(amount))
            elif  op == 2:
                amount = int(input('Enter your amount: '))
                user.withdraw(amount)
            elif op == 3:
                print(user.get_transactions())
            elif op == 4:
                print(user.get_balance())
            elif op == 5:
                acc_number = str(input('Enter account number: '))
                amount = int(input('Enter your amount: '))
                user.transfer_amount(acc_number,amount,admin)
            elif op == 6:
                amount = int(input('Enter your amount: '))
                user.get_loan(amount,admin,Brac)
            elif op == 7:
                break
            else:
                print('Invalid choise.Try again !!')
    else:
        print(f'This number of account: {acc_number} can not exist.You can try again!!')

    

while True:
    print('Welcome to our Bank!')
    print('-----------------------')
    print('Choise your option')
    print('-----------------------')
    print('1. Admin')
    print('2. User')
    print('3. Exit')

    op = int(input('Enter your choise: '))
    if op == 1:
        admin_section()
    elif op == 2:
        user_section()
    elif op == 3:
        break
    else:
        print('Invaid choise!!')





