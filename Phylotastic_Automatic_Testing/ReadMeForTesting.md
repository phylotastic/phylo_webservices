# Guidelines for testing web services with test cases

1. Each web service has a folder of its own in the [repository](https://github.com/phylotastic/phylo_webservices/tree/master/Phylotastic_Automatic_Testing). 
2. To test a web service the __test case__ files need to be committed into its respective folder.
3. A **test case** will consist of two types of text files (files with *.txt* extension) : 
   - input file: containing the input for the web service    
   - output file: containing the expected output from the web service 
4. The test case files must conform to a naming convention. The input files must have the word _"input"_ and a test case number following the underscore (_) after the _"input"_ word. Before the _input_ word any name can be attached. For example, "_ws1_birds_input_1.txt_" is a valid name for a input file where 1 is the test case number. Same rules must be followed for the name of the corresponding output files except that the word "_input_" will be replaced with the word "_output_". **The test case numbers must match for the input and corresponding output files.**

5. The contents of the test case files must conform to some rules. Single input or outout must be in one line. In case of multiple inputs or outputs each input/output must be in a separate line. Depending on the web service the content types (single or multiple) of test case files may be different. 
