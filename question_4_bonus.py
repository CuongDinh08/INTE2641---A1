# Student ID: S4032825
# Student name: Dinh Ngoc Hoang Cuong

# NOTE: This program is just for fun and educational purposes.
# In this program, I redesign the mining process of the blockchain, so that it could simtaneously mine multiple blocks at the same time.
# The first block (genesis block) will be mined first, then the rest of the blocks will be mined concurrently.
# By using the data of the block, you could see the mining process happening not in order at all
# but any block be successfully mined will be added to the blockchain

from time import time as unix_time
from hashlib import md5, sha256
from typing import  Optional
from termcolor import colored
from datetime import datetime
import os
from concurrent.futures import ThreadPoolExecutor



DIFFICULTY: int = 3
DEFAULT_NONCE: int = 0
GENESIS_PREVIOUS_HASH: str = "0"
GENESIS_DATA: str = "Genesis block"
NUMBER_OF_BLOCKS: int = 5 # Edit this to change the number of blocks to be created in the main function

# Turn on this for cool effect! But it will slow down the mining process.
# If you turn on the DEBUG mode, the mining process will print the hash in a colored format and amount of time used to mine the nonce.
# I suggest you lower the DIFFICULTY to 2 or 3 for a better experience if you want to see the effect.
DEBUG: bool = True

BLOCKCHAIN: list["Block"] = [] # This will hold the blockchain



def clear_console() -> None:
    """
    This function clears the console.
    Source: https://stackoverflow.com/questions/2084508/clear-the-terminal-in-python
    """
    os.system('cls' if os.name == 'nt' else 'clear')



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
    timestamp: float # UNIX timestamp 
    data: str
    previous_hash: str
    nonce: int

    # This variable just for fun!
    start_time: float # The time when the block is start to be mined
    end_time: float # The time when the block is mined (not used in this version, but can be used for future improvements)


    def __init__(self, data: str) -> None:
        self.block_id = self._generate_block_ID()
        self.data = data
        self.nonce = DEFAULT_NONCE


    @classmethod
    def _generate_block_ID(cls) -> str:
        """This method generates a unique block ID based on the current time and MD5 (for short)."""
        return md5(str(unix_time()).encode()).hexdigest()


    @classmethod
    def generate_block(cls, data: Optional[str] = None, genesis_block: bool = False) -> "Block":
        """
        This method generates a new block with the given data and previous block, and also mine the nonce.
        In case of the genesis block, it will use the default data and previous hash.
        If no data is provided, it will use the default genesis data.
        """
        block = cls(data = GENESIS_DATA if genesis_block else data)
        return block


    def mine(self) -> None:
        """This method mines the block by finding a nonce that satisfies the difficulty requirement."""
        print(f"\nMining block { self.block_id }...")

        self.start_time = unix_time()
        previous_block = BLOCKCHAIN[-1] if BLOCKCHAIN else None
        
        # Set the timestamp, block counter, and previous hash based on the previous block
        self.timestamp = unix_time()  # Set the current timestamp
        self.block_counter = 0 if previous_block is None else previous_block.block_counter + 1
        self.previous_hash = GENESIS_PREVIOUS_HASH if previous_block is None else Block.hash_block(previous_block)

        # Hash the block and check if it starts with the required number of zeros
        hash_result = Block.hash_block(self)
        while not hash_result.startswith('0' * DIFFICULTY):
            # Updating the nonce and timestamp
            self.nonce += 1

            # Updating the previous hash and block counter
            previous_block = BLOCKCHAIN[-1] if BLOCKCHAIN else None
            self.timestamp = unix_time()  # Update the timestamp to the current time
            self.block_counter = 0 if previous_block is None else previous_block.block_counter + 1
            self.previous_hash = GENESIS_PREVIOUS_HASH if previous_block is None else Block.hash_block(previous_block)

            hash_result = Block.hash_block(self)

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

        # Adding the mined block to the blockchain
        print(f"\nBlock { self.block_id } mined with nonce { self.nonce } and hash { hash_result }")
        BLOCKCHAIN.append(self)
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
        return f"ID: { self.block_id } | Timestamp: { int(self.timestamp) } | Data: { self.data } | Previous: { self.previous_hash } | None: { self.nonce }"
    

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

        this_block_hash = colored(Block.hash_block(self), "green")
        colored_hash_result = colored("Hash result:", "blue")
        hash_str = f"{ colored_hash_result }   {this_block_hash}"
        print(f"| {hash_str.ljust(79)} |")

        print(f"-----------------------------------------------------------------------------------", end="\n\n")



if __name__ == "__main__":

    # Generate the genesis block and add it to the blockchain
    genesis_block = Block.generate_block(genesis_block=True)
    genesis_block.mine()  # Mine the genesis block

    # Generate the rest of the blocks
    blocks = [Block.generate_block(data=f"Block { index+1 } data") for index in range(NUMBER_OF_BLOCKS - 1)]

    # Multi-threading to simulate concurrent mining
    with ThreadPoolExecutor(max_workers=os.cpu_count() or 1) as executor:
        futures = [executor.submit(block.mine) for block in blocks]
        for future in futures:
            future.result()

    clear_console()  # Clear the console for a fresh start
    # Print the blockchain
    for block in BLOCKCHAIN:
        if block.block_counter != 0: print_arrow_up()  # Print an arrow up symbol for all blocks except the genesis block
        block.beautiful_print()  # Print each block in a beautiful way
