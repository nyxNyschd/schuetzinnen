from fuzzywuzzy import fuzz
from fuzzywuzzy import process


Str1 = "The supreme court case of Nixon vs The United States"
Str2 = "Nixon v. United States"
Token_Sort_Ratio = fuzz.token_sort_ratio(Str1,Str2)
Token_Set_Ratio = fuzz.token_set_ratio(Str1,Str2)
print(Token_Sort_Ratio)
print(Token_Set_Ratio)
