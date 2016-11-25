import sys
import requests
import json
from datetime import datetime

# This file will get the commit history for all repos for a user.
GitUsers =["dakota002","squeeeeeeeee","nasa"]

def UpdateJson(GitUserList):
    # get the date for when the program runs
    now = datetime.now()
    todayDate = str(now.year)+str(now.month)+str(now.day)+str(now.hour)+str(now.minute)

    for user in GitUserList:

        shouldGetForUser = str(raw_input("Get data for "+user+"? "))
        if shouldGetForUser.lower() in ["y","yes","yeah","yup"]:
            # Get the names of the repos for a given github user, in this case, me :)
            repoRequest = requests.get("https://api.github.com/users/"+user+"/repos")
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
                    shouldGetRepo = str(raw_input("Get data for "+name+"?"))
                    if shouldGetRepo in ["y","yes","yeah","yup"]:
                        print("Getting info from repo: "+name)
                        r = requests.get("https://api.github.com/repos/"+user+"/"+str(name))
                        if r.status_code == 200:
                            repo = json.loads(r.content)
                            c = requests.get("https://api.github.com/repos/"+user+"/"+name+"/commits")
                            if c.status_code == 200:
                                commits = json.loads(c.content)
                                repoInfo[name] = {
                                    "languages":json.loads(requests.get(repo["languages_url"]).content),
                                    }
                                repoInfo[name]["commits"]=[]
                                for commit in commits:
                                    getCommitStats = json.loads(requests.get("https://api.github.com/repos/"+user+"/"+name+"/commits/"+commit['sha']).content)
                                    commitStats = getCommitStats["stats"]
                                    repoInfo[name]["commits"].append({"sha":commit['sha'],"stats":commitStats})
                                with open("gitData_"+user+".json","r+") as file1:
                                    file1.write(json.dumps(repoInfo, indent=4, separators=(',',':')))
                            else:
                                print("Error trying to get commits, returned error code: " +str(c.status_code))
                        else:
                            print("Error trying to get repo, {0}, returned error code: {1}".format(name,r.status_code))
                    else:
                        print("Skipping "+name)
            elif repoRequest.status_code == 403:
                print(json.loads(repoRequest.content))
        else:
            print("Skipping "+user)


if __name__ == "main":
    UpdateJson(GitUsers)
