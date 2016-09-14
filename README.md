# dmgCracker
Brute-force dictionary program to test out many different passwords as fast as possible. 
Forced to write own program since crowbarDMG was very slow around 1.2seconds per password check. Single threaded and was also i believe trying to mount the drive at the same time. Using 'verify' and not 'attach' subprocess, i hope to do more passwords cycles and run multiple cycles per minute to increase chances of finding the password with a larger dictionary.

LEGAL NOTE: This program was created for the intention of cracking my own .dmg image which I had locked myself out of. I do not suggest using this program for illegal purposes such as opening .dmg images that you are not allowed access to and that you do not own yourself. 

If you require a wordlist-generator, I also wrote a program to do this as well. 
