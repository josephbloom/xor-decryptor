# Xor Decryptor
A simple repeating-xor encryption and decryption tool.

This is a simple repeating-xor encryption and decryption tool. This tool is not
meant to securely encrypt any information, and in fact shows how insecure this
kind of encryption is. This is only a demonstration meant for my portfolio and
coding practice.

The two main options are Encrypt and Decrypt. You can encrypt a message by 
entering it manually or by using a simple text file (.txt), and then choosing
a key to encrypt themessage with, also either by manual input or by selecting a
text file with the key in it. A text file with the encrypted message is 
produced, and is base64 encoded so that the message can still be parsed, if not
read intelligibly. This is because an unencoded encrypted message may contain 
non-printable characters, and information could be lost in a simple text file,
or if the encrypted message is simply copy and pasted from the text file 
produced.

The decryption process does not use the selected key, but guesses it instead. 
Start by selecting a .txt file with the (base64 encoded) encrypted message. 
The text file doesn't necessarily need to be produced from this program. Any 
base64 encoded, repeating-xor encrypted message will do. Next, select the range
of possible keysizes, the number of characters, the key may have by choosing 
the lowest guess and then the highest guess. The program will make some 
calculations and will try to guess that was used to encrypt the message. If it
chooses a likely key, but that key still produces some non-printable characters,
then the correct key may not have been in that range of keysizes (or the message
was ecrypted by some other means). It will also show you the decrypted message
using that key. The next three key guesses are also listed above during 
the calculating.

This particular tool guesses based on how much the decrypted message looks like
normal English, or any language with the same set of letters. So any encrypted
message that uses non-standard English characters, like accented letters 
(é, ü, etc.), different alphabets like Korean or Urdu, or "alternative" 
alphabets like leet (1337), will not be decrypted. 

Again, this is for demonstration purposes only, and not serious use. 
I hope you enjoy it!

www.JosephBloomWorks.com
