# Quine-McCluskey-Implementation
By Joshua Joseph and Evan Chang
## Usage
To use the script, use the following command: `python3 main.py <input pla file> <output pla file>`
## Challenges
### '1111' Problem
One of the most significant challenges we encounted was a bug with our code resulting in the loss of any all '1' terms in the onset. This was a result of several issues. The first of which was that loop to check was not indexing correctly. Because of how we sorted terms and the fact that we were using lookahead in our loop, if the all 1 term was not able to be combined with a term in a previous loop, it would be completely lost. This was rectified by adding a flag in the loop to determine whether the all 1 term had been used and whether to add it to our terms or not.
### Don't Care Inputs
Initially, all inputs were treated the same which resulted in unintended behavior. 
## Verification
To verify the functionality of our implementation, we designed a test suite of varying different cases. To run the test suite, clone the repo. Then from within the repo, run the command `./testSuite.sh`. Doing so will automatically run 7 tests and compare the results with a validation output. Upon testing, the test suite revealed several bugs which have now been rectified.