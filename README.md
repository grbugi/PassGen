# Password Generator 🔑

This Password Generator creates semi-randomize combinations of charters.

## Featchers
Main feachure is algorithm that never miss required chater's type (excluding case where number of charters less then number of required charter's types).

🖥️ It is compleatly offline.
📜 It creates log file every time when you open the program. So you will never been missed your random password.
🧮 It counts nuber of chars from manual inputed password.
💾 It will save your preferences in configuration file and load it next time.
✏️ You can easely edit random password and it will have been saved after edited password copying.
🖱️ If you copy password it will copy that whole (even if you miss first or last charter when you select it). 

## Usage
Enter number of characters.
Select the required options for include or exlude the characters:

```
a..z        - Lowercase letters
A..Z        - Uppercase Letters
0..9        - Numbers
!@#$        - Symbols
oO0lI1|     - Similar characters
.,_:;\'\"`? - Dots like symbols and ? (for Cisco equipment)
/()[]{}<>|  - Brackets
Excel       - Replace last character for letter (for slove Excel's issues)
```

Click on "Generate" button or hit "Enter" or "Return" on your keyboard.
After generation, the password will be automatically copied to your clipboard.
You can edit generated password and copy it with "Copy" button or with Ctrl+C. PassGen will count the numer of charters in your password. Take a note, Password Generator copying whole password everytime.'
The Password Generator keeps logs. You can open the log file by clicking on the appropriate button or with Ctrl+L.
You can find the log files and configuration file in "Password Generator" folder near executable file of the application.



_It is my firs Python expirience. So I will be happy if comunity will support me._
