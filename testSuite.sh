echo "Starting QM Test Suite"
echo "Generating data..."
python3 main.py testInputs/test1.pla testOutputs/testOutput1.pla
python3 main.py testInputs/test2.pla testOutputs/testOutput2.pla
python3 main.py testInputs/test3.pla testOutputs/testOutput3.pla
python3 main.py testInputs/test4.pla testOutputs/testOutput4.pla
python3 main.py testInputs/test5.pla testOutputs/testOutput5.pla
python3 main.py testInputs/test6.pla testOutputs/testOutput6.pla
echo "Finished generating data. Comparing results..."
diff -iw testOutputs/testOutput1.pla validationOutputs/output1.pla
echo "Test 1 Complete"
diff -iw testOutputs/testOutput2.pla validationOutputs/output2.pla
echo "Test 2 Complete"
diff -iw testOutputs/testOutput3.pla validationOutputs/output3.pla
echo "Test 3 Complete"
diff -iw testOutputs/testOutput4.pla validationOutputs/output4.pla
echo "Test 4 Complete"
diff -iw testOutputs/testOutput5.pla validationOutputs/output5.pla
echo "Test 5 Complete"
echo "Finished running test suite"