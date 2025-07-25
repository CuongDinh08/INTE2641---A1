# Student ID: S4032825
# Student name: Dinh Ngoc Hoang Cuong

from time import time as unix_time
from hashlib import md5, sha256
from typing import  Optional
from termcolor import colored
from datetime import datetime
from random import randint, choice
import os


DIFFICULTY: int = 3
DEFAULT_NONCE: int = 0
GENESIS_PREVIOUS_HASH: str = "0"
GENESIS_DATA: str = "Genesis block"
NUMBER_OF_BLOCKS: int = 5 # Edit this to change the number of blocks to be created in the main function

# Turn on this for cool effect! But it will slow down the mining process.
# If you turn on the DEBUG mode, the mining process will print the hash in a colored format and amount of time used to mine the nonce.
# I suggest you lower the DIFFICULTY to 2 or 3 for a better experience if you want to see the effect.
DEBUG: bool = True


def clear_console() -> None:
    """
    This function clears the console.
    Source: https://stackoverflow.com/questions/2084508/clear-the-terminal-in-python
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def random_string(length: int = 10) -> str:
    """
    This function generates a random string of the given length.
    In case that the length is less than or equal to 0, it will generate a random length between 1 and 20.
    The string will contain characters from a-z, A-Z, and 0-9.`
    """
    length = length if length > 0 else randint(1, 20)
    lowercase = [chr(index) for index in range(97, 123)]  # a-z
    uppercase = [chr(index) for index in range(65, 91)]  # A-Z
    digits = [chr(index) for index in range(48, 58)]  # 0-9

    random_string = []
    for _ in range(length):
        # Generate a random character from a-z, A-Z, 0-9
        random_string.append(choice(lowercase + uppercase + digits))
    return ''.join(random_string)


def print_arrow_up() -> None:
    """This function prints an arrow up symbol."""
    print("                                      /|\        ")
    print("                                     / | \       ")
    print("                                    /  |  \      ")
    print("                                       |         ")
    print("                                       |         ", end="\n\n")


class Block:
    block_counter: int  # Static variable to keep track of the number of blocks created
    block_id: str
    timestamp: float # UNIX timestamp when the block is created (not mined or confirmed)
    data: str
    previous_hash: str
    nonce: int
    confirm_time: float # The time when the block is mined (confirmed)

    # This variable just for fun!
    start_time: float # The time when the block is start to be mined
    end_time: float # The time when the block is mined (not used in this version, but can be used for future improvements)


    def __init__(self, block_counter: int, data: str, previous_hash: str) -> None:
        self.block_counter = block_counter
        self.block_id = self._generate_block_ID()
        self.timestamp = unix_time()  # Set the timestamp to the current time
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = DEFAULT_NONCE


    @classmethod
    def _generate_block_ID(cls) -> str:
        """This method generates a unique block ID based on the current time and MD5 (for short)."""
        return md5(str(unix_time()).encode()).hexdigest()


    @classmethod
    def generate_block(cls, data: Optional[str] = None, previous_block: Optional["Block"] = None) -> "Block":
        """
        This method generates a new block with the given data and previous block, and also mine the nonce.
        In case of the genesis block, it will use the default data and previous hash.
        If no data is provided, it will use the default genesis data.
        """
        block = cls(
            block_counter = 0 if previous_block is None else previous_block.block_counter + 1,
            data = GENESIS_DATA if previous_block is None else data,
            previous_hash = GENESIS_PREVIOUS_HASH if previous_block is None else Block.hash_block(previous_block),
        )
        block.mine()
        return block


    def mine(self) -> None:
        """This method mines the block by finding a nonce that satisfies the difficulty requirement."""
        print(f"Mining block {self.block_id}...")

        self.start_time = unix_time()
        self.confirm_time = unix_time()  # Set the confirm_time to the current time

        # Hash the block and check if it starts with the required number of zeros
        hash_result = Block.hash_block(self)

        # In case the hash already satisfies the difficulty requirement, we can skip the mining process
        # If not, we will keep incrementing the nonce until we find a valid hash
        while not hash_result.startswith('0' * DIFFICULTY):
            self.nonce += 1 # Update the nonce
            self.confirm_time = unix_time()  # Update the confirm_time to the current time
            hash_result = Block.hash_block(self) # Hash the block again with the new nonce

            # Where the cool effect happens
            if DEBUG:
                console_hash_output: list = []
                for index in range(DIFFICULTY):
                    if hash_result[index] == '0':
                        console_hash_output.append(colored(hash_result[index], 'green'))
                    else:
                        console_hash_output.append(colored(hash_result[index], 'red'))
                # Append the rest of the hash
                console_hash_output += hash_result[DIFFICULTY:]
                print(f"\rMining block { self.block_id } with nonce { self.nonce }: { ''.join(console_hash_output) }", end='\n')

        # Once we find a valid nonce, we can print the result
        self.end_time = unix_time()

        if DEBUG:
            consume_time = self.end_time - self.start_time
            consume_time = colored(f"{consume_time:.2f} seconds", "yellow")
            # Print the time taken to mine the block
            print(f"\nBlock { self.block_id } mined in { consume_time }.")

            hash_rate = self.nonce / (self.end_time - self.start_time)
            hash_rate = colored(f"{hash_rate:.2f} hashes/second", "yellow")
            print(f"Hash rate: { hash_rate }")

        # Print 2 empy lines for better readability
        print("\n\n", end="")
                    
    
    @classmethod
    def hash_block(cls, block: "Block") -> str:
        """This method hashes the block using SHA-256."""
        return sha256(str(block).encode()).hexdigest()
    

    def __str__(self, show_human_time: bool = False) -> str:
        """This method returns a string representation of the block."""
        return f"ID: { self.block_id } | Timestamp: { int(self.timestamp) } | Data: { self.data } | Previous: { self.previous_hash } | None: { self.nonce } | Confirmed: { self.confirm_time }"
    

    def beautiful_print(self) -> None:
        """This method prints the block in a beautiful way."""
        print(f"-----------------------------------------------------------------------------------")

        colored_previous_hash = colored(self.previous_hash, "green")
        previous_hash_title = colored("Previous hash:", "blue")
        previous_hash_str = f"{ previous_hash_title } { colored_previous_hash }"
        print(f"| {previous_hash_str.ljust(97)} |")

        colored_block_counter = colored("Block counter:", "blue")
        block_counter_str = f"{ colored_block_counter } { self.block_counter }"
        print(f"| {block_counter_str.ljust(88)} |")

        colored_block_id = colored("Block ID:", "blue")
        block_id_str = f"{ colored_block_id } { self.block_id }"
        print(f"| {block_id_str.ljust(88)} |")

        readable_time = datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d %H:%M:%S.%f')
        colored_timestamp = colored("Timestamp:", "blue")
        timestamp_str = f"{ colored_timestamp } {self.timestamp} ({ readable_time })"
        print(f"| {timestamp_str.ljust(88)} |")

        colored_data = colored("Data:", "blue")
        data_str = f"{ colored_data } {self.data}"
        print(f"| {data_str.ljust(88)} |")

        colored_nonce = colored("Nonce:", "blue")
        nonce_str = f"{ colored_nonce } {self.nonce}"
        print(f"| {nonce_str.ljust(88)} |")

        readable_time = datetime.fromtimestamp(self.start_time).strftime('%Y-%m-%d %H:%M:%S.%f')
        colored_confirm_time = colored("Confirm time:", "blue")
        confirm_time_str = f"{ colored_confirm_time } {self.confirm_time} ({ readable_time })"
        print(f"| {confirm_time_str.ljust(88)} |")

        this_block_hash = colored(Block.hash_block(self), "green")
        colored_hash_result = colored("Hash result:", "blue")
        hash_str = f"{ colored_hash_result }   {this_block_hash}"
        print(f"| {hash_str.ljust(79)} |")

        print(f"-----------------------------------------------------------------------------------", end="\n\n")


if __name__ == "__main__":
    clear_console()  # Clear the console for a fresh start

    blockchain: list[Block] = []

    print(f"The system will generate {NUMBER_OF_BLOCKS} blocks in total, including the genesis block with difficulty: { DIFFICULTY }\n")
    input("Press any key and Enter to generate the genesis block...")
    clear_console()  # Clear the console for a fresh start

    # Create the genesis block and append it to the blockchain
    genesis_block = Block.generate_block()
    blockchain.append(genesis_block)
    genesis_block.beautiful_print()  # Print the genesis block in a beautiful way

    for index in range(1, NUMBER_OF_BLOCKS):
        input("Press any key and Enter to generate the next block...")
        clear_console()  # Clear the console for a fresh start

        # Generate a new block with random data and the previous block
        block = Block.generate_block(data=random_string(), previous_block=blockchain[-1])
        blockchain.append(block)
        block.beautiful_print()  # Print each block in a beautiful way

    print("\nAll blocks have been generated successfully!\n")
    input("Press any key and Enter to print the blockchain...")
    clear_console()  # Clear the console for a fresh start

    # Print the blockchain
    for block in blockchain:
        if block.block_counter != 0: print_arrow_up()  # Print an arrow up symbol for all blocks except the genesis block
        block.beautiful_print()  # Print each block in a beautiful way
