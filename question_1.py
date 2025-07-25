# Student ID: S4032825
# Student name: Dinh Ngoc Hoang Cuong

from hashlib import sha256
from random import randint
from termcolor import colored
from sys import stdout



def change_minimal(input_str: str) -> str:
    """
    Returns a new string with randomly change one character in the input string.
    """
    # Get the index of the character to change
    change_index = randint(0, len(input_str) - 1)
    
    # Get the random character to replace the original character
    random_char = ""
    while True:
      # Generate a random character in the range of lowercase letters (ASCII 97-122)
      random_char = chr(randint(97, 122))
      # Ensure the random character is different from the original character
      if random_char != input_str[change_index]:
        break
      
    # Create a new string with the changed character
    new_string = input_str[:change_index] + colored(random_char, 'red') + input_str[change_index + 1:]
    return new_string



def highlight_difference(original: str, modified: str) -> tuple[str, str]:
    """
    Highlights the difference between the original and modified strings.
    """
    original_hightlights = []
    modified_hightlights = []
    
    total = len(original)
    total_difference = 0
    
    for origin, modify in zip(original, modified):
      if origin != modify:
        original_hightlights.append(colored(origin, 'red'))
        modified_hightlights.append(colored(modify, 'yellow'))
        total_difference += 1
      else:
        original_hightlights.append(colored(origin, 'green'))
        modified_hightlights.append(colored(modify, 'green'))
    
    return "".join(original_hightlights), "".join(modified_hightlights), f'{total_difference}/{total}'



def create_sequence_string(previous: str | None) -> str:
  """
  This function is used to create a sequence string based on the previous string.
  It uses a custom sequence of characters: lowercase letters, uppercase letters, and digits.

  This function is created with the help of ChatGPT, which was then revised.
  """
  lowercase = [chr(index) for index in range(97, 123)]  # ASCII values for 'a' to 'z'
  uppercase = [chr(index) for index in range(65, 91)]  # ASCII values for 'A' to 'Z'
  digits = [chr(index) for index in range(48, 58)]  # ASCII values for '0' to '9'
  specials = [chr(index) for index in range(32, 48)]  # ASCII values for special characters from space to '/'
  specials += [chr(index) for index in range(58, 65)]  # ASCII values for special characters from ':' to '@'

  sequence = lowercase + uppercase + digits + specials

  def increment(string):
    # If the string is empty, return the first character in the sequence, which should be 'a'
    if not string:
        return sequence[0]

    last_char = string[-1] # Get the last character of the string
    rest = string[:-1]  # All characters except the last one

    # Find the index of the last character in the sequence
    index = sequence.index(last_char)

    # In the case of the last character not being the last in the sequence,
    # increase it and return the new string
    if index + 1 < len(sequence):
        return rest + sequence[index + 1]
    
    # Otherwise, we need to rollover this character and increase the rest
    # rollover, reset this character and increase the rest
    else:
        return increment(rest) + sequence[0]
  
  return increment(previous)



# ------- Main program -------
if __name__ == "__main__":


  # ------- Task 1.1 and 1.2 -------
  # Get arbitrary string from the command line
  input_str = input("Enter an arbitrary string: ")
  
  # Calculate the SHA256 hash of the input string
  hashed_input_string = sha256(input_str.encode()).hexdigest()
  # Print the hashed string
  print(f"SHA256 hash of the input string: {hashed_input_string}")
  


  # ------- Task 1.3 -------
  print("\n-------------------------------------------------------------------------------------------------")
  # Change one character in the input string
  new_string = change_minimal(input_str)
  print(f'Generated string with one character changed: {new_string}')
  # Calculate the SHA256 hash of the new string
  hashed_new_string = sha256(new_string.encode()).hexdigest()
  # Print the hashed new string
  print(f"SHA256 hash of the new string: {hashed_new_string}")
  
  print("-------------------------------------------------------------------------------------------------")
  # Highlight the difference between the original and modified strings
  origin_highlight, modified_highlight, total_difference = highlight_difference(hashed_input_string, hashed_new_string)
  print(f'Original hash: {origin_highlight}')
  print(f'Modified hash: {modified_highlight}')
  print(f'Total differences: {total_difference}')


  # ------- Task 2 -------
  # This is where the brute force begin =))
  # I can make it running faster using multiple cores or threads
  # But I love the looking cool effect, so I choose to make it this way
  print("\n-------------------------------------------------------------------------------------------------")
  print("Attempting to break the hash by generating a sequence of strings...")

  attempt_number = 0
  # Get the number of attempts from the command line
  while True:
    attempt_number = input("Enter the number of attempts (0 for unlimited), you could press Ctrl+C or Command+C to stop: ")
    # Checking if the user input is valid
    if attempt_number.isdigit() and int(attempt_number) >= 0:
      attempt_number = int(attempt_number)
      break
    else:
      print("Please enter a valid non-negative integer for the number of attempts.")

  found = True
  # If the user entered 0, set the attempts to unlimited
  if attempt_number == 0: 
    current_value = None
    attempt_index = 1

    while True:
      if attempt_index != 1:
        # Put the cursor back 4 lines to overwrite the previous output
        print("\033[F\033[F\033[F\033[F", end="")

      current_value = create_sequence_string(current_value)
      print(f"Attempt {attempt_index}: {current_value}")
      attempt_index += 1

      # Hash the current value
      hashed_current_value = sha256(current_value.encode()).hexdigest()

      origin_highlight, modified_highlight, total_difference = highlight_difference(hashed_input_string, hashed_current_value)
      print(f'Original hash: {origin_highlight}', flush=True)
      print(f'Modified hash: {modified_highlight}', flush=True)
      print(f'Total differences: {total_difference} ', flush=True)

      # Check if the hash matches the hashed new string
      if hashed_current_value == hashed_input_string:
        print(f"Hash match found after {attempt_index - 1} attempts: {current_value}")
        break
      else:
        stdout.flush()
  
  # Otherwise, only run at the limit 
  else:
    current_value = None
    for attempt_index in range(1, attempt_number + 1):
      if attempt_index != 1:
        # Put the cursor back 4 lines to overwrite the previous output
        print("\033[F\033[F\033[F\033[F", end="")

      current_value = create_sequence_string(current_value)
      print(f"Attempt {attempt_index}: {current_value}")

      # Hash the current value
      hashed_current_value = sha256(current_value.encode()).hexdigest()

      origin_highlight, modified_highlight, total_difference = highlight_difference(hashed_input_string, hashed_current_value)
      print(f'Original hash: {origin_highlight}')
      print(f'Modified hash: {modified_highlight}')
      # If the differnce get low to only one digits, it could cause the output do not clear the last ouput, so I add a space at the end
      print(f'Total differences: {total_difference} ')

      # Check if the hash matches the hashed new string
      if hashed_current_value == hashed_input_string:
        print(f"\nHash match found after {attempt_index} attempts: {current_value}")
        break
