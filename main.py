# By Andreas <git@fsck.rip>

import csv
import win32net
import win32netcon
import argparse


def main(args):
    with open("./userpass.csv") as csvfile:
        userpassreader = csv.DictReader(csvfile, delimiter=",")
        count = 0

        group = None
        if args.mode == "domain":
            group = args.group

        if args.mode == "domain" and args.group is None:
            raise Exception("You must provide a group name with domain mode (e.g. group-14.lab.tu)")

        for row in userpassreader:
            try:
                # Delete the user first (if they exist) and create again.
                # Makes my life easier :)
                win32net.NetUserDel(group, row["username"])
            except win32net.error:
                pass

            try:
                win32net.NetUserAdd(
                    group,
                    1,
                    dict(
                        name=row["username"],
                        password=row["password"],
                        priv=win32netcon.USER_PRIV_USER,
                        flags=win32netcon.UF_SCRIPT,
                        comment="added from script",
                    ),
                )

                print(
                    f"Created user {row["username"]}, with password {row["password"]} to {args.mode} users"
                )
                count += 1
            except win32net.error as e:
                print(e)

        print(f"Added a total of {count} users")


if __name__ == "__main__":
    parser: argparse.ArgumentParser = argparse.ArgumentParser()
    parser.add_argument("mode", type=str, default="local", choices=["local", "domain"])
    parser.add_argument("--group", type=str)
    main(parser.parse_args())
