# There is a FASTER method:

Download http://www.openwall.com/john/ (John the ripper)

Locate /run folder in the john folder (you may have to compile)

Locate /run/dmg2john

$./dmg2john your_file.dmg >> output

$./john output

or

$./john --format=dmg-opencl output

note: this will use john's standard wordlist tries, please read john's documentation to use your own wordlists or password rules. I found that with my laptop I can get 15 tries p/s. 



# dmgCracker
Brute-force dictionary program to crack dmg encrypted images.
I wrote this program as the next available program was crowbarDMG.
From a glance crowbar was: 
  Single threaded.
  Tries to mount the drive at the same time.
  Runs about .8 passwords per second. (256bit encryption)
dmgCracker is better because:
  Multi-threaded, and allows for multiple dictionary files to be tested (increases chances of finding password).
  Uses 'verify' and not 'attach' subprocess for faster password checking.
  Runs about 55 passwords per second with 128bit encryption.
  Runs about 3.6 passwords per second with 256bit encryption.

LEGAL NOTE: This program was created for the intention of cracking my own .dmg image which I had locked myself out of. I do not suggest using this program for illegal purposes such as opening .dmg images that you are not allowed access to and that you do not own yourself. 

If you require a wordlist-generator, I also wrote a program to do this as well. 

To run, you must have a encrypted dmg file in the same folder, and at least 1 passphrase file containing a dictionary. (a list of words)
