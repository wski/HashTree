from hashlib import sha256

class HashTree:
    
    def __init__(self, transactions=None):
        self.transactions = transactions
        # Root hash
        self.root = None
        # Tree (e.g. [roothash, [h0, h1], [h0-0, h0-1, h1-0, h1-1]])
        self.tree = []
        # Hash leaf nodes
        self.leaves()

    # Hash transaction data
    def leaves(self):
        leaf = []
        for tx in self.transactions:
            leaf.append(sha256(tx).hexdigest())
        self.tree.append(leaf)

    def hash(self, transactions=None):
        # Used to store hashed nodes
        cache = []
        # If transactions are provided, we're hashing nodes, not leaves
        txs = transactions or self.transactions
        # If our transactions are not even, we'll iterate once more
        length = len(txs) / 2 + len(txs) % 2
        
        for i in range(length):
            # Hash leaves
            left = sha256(txs[i]).hexdigest()
            right = sha256(txs[i + 1] or '').hexdigest()
            # Combine data hashes
            node = left + right
            # Hash nodes
            cache.append(sha256(node).hexdigest())
        
        # Finalize tree
        self.tree.insert(0, cache)
        # If we haven't gotten to the root hash, keep going
        if len(cache) is not 1:
            self.hash(cache)
        # Otherwise set our root hash and quit iterating
        else:
            # Replace transaction data with hashes for ease of use
            self.transactions = self.tree[-1]
            # Set root hash
            self.root = cache[0]
        

