from pprint import pprint
from beem import Steem
from beem.account import Account
from beem.comment import Comment
from beem.blockchain import Blockchain
from beem.instance import set_shared_steem_instance

# not a real working key
wif = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3"

stm = Steem(
    bundle=True, # Enable bundle broadcast
    # nobroadcast=True, # Enable this for testing
    keys=[wif],
)
# Set stm as shared instance
set_shared_steem_instance(stm)
chain = Blockchain(steem_instance=stm)

blocks = []
current_num = chain.get_current_block_num()
for block in chain.blocks(start=current_num):
    blocks.append(block)
    for op in block.operations:
        #print(op["type"])
        if op["type"] == "comment_operation":
            print(op)


def populate_old_posts():

    current_num = chain.get_current_block_num()
    for operation in chain.ops(start=current_num - 99, stop=current_num):
