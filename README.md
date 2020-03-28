# README

### Description

This project is a *Proof Of Concept* which shows how to store in database encrypted value in order to prevent leaked stolen data issue.

Two examples are in this project:
    
 * **OPE_Example** : script that will access a table in the DBMS, table where are stored name of users and their salaries (the salaries
 are encrypted with an OPE(*Order Preserving Encryption*), which allows intervals queries)
 
 * **HOMOMORPHIC_Example** : script that will access a table in the DBMS, table similar to the previous example,
 but where an another column has been added, where the salaries are encrypted with an homomorphic algorithm.<br/>
 This added encryption allows a client to transfer the encrypted data to a *simulated* middleware server
 which will be able to proceed to data calculations without having data's true contents


### How to run it ?

Run the script SQL in your *MySql* DBMS.

Then, run either the *OPE_Example.py* or the *HOMOMORPHIC_Example.py* script.
It will ask you the name and the password of the user you want to use.<br/>
(The script has created a new user you may use, but you still can use the *root* user)