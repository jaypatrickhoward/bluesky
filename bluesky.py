import argparse
import requests
import sys

def chunked(items, n=1):
    chunk = []
    for item in items:
        chunk.append(item)
        if len(chunk) >= n:
            yield chunk
            chunk = []
    if chunk:
        yield chunk

def parse_arguments():
    parser = argparse.ArgumentParser(
        prog="python3 bluesky.py",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Ranks accounts by their popularity among the accounts you follow.")
    parser.add_argument(
        "actor",
        help="your account did or fully qualified handle, foobar.bsky.social")
    parser.add_argument(
        "-n", "--number-to-show",
        dest="number_to_show", type=int, default=30,
        help="number of results to show in each ranking")
    parser.add_argument(
        "-l", "--global-follower-threshold",
        dest="global_follower_threshold", type=int, default=500,
        help="only show accounts in the relative ranking that are followed by at least this many accounts")
    parser.add_argument(
        "-g", "--local-follower-threshold",
        dest="local_follower_threshold", type=int, default=5,
        help="only show accounts in the relative ranking that are followed by at least this many accounts that you follow")
    return parser.parse_args()

def get_follows(actor, limit=100):
    url = "https://public.api.bsky.app/xrpc/app.bsky.graph.getFollows"
    params = {"actor": actor, "limit": limit}

    results = []

    response = requests.get(url, params=params)
    response.raise_for_status()
    response_data = response.json()
    results.extend(response_data["follows"])

    while "cursor" in response_data:
        params["cursor"] = response_data["cursor"]
        response = requests.get(url, params=params)
        response.raise_for_status()
        response_data = response.json()
        results.extend(response_data["follows"])

    return results

def get_profile(actor):
    url = "https://public.api.bsky.app/xrpc/app.bsky.actor.getProfile"
    params = {"actor": actor}
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()

def get_profiles(actors):
    url = "https://public.api.bsky.app/xrpc/app.bsky.actor.getProfiles"
    params = {"actors": actors}
    response = requests.get(url, params=params)
    response.raise_for_status()
    response_data = response.json()
    return response_data["profiles"]

args = parse_arguments()

profile = get_profile(args.actor)

follows = get_follows(args.actor)

print(f"Loading accounts followed by the {len(follows)} accounts you follow:", file=sys.stderr)
stats_by_did = {}
for i, follow in enumerate(follows, start=1):
    sub_follows = get_follows(follow["did"])
    if not i % 10:
        print(f"...completed loading follows for {i} accounts", file=sys.stderr)
    for sub_follow in sub_follows:
        if sub_follow["did"] in stats_by_did:
            stats_by_did[sub_follow["did"]]["count"] += 1
        else:
            stats_by_did[sub_follow["did"]] = {
                "did": sub_follow["did"],
                "handle": sub_follow["handle"],
                "displayName": sub_follow["displayName"].strip() if "displayName" in sub_follow else None,
                "count": 1 }
print(file=sys.stderr)

follows_did_only = [f["did"] for f in follows]
stats_as_list = [v for v in stats_by_did.values()
                 if v["did"] != profile["did"] and v["did"] not in follows_did_only]

stats_as_list.sort(key=lambda x: x["count"], reverse=True)

for stats in stats_as_list[:args.number_to_show]:
    print(f"{stats['count']}: {stats['handle']} ({stats.get('displayName')})")

print()

stats_as_list = [stats for stats in stats_as_list if stats["count"] >= args.local_follower_threshold]
print(f"Loading {len(stats_as_list)} account profiles:", file=sys.stderr)
for i, chunk in enumerate(chunked(stats_as_list, 25), start = 1):
    if not i % 4:
        print(f"...completed loading {i * 25} account profiles", file=sys.stderr)
    for profile in get_profiles([elem["did"] for elem in chunk]):
        stats = stats_by_did[profile["did"]]
        stats["followersCount"] = profile["followersCount"]
        stats["share"] = stats["count"] / profile["followersCount"]
print(file=sys.stderr)

stats_as_list = [stats for stats in stats_as_list if stats['followersCount'] >= args.global_follower_threshold]
stats_as_list.sort(key=lambda x: x["share"], reverse=True)

for stats in stats_as_list[:args.number_to_show]:
    print(f"{stats['share']:.4f}: {stats['handle']} ({stats.get('displayName')})")
