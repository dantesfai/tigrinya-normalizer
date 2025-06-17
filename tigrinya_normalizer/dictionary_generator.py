import json
import re
import os
import string
import logging
from collections import Counter

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

class TiDictionary:
    """
       A dictionary class designed to process and generate dictionaries from a given input file.

       Attributes:
         input_file (str): The path to the input file.
         output_dir (str): The directory where the output files will be saved.
         logger (Logger): A logger instance for logging important events and errors.

         clitic_zipped_dict (dict): A dictionary mapping clitic tokens to their corresponding zip codes.
         clitic_bind_list (dict): A dictionary mapping bind tokens to their corresponding words.
         short_written_words (dict): A dictionary mapping words with forward slashes to their corresponding original words.
         short_written_words_v2 (dict): A dictionary mapping words with dots to their corresponding original words.
         clitic_dictionary (dict): A dictionary mapping clitic with apostroph to their corresponding expaned word.
         hyphenated_words_v1 (list): A list of hyphenated words for version 1.
         hyphenated_words_v2 (list): A list of hyphenated words for version 2.
    """
    def __init__(self, input_file, output_dir):
        """
        Initializes a new instance of the TiDictionary class.

        Args:
            input_file (str): The path to the input file.
            output_dir (str): The directory where the output files will be saved.
        """
        self.input_file = input_file
        self.output_dir = output_dir
        self.logger = logging.getLogger(__name__)

        # Initialize dictionaries with default values
        from collections import defaultdict
        self.clitic_zipped_dict = defaultdict(str)
        self.clitic_bind_list = defaultdict(str)
        self.short_written_words = defaultdict(str)
        self.short_written_words_v2 = defaultdict(str)
        self.clitic_dict = defaultdict(str)
        self.hyphenated_words_v1 =defaultdict(str)
        self.hyphenated_words_v2 =defaultdict(str) 
    
    def create_output_dir(self, output_dir: str):
        """
        Creates the output directory if it doesn't exist.

        Args:
        output_dir (str): The path of the output directory.
        """
        if not os.path.exists(output_dir):
            try:
                os.makedirs(output_dir)
                self.logger.info(f"Output directory '{output_dir}' created.")
            except Exception as e:
                self.logger.error(f"Error creating output directory: {str(e)}")
     
    def _is_proper_token(self, token):
        # Simplify the condition for proper tokens
        return len(token) == 2 and token[0] != '' and token[1]!=''
   
    def clean_word(self, word: str, keep_punctuation: set = None) -> str:
        """
        Remove all punctuation from the word except the ones specified.
        
        If `keep_punctuation` is None, remove all punctuation.

        Args:
            word (str): The input word to be cleaned.
            keep_punctuation (str, optional): A string of punctuation marks to retain in the word. Default is None.

        Returns:
            str: The cleaned word with only the specified punctuation retained (or all punctuation removed if None).
        """
        # Define all punctuation marks
        all_punctuation = string.punctuation

        if keep_punctuation is None:
            # If keep_punctuation is None, remove all punctuation
            cleaned_word = ''.join(c for c in word if c not in all_punctuation)
        else:
            # Otherwise, retain the specified punctuation
            cleaned_word = ''.join(c for c in word if c not in all_punctuation or c in keep_punctuation)

        return cleaned_word
   
    def create_dictionary(self, clitic_dictionary=None, words_with_fwd_slash=None, words_with_dots=None): 
        self.create_output_dir(self.output_dir)

        if words_with_fwd_slash is not None:
            self.short_written_words = self.read_dict(self.output_dir +"/" + words_with_fwd_slash)
        
        if words_with_dots is not None:
            self.short_written_words_v2 = self.read_dict(self.output_dir +"/" + words_with_dots)

        if clitic_dictionary is not None:
            self.clitic_dict = self.read_dict(self.output_dir + "/"+ clitic_dictionary)
  
        try: 
            with open(self.input_file, encoding="utf-8-sig") as f:
                data = f.read() 
          
            #tokens = re.findall(r'\w+', cleaned_data)
            tokens = data.split()
 
            for word in tokens:

                if '-' in word:  # Handle hyphenated words
                    cleaned_word=self.clean_word(word, "-")
                    parts = cleaned_word.split('-')
                    if len(parts) == 2 and self._is_proper_token([parts[0], parts[1]]):
                        self.hyphenated_words_v1[f"{parts[0]}{parts[1]}"] = cleaned_word
                        self.hyphenated_words_v2[cleaned_word] = f"{parts[0]} {parts[1]}"
                elif '/' in word:  # Handle words with forward slashes
                    cleaned_word = self.clean_word(word, "/")
                    if cleaned_word not in self.short_written_words:
                        #proper_word = self.lookup_proper_word(word)
                        self.short_written_words[cleaned_word] = cleaned_word
                        #self.short_written_words[proper_word] = proper_word
                elif "'" in word or "`" in word or "’" in word:  # Handle clitic words
                    
                    cleaned_word= self.clean_word(word, set("`’'"))  
                    token_parts = re.split(r"[`’']", cleaned_word)
                  
                    if self._is_proper_token(token_parts):
                        self.clitic_zipped_dict[token_parts[0]] = token_parts[1]
                        bind_token = ''.join(token_parts[:2])
                        self.clitic_bind_list[bind_token] = cleaned_word
            
            self.extract_shortened_words_By_dots(data)
            #self.extract_shortened_words_By_fwd_slash(data)
            self.write_to_dict()

            print('Process done. Ready for writing to a file.')
        except Exception as e:
            logging.error(f"Error creating dictionary: {str(e)}")
  
    def read_dict(self, filename):
       # Read the dictionary from the text file
        with open(filename, 'r', encoding="utf-8") as file:
            dict_obj = json.load(file)

        return dict_obj
    
    
    def extract_shortened_words_By_dots(self, text):
        """
        Extract shortened words (e.g., A.I, ኤስ.ፒ.ኤል.ኤም) from the text and create a dictionary
        with empty strings as placeholders for their expanded forms.
        
        Args:
            text (str): Input text containing shortened words.
            
        Returns:
            dict: A dictionary with shortened words as keys and empty strings as values.
        """
        # Updated regex to include patterns for Tigrinya words like ኪ., ምም., ቤ.ት, ሃ.ማ.መ.ተ.ኤ
        pattern = r"(?<!\w)(?:[\w\u1200-\u137F]{1,2}+\.)+(?:[\w\u1200-\u137F]{1,7}+)?(?:\.)?(?!\w)" # Matches sequences of at least 2 dot-separated letters
       
        # Find all matches
        shortened_words = re.findall(pattern, text) 
        # Create a dictionary with empty strings as values
        shortened_dict = {word: word for word in shortened_words if word not in self.short_written_words_v2}
        #print(shortened_dict)
        self.short_written_words_v2.update(shortened_dict)
        
        return shortened_dict
    
    def extract_shortened_words_By_fwd_slash(self, text):
        """
        Extract shortened words (e.g., A.I, ኤስ.ፒ.ኤል.ኤም) from the text and create a dictionary
        with empty strings as placeholders for their expanded forms.
        
        Args:
            text (str): Input text containing shortened words.
            
        Returns:
            dict: A dictionary with shortened words as keys and empty strings as values.
        """
        # Updated regex to include patterns for Tigrinya words like ኣፍ., ምም., ቤ.ት, ሃ.ማ.መ.ተ.ኤ
        pattern = r"(?<!\w)(?:[\w\u1200-\u137F]{1,2}+/)+(?:[\w\u1200-\u137F]{1,2}+)?(?:/)?(?!\w)" # Matches sequences of at least 2 dot-separated letters
        
        # Find all matches
        shortened_words = re.findall(pattern, text)
        
        # Create a dictionary with empty strings as values
        shortened_dict = {word: "" for word in shortened_words if word not in self.short_written_words}
        self.short_written_words.update(shortened_dict)
        
        return shortened_dict
    
    def write_to_dict(self):
        try:
            self._write_file("clitic_zipped_dict.txt",   dict(sorted(self.clitic_zipped_dict.items())))
            self._write_file("clitic_bind_dic.txt",      dict(sorted(self.clitic_bind_list.items())))
            self._write_file("words_with_fwd_slash.txt", dict(sorted(self.short_written_words.items())))
            self._write_file("words_with_dots.txt",      dict(sorted(self.short_written_words_v2.items())))
            self._write_file("hyphenated_words_v1.txt",  dict(sorted(self.hyphenated_words_v1.items())))
            self._write_file("hyphenated_words_v2.txt",  dict(sorted(self.hyphenated_words_v2.items())))
        except Exception as e:
            logging.error(f"Error writing to dictionary: {str(e)}")

    def _write_file(self, filename: str, data: dict) -> None:
        try:
            with open(self.output_dir + "/" + filename, "w", encoding="utf-8") as file:
                json.dump(dict(data), file, ensure_ascii=False, indent=1)
        except Exception as e:
            logging.error(f"Error writing {filename}: {str(e)}")       
    
    def create_improper_clitic(self):
        """
        Create a dictionary of improper clitics from 'clitic_bind_list' and update it based on the text in 'infile'.
        
        The resulting dictionary is written to 'cliticize_improper_words.txt' in JSON format.
        """
        
        # Load the dictionary of improper clitics
        self.clitic_concat_words = json.load(open(self.output_dir + '/' + "clitic_bind_dic.txt", encoding='utf-8'))
        
        # Initialize dictionaries for clitic counts and improper words
        clitic_counts = {}
        cliticize_improper_words = {}
        
        # Populate the initial clitic counts dictionary
        for key, value in self.clitic_concat_words.items():
            clitic_counts[key] = 0
        
        try:
            with open(self.input_file, encoding='utf-8-sig') as f:
                data = f.read()
                
                # Split the data into individual words
                for word in data.split():
                    if word in clitic_counts:
                        clitic_counts[word] += 1
                
                # Sort the clitic counts dictionary by value in descending order
                sorted_by_value = dict(sorted(clitic_counts.items(), key=lambda kv: kv[1], reverse=True))
                
                # Filter out words with higher than 5 occurrences and update the improper words dictionary
                for key, value in sorted_by_value.items():
                    if value > 5:
                        cliticize_improper_words[key] = self.clitic_concat_words[key]

                # Write the improper words dictionary to a file
            with open(self.output_dir + '/' + 'cliticize_improper_words.txt', 'w', encoding='utf-8') as file:
                file.write(json.dumps(cliticize_improper_words, ensure_ascii=False, indent=1))
            
            print("Done!")

        except FileNotFoundError as e:
            print(f"Error: File '{self.infile}' not found.")
            raise

    def write_clitic_dict(self, input_dict): 

        # Count the frequency of each value in the input dictionary
        value_counts = Counter(input_dict.values())
        #print(value_counts)
        #Sort the values by frequency (highest to lowest)
        sorted_values = [item[0] for item in value_counts.most_common()]

        # Create a new dictionary with sorted values (empty string as value)
        sorted_dict = {value: value for value in sorted_values}
        
        self.clitic_dict.update({v:v for v in sorted_dict if not self.clitic_dict.get(v)})
 
        # Create a new dictionary where values from the input dict become keys, with empty strings as their values
        #output_dict = {value: "" for value in set(input_dict.values())}

        # Define the output file path
        output_file_path = self.output_dir + '/' +"clitic_dict.txt"

        # Save the new dictionary to a file
        with open(output_file_path, 'w', encoding='utf-8') as f:
            json.dump(self.clitic_dict, f, ensure_ascii=False, indent=4)

        print(f"Dictionary saved to {output_file_path}")    
        
