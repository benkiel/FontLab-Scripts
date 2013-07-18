#! /usr/bin/awk -f
# Change this to suit your system

# makeText, a short program to create a resonable representation of normal
# English with a string of characters that is less then 26
# Copyright (C) 2004, Ben Kiel, ben@benkiel.com
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA


BEGIN {

  load_dict();
  print "Processed " num_dict " words from dictionary. The longest word is " length_dict "."
  
  # Break txt file words and count the number of letters and 'e's, dump to text file
  while ((getline < "input.txt") > 0) {
    
    #Start loop to create a file that has a pair of numbers seperated by spaces.
    #The first number is the length of the word. The second is the number of 'e's in the word.
    for (i = 1; i <= NF; i++) {
		wordlength = length($i)
    	numberofe = 0
    	numberofa = 0
    	split($i, characterlookup, "")
    	for (item in characterlookup) {
    		if (characterlookup[item] == "e") { 
    			++numberofe
    		}
    		if (characterlookup[item] == "a") {
    			++numberofa
    		}
		}
		print wordlength ":" numberofe ":" numberofa " " > "textFileProcess.tmp"
	}
  }

  print "Processed input text"
  FS = ":"
  while ((getline < "textFileProcess.tmp") > 0) {
  	#Load the value for length and the number of 'e's
  	
  	replaceLength = $1
  	replaceE = $2
  	replaceA = $3
  	#Check to see if the word to be replaced is longer then the longest word
  	#in the dictionary. If so, replace with the longest word possible.
  	if (replaceLength > length_dict) {
  		replaceLength = length_dict
  	}
  	foundWord = 0
  	loopCount = 0
  	failsafe = 0
  	while (foundWord == 0) {
	  ++loopCount
	 
	  #Get random word from the dictionary
	  randomNumber = generateRandom(num_dict)
	  compareWord = dict[randomNumber]
	  
	  if (loopCount == num_dict) {
	  		if (failsafe == 1) {
	  			newText = newText backupWord " "
	  			foundWord = 1
	  		}
	  		else {
	  			newText = newText compareWord " "
	  			foundWord = 1
			}
	  }
	  
	  #Does the random word meet the criteria?
	  numberofe = 0
	  numberofa = 0
    	split(compareWord, characterlookup, "")
    	for (item in characterlookup) {
    		if (characterlookup[item] == "e") { 
    			++numberofe
    		}
    		if (characterlookup[item] == "a") {
    			++numberofa
    		}
		}
	  if (replaceLength == length(compareWord)) {
	  		backupWord = compareWord
	  		failsafe = 1
	  	}
		
	  if ((replaceLength == length(compareWord)) && (numberofe == replaceE) && (numberofa == replaceA)) {
	  		newText = newText compareWord " "
	  		foundWord = 1
	  }
	}
  }
  	print "Done replacing text."
	print newText > "newText.txt"
}

function load_dict() {
  # Load list of words
  num_dict = 0
  length_dict = 0
  
  while ((getline < "wordList.dict") > 0) {
		if (length($0) > length_dict) {
  			length_dict = length($0)
  		}
  		dict[num_dict] = $0
  		++num_dict	
  }
}

# Function to give a random number from 0 to n - 1
function generateRandom(n) { 
	return int(n * rand())
}


