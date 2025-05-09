# fizanto


## 1. The folder docker_images contain code that will run inside a docker container.

   There are 3 files :-

   1. initial_image :- Hits the email endpoint, replies to the email, saves all the attachments to a folder, generates and runs pandas analysis cod to do a initial data anlysis of the csv file in the email attachment and loads the result in knowledge base, summarizes the markdown files and loads the knowledge base. This image should run once when a new email arrives.

   2. analysis_image :- Takes input a prompt, generates and runs pandas analysis code based on the prompt given and csv metadata stored in the folder by the first image and returns the output directly. This runs everytime when knowledge agent doesn't find answer in knowledge base and the asked question is related to data analysis.

   3. visualization_image :- Takes input a prompt, generates and runs matplotlib visualization code based on the prompt given and csv metadata stored in the folder by the first image and returns the filepath of the plot where it is stored. This runs everytime when knowledge agent is asked to generate a plot.


To create docker image for these files, run :-

 1. docker build -t initial-kb-load .

 2. docker build -t analysis-service .

 3. docker build -t vis-service .


Modify the dockerfile everytime accordingly.



Use the following to run the docker images :-

 1. docker run --rm \
  --add-host=host.docker.internal:host-gateway \
  -v /home/pranjal/Downloads/fizanto/attachments:/app/attachments \
  -v /home/pranjal/Downloads/fizanto/.env:/app/.env \
  -v /home/pranjal/Downloads/fizanto/tmp:/app/tmp \
  initial-kb-load


  For email server running locally. Remove   "--add-host=host.docker.internal:host-gateway \" when using fly's hosted email server



  2. docker run --rm \
  -v /home/pranjal/Downloads/fizanto/attachments:/app/attachments \
  -v /home/pranjal/Downloads/fizanto/.env:/app/.env \
  -e ANALYSIS_PROMPT="What is the average annual income?" \
  analysis-service


  3. docker run --rm \
  -v /home/pranjal/Downloads/fizanto/attachments:/app/attachments \
  -v /home/pranjal/Downloads/fizanto/.env:/app/.env \
  -v /home/pranjal/Downloads/fizanto/output:/app/output \
  -e VISUALIZATION_PROMPT="Create a bar plot of grade column." \
  vis-service



## The Email folder contains api process-email used by the initial_image. Its deployed version is here :- 

  https://github.com/pranzalkhadka/Email_Automation


## The memoyy folder uses sqlite to store session summary. For agents to remember the past conversations.

## The Teams-app folder contains code for teams integration and appManifest for uploading custom app in teams


## The to_send_in_email folder contains files to attach when sending email to Sarah Wilson

## The check_db.py file is used to check whats stored in knowledge base.

## The file agno_supervisor is the agno app integrated with docker image and knowledge base.

## mrm_report folder contains code for mrm pdf generation and uses a completely diffrent agno app. This folder is completely independent to the rest of the files.

