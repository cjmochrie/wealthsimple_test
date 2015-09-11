 rebalance.py
 Cameron Mochrie
 
  **Usage:**
 
  From the command line:
  $ python rebalance.py test_files/portfolio.csv
  
  1) Will load the command line argument .csv file.
  2) Create Position objects and populate a Portfolio object.
  3) Print out the Portfolio object.
  4) Run rebalance() on the Portfolio object and return a list of instructions in the form: 
    'Instruction(ticker='GOOG', instruction='Buy 9 shares of GOOG')'. These instructions will be made to most closely
    match the actual portfolio to the target portfolio by transacting round-numbers of shares.
    
   **Testing:**
   
   Tests can be run from the command line:
   $ python -m unittest testing.py
   
   This runs a series of 6 tests across 7 .csv files to verify that instructions generated are correct, and various 
   invalid input exceptions or warnings are raised.
   
   **Technical Choices:**
   
   Using a .csv file as the input format seemed to me to be a sensible choice, as it is easy to output from Excel
   which would be a natural source for defining target allocations and position lists.
   
   Both Portfolios and Positions are represented as objects. This may be overkill for Positions, but I did it this
   way to encapsulate a lot of error handling. If speed is of concern then obviously a simple tuple or named
   tuple could serve just as well.
   
   I felt defining a Portfolio class is a more obvious choice. It allows for easy extensibility, and is well suited
    to being adapted to a table definition for permanent storage in a relational database.
    
   Instructions are simple strings to match the spec output requirements. To extend this functionality I would include
   additional fields that could be machine readable (trade type, shares transacted etc).
     
  **Additional Functionality:**
  
  The rebalancing logic is very limited at the moment. Natural extensions would include: ensure net cash change over
   the transactions is not negative (or not positive) or enforcing a minimum trade size.
   
   Obviously more would need to be done to make these Portfolio objects *able* to rebalance and not just emit 
   instructions such as handle trade instructions and so on.
   
  Portfolio persistence - modify the Portfolio class to define a relational database table (SQLAlchemy is what I know,
  and where I would likely go to implement this).
  
  **Testing:**
  
  The testing suite for rebalance.py is limited owing to the simplicity of the overall functionality. I did try and 
  include validation of the instructions generated, and basic error handling for likely errors in .csv construction.
  
  One weakness of the tests I wrote are that they are difficult to update if functionality is changed. For example if
  Exception messages, or Instruction output is reformatted, the tests will also have to be reformatted. They do not 
  as a whole generalize over any input data. Ie; I didn't write any tests that check that a set of instructions 
  results in minimal net change in cash. This seemed a little arbitrary to implement so I stuck with the basic tests 
  of known inputs and known outputs for the sample data files.
  