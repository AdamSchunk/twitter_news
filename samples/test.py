import sys
import time
import re

text = "May 3: Rubio tells Trump to act fast on Cuba, WH agrees\n\nMay 9: Comey fired\n\nDuring Comey testimony, Rubio acts as\u2026 https://t.co/diNSDqrjDv"
print(text)

text = re.sub(r'https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)



print(text)