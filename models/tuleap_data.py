import requests
import json

url_base = "https://try.tuleap-enterprise.com/api/"
url_getproject_base = url_base + "projects?limit=10&query=%7B%22is_member_of%22%3A%20true%7D"
url_getuserstory_base = url_base + "trackers/userstories_id/artifacts"
url_getuserstories_base = url_base + "projects/project_id/trackers/"
url_gettask_base = url_base + "artifacts/userstory_id"
url_gettimetracking_base = url_base + "timetracking?query=%7B%20%22artifact_id%22%3A%20task_id%20%7D"
url_getuser_base =  url_base + "artifacts/task_id"

payload={}
headers = {
'X-Auth-AccessKey': 'tlp-k1-43.1917fa1769de7bc9fd8c8ae577508e3bc0ffdb38817639383d33fb40ae32e971'
}

def get_Data():

    data=[]

    projects_list = requests.request("GET", url_getproject_base, headers=headers, data=payload)
    projects_json=json.loads(projects_list.text)
    #for each project
    for project in projects_json :
        #project id
        project_id = str(project["additional_informations"]["agiledashboard"]["root_planning"]["milestone_tracker"]["project"]["id"])
        #print(project_id)
        #project name
        project_name =project["additional_informations"]["agiledashboard"]["root_planning"]["milestone_tracker"]["project"]["label"]
        #print (project_name)
        url_getuserstories_new=url_getuserstories_base.replace("project_id",project_id)
        userstory_id_list = requests.request("GET", url_getuserstories_new, headers=headers, data=payload)
        userstory_id_json=json.loads(userstory_id_list.text)
        #print (userstory_id_json)
        userstories_id= str (userstory_id_json[7]["id"])
        userstories_name= str (userstory_id_json[7]["label"])
        userstories_name2= str (userstory_id_json[8]["label"])
        #print(userstories_name2)
        #print (userstory_id_json[7]["label"])
        longeur=len(userstory_id_json)
        #print (longeur)
        for nb in range (longeur) :
            #print(userstory_id_json[nb])
        #    di=userstory_id_json[nb]
            if userstory_id_json[nb]["label"] == "User Stories":
                userstories_id= str (userstory_id_json[nb]["id"])
        #print (userstories_id)
        url_getuserstory_new=url_getuserstory_base.replace("userstories_id",userstories_id)
        userstories_list = requests.request("GET", url_getuserstory_new, headers=headers, data=payload)
        userstories_json = json.loads(userstories_list.text)
        #for each user story
        for userstory in userstories_json :
            #user story id
            userstory_id= str(userstory["id"])
            #user story name
            userstory_title = str(userstory["title"])
            url_gettask_new=url_gettask_base.replace("userstory_id",userstory_id)
            tasks_list = requests.request("GET", url_gettask_new, headers=headers, data=payload)
            tasks_json = json.loads(tasks_list.text)
            tasks =tasks_json["values"][3]["links"]
            #for each task
            for task in tasks :
                #time spent on the task
                task_time=0
                #task id
                task_id= str(task["id"])
                url_gettimetracking_new=url_gettimetracking_base.replace("task_id",task_id)
                timetracking_list = requests.request("GET", url_gettimetracking_new, headers=headers, data=payload)
                timetricking_json = json.loads(timetracking_list.text)
                for step in timetricking_json :
                    try :
                        task_time+=step["minutes"]
                    except IndexError:
                        task_time+=0
                url_getuser_new=url_getuser_base.replace("task_id",task_id)
                users_list = requests.request("GET", url_getuser_new, headers=headers, data=payload)
                users_json = json.loads(users_list.text)
                #id of the user who did the task
                user_id = users_json["values"][3]["values"][0]["id"]
                data.append({"userstory_id":userstory_id,"userstory_title":userstory_title, "project_id":project_id,"project_name":project_name,"user_id":user_id,"time_spent":task_time})
                data_json=json.dumps(data)
    return(data)

#programme principal
resultat=get_Data()
print (resultat)
