import sys
from steemapi.steemnoderpc import SteemNodeRPC

class FollowMe(object):
    def __init__(self):
        self.rpc = SteemNodeRPC("wss://node.steem.ws", "", "", apis=["follow"])

    def followers(self, account):
        return [ f["follower"] for f in self.rpc.get_followers(account, "", "blog", 100, api="follow") ]

    def following(self, account):
        return [ f["following"] for f in self.rpc.get_following(account, "", "blog", 100, api="follow") ]



if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: %s <steem_account>" % (sys.argv[0],))
        sys.exit(1)
    f = FollowMe()
    print("%s followers %s" % (sys.argv[1], f.followers(sys.argv[1])))
    print("%s follows %s" % (sys.argv[1], f.following(sys.argv[1])))

    for follower in f.followers(sys.argv[1]):
        print("%s is followed by %s" % (follower, f.followers(follower)))
        print(60*"-")

    for following in f.following(sys.argv[1]):
        print("%s follows %s" % (following, f.following(following)))
        print(60*"-")
