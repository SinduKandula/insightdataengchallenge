# insightdataengchallenge
Used Python for this challenge.
Summary of my approach:
1. Read records from the input file and each record was split on pipe and checked for validity.
2. Checked if the name and zipcode was repeated or not by using HashSet. If it was repeated then it would be considered a repeat donor.
3. Then checked for the recipient, zipcode and year and stored it into a dictionary(HashMap) and calculated the count and amount. 
4. Using all of the above percentile was calculated.
5. Then the output was written onto the output file.
