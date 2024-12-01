# Quine-McCluskey-Implementation
By Joshua Joseph and Evan Chang

## About the Project
This repository contains our implementation of Quine McCluskey's Algorithm which is used to simplify boolean functions. Through a cyclical process of grouping, combining and elminating terms, the algorithm chooses the most optimal and minimal terms in order to represent the function. Our implementation receives input as a .pla file which contains the number of inputs, names of the input, and minterms of the boolean function. Once the input is received it is processed, the algorithm is run and the program outputs an .pla file with the minimized representation.
## Usage
To use the script, use the following command: `python3 main.py <input pla file> <output pla file>`
## Challenges
### '1111' Problem
One of the most significant challenges we encounted was a bug with our code resulting in the loss of any all '1' terms in the onset. This was a result of several issues. The first of which was that loop to check was not indexing correctly. Because of how we sorted terms and the fact that we were using lookahead in our loop, if the all 1 term was not able to be combined with a term in a previous loop, it would be completely lost. This was rectified by adding a flag in the loop to determine whether the all 1 term had been used and whether to add it to our terms or not.
### Updating Tables after Row and Column Domination
In this implementation, we created two dictionaries which mapped a minterm to a list of corresponding implicants and implicants to a list of corresponding minterms. When implementing column domination, this was done by iterating through the implicants to minterms dictionary and if one implicant's list of minterms was a sublist of another, then the sublist would be deleted along with the implicant tied to the sublist. This process easily allowed us to update the dictionary that mapped implicants to minterms but we wer having difficulty updating the minterm to implicant table within the column domination function. To resolve this, instead of updating the minterm to implicant table within the column domination function, we waited for the column domination function fully execute giving the final modified implicant to minterm table and then used this final table to reconstruct the minterm to implicant table. Although this created some redundant functions, it made it much easier to visualize and understand what was going on the program.
### Don't Care Inputs
Initially, all inputs were treated the same which resulted in unintended behavior. 
### Indexing Issues
Several bugs arose because of my misunderstanding of the slicing behavior in python, as I mistakenly tried to access data that did not exist in some edge cases. This was corrected by adding several validation checks before trying to make an access.
## Verification
To verify the functionality of our implementation, we designed a test suite of varying different cases. Doing this allowed for edge cases in our code to be exercised and test. When problems came up would diagnose the code and fix it accordingly. To run the test suite, clone the repo. Then from within the repo, run the command `./testSuite.sh`. Doing so will automatically run 8 tests and compare the results with a validation output. Upon testing, the test suite revealed several bugs which have now been rectified.