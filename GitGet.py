import sys
import requests
import json
from datetime import datetime

# This file will get the commit history for all repos for a user.
# The fucking request limit is killing me
# GitUsers =["dakota002","squeeeeeeeee"]

# get the date for when the program runs
now = datetime.now()
todayDate = str(now.year)+str(now.month)+str(now.day)+str(now.hour)+str(now.minute)


# Get the names of the repos for a given github user, in this case, me :)
repoRequest = requests.get("https://api.github.com/users/dakota002/repos")
print("Status of request: " + str(repoRequest.status_code))


# If we get a good response, we continue on!!
if repoRequest.status_code == 200:


    # Load the response content into a json object
    userReposContent = json.loads(repoRequest.content)


    # Get pull out the names of each repo
    names = []
    for i in range(len(userReposContent)):
        names.append(userReposContent[i]["name"].encode())


    # Now we will build the repo info into the repoInfo object
    repoInfo = {}
    for name in names:
        print("Getting info from repo: "+name)
        r = requests.get("https://api.github.com/repos/dakota002/"+str(name))
        if r.status_code == 200:
            repo = json.loads(r.content)
            c = requests.get("https://api.github.com/repos/dakota002/"+name+"/commits")
            if c.status_code == 200:
                commits = json.loads(c.content)
                repoInfo[name] = {
                    "languages":json.loads(requests.get(repo["languages_url"]).content),
                    }
                repoInfo[name]["commits"]=[]
                for commit in commits:
                    getCommitStats = json.loads(requests.get("https://api.github.com/repos/dakota002/"+name+"/commits/"+commit['sha']).content)
                    commitStats = getCommitStats["stats"]
                    repoInfo[name]["commits"].append({"sha":commit['sha'],"stats":commitStats})
                with open(todayDate+"gitData.json","w+") as file1:
                    file1.write(json.dumps(repoInfo, indent=4, separators=(',',':')))
            else:
                print("Error trying to get commits, returned error code: " +c.status_code)
        else:
            print("Error trying to get repo, {0}, returned error code: {1}".format(name,r.status_code))
elif repoRequest.status_code == 403:
    print(json.loads(repoRequest.content))
