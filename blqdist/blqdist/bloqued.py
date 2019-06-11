#!/usr/bin/env python
__author__ = "http://steemit.com/@cervantes"
__copyright__ = "Copyright (C) 2018 steem's @cervantes"
__license__ = "MIT"
__version__ = "0.1"

from beem import Steem
from beem.comment import Comment
from beem.nodelist import NodeList
from beem.blockchain import Blockchain
from beem.utils import addTzInfo, construct_authorperm
from steemengine.tokenobject import Token
from steemengine.wallet import Wallet
import time
import json
import shelve
import math
import argparse
import logging
from datetime import datetime, date, timedelta
import data
from data import Post, Config
import traceback, sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logging.basicConfig()

timeFormatZ = '%Y-%m-%dT%H:%M:%S.%fZ'

class BlqDistributor:

    def __init__(self, config, steemd_instance):

        self.config = config
        self.stm = steemd_instance
        self.reward_pool = 0
        self.rewards_token = 1
        self.rewards_token_every_n_block = 5
        self.reduction_every_n_block = 10512000
        self.reduction_percentage = 0.5
        self.cashout_window_days = 7
        self.issue_token = False
        self.author_reward_percentage = 75
        self.author_curve_exponent = 1
        self.curation_curve_exponent = 0.5
        self.vote_regeneration_seconds = 432000
        self.vote_power_consumption = 200
        self.downvote_regeneration_seconds = 200
        self.downvote_power_consumption = 432000


    def run(self):

        blocks = []

        chain = Blockchain(steem_instance=steemd_instance)
        current_num = chain.get_current_block_num()
        for block in chain.blocks(start=current_num):
            blocks.append(block)
            print(block.block_num)
            if (block.block_num % self.rewards_token_every_n_block == 0):
                self.reward_pool = self.reward_pool + self.rewards_token
                print("Adding %i BLQS to the rewards pool (actual reward pool: %i BLQ's) " % (self.rewards_token, self.reward_pool))
        len(blocks)


class PostFeeder:

    def __init__(self, config, steemd_instance):

        self.including_tags = ["bloque64"]
        self.including_metadata = []
        self.config = config
        self.steemd_instance = steemd_instance
        self.sa_session = data.return_session()
        self.populate_only_bloque64_posts = False
        self.config_table = self.sa_session.query(Config).filter(Config.token=="BLQ").first()
        

  

    def update_post(self, post):


        self.sa_session.commit()

        

    def update_posts(self):

        posts = self.sa_session.query(Post).all()
        for p in posts:
            self.update_post(p)

    #block including bloque64 post: 33,644,394
    
    def is_bloque64_comment_op(self, op):
        #TODO: Add other bloque64 conditions if needed.
        if(op["value"]["parent_permlink"] == "bloque64"):
            return(True)
        else:
            return(False)

    def get_last_replayed_block(self):
        my_config = self.sa_session.query(Config).filter(Config.token=="BLQ").first()
        return(my_config.last_replayed_block)

    def populate_old_posts(self):

        starting_block = 33644394

        chain = Blockchain(steem_instance=self.steemd_instance)
        current_num = chain.get_current_block_num()
        last_replayed_block = self.get_last_replayed_block()

        logger.info("Populating DB with old bloque64 posts...")
        logger.info("Parsing from last replayed block %s " % last_replayed_block)

        current_num = chain.get_current_block_num()
        #current_num = starting_block
        for b in chain.blocks(start=last_replayed_block):
            logger.info(b)
            for op in b.operations:
                if op["type"] == "comment_operation":  
                    p_json = op["value"]
                    #print(p_json)
                    post = Post(author=p_json["author"], \
                                block = b.block_num, \
                                json_metadata=p_json["json_metadata"], \
                                body = p_json["body"], \
                                parent_permlink = p_json["parent_permlink"] , \
                                parent_author = p_json["parent_author"], \
                                title = p_json["title"], \
                                permlink=p_json["permlink"])

                    try:    
                        identifier =  post.author + "/" + post.permlink   
                        c = Comment(identifier, steem_instance=self.steemd_instance)
                        post.created = c["created"]
                    except:
                        logger.error("Post does not longer exist today: %s" % identifier)
                        #traceback.print_exc(file=sys.stdout)
                        self.sa_session.rollback()

                    self.config_table.last_replayed_block = b.block_num
                    
                    if self.populate_only_bloque64_posts:                    
                        if self.is_bloque64_comment_op(op):
                            self.sa_session.add(post)
                            logger.info("Adding Post: %s" % str(post))
                    else:
                        self.sa_session.add(post)
                        #logger.info("Adding Post: %s" % str(post))
                try:
                    self.sa_session.commit()
                except:

                    logger.error("Could not add post to database: %s" % str(identifier))
                    self.sa_session.rollback()
                    traceback.print_exc(file=sys.stdout)


    def test_parser_1(self):

        c = Comment("stephde/who-wants-to-live-an-ordinary-life-z6jbaeqc", steem_instance=self.steemd_instance)
        p = Post()
        p.body = c["body"]
        self.sa_session.add(p)
        self.sa_session.commit()



def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("config", help="Config file in JSON format")
    args = parser.parse_args()
    config = json.loads(open(args.config).read())
    stm = stm = Steem("https://api.steemit.com")

    #blq_dist = BlqDistributor(config, stm)
    #blq_dist.run()

    blq_post_feeder = PostFeeder(config, stm)
    #blq_post_feeder.run()
    blq_post_feeder.populate_old_posts()
    #blq_post_feeder.update_posts()
    #blq_post_feeder.test_parser_1()


if __name__ == '__main__':
    main()   
