## Getting Started Guide

Step by step guide to make sure you can use our system on your server.

## Prerequisites

You should have an Ubuntu Linux server, to which you have access either directly or through ssh client. Our suggestion is using AWS, as this was initially specified by our client and the whole system was tested on such infrastructure. If you are not using AWS, the guide will still be very useful to you, though some parts of it will be not applicable. 

We suggest using a free-tier AWS EC2 instance for testing, you can easily create such instance in 3-4 minutes, after you registered on AWS. Make sure to choose options which are eligible for tier, otherwise you will have to pay for the resources you use. There is a lot of guides on how to create an EC2 instance on AWS, if you have trouble you can have a look at this one, for example, [Amazon EC2 Basics & Instances Tutorial](https://www.youtube.com/watch?v=iHX-jtKIVNA). 

Please specify the security group as follows: 

![1_WJRhXaUU0DjvlCwQXUj6AA](https://user-images.githubusercontent.com/24837651/115159314-77286880-a08a-11eb-87dc-cc4003b19b50.png)

To connect to your instance, you can use standard terminal in Linux or Putty on Windows, you will have to convert your pem key into a ppk so as to use Putty. This can be done with PuttyGen. Here is a [Putty tutorial](https://www.siteground.com/tutorials/ssh/putty/)


NB: If you are using a low-perfomance machine or a free-tier machine, we suggest you allocate a swap file. Here is a guide on how to do that [Swap file guide](https://linuxize.com/post/create-a-linux-swap-file/). We suggest you allocate 4GiB, if you are using a machine with 1GiB of RAM (free-tier). 

## Step 1, obtaining a free domain and setting up DNS

1. Go to [freenom.com](https://www.freenom.com/ru/index.html?lang=ru) and register for an account.
2. Go to Services -> Register a new domain.
3. Enter the desired domain name and check it’s availability.
4. Continue with the checkout process and you should be on the same step as the screenshot below.

![1_mk-DtmeOOwzDZRx7JU0bYg](https://user-images.githubusercontent.com/24837651/115148719-c786d280-a058-11eb-914b-4fa3c3ce3274.png)

5. Skip the DNS for now (We will configure it later once we have the Nameservers of our EC2 instance) and under the Period column, select an option for how long would you use the domain. (Maximum of 1 Year to avail it for free)

6. Allocate a new Elastic IP address for your EC2 instance (Elastic IP product). In "Actions", choose "associate address" and associate the address you just allocated with the EC2 instance you created. 

7. Create a new public hosted zone (Amazon Route 53 product) with the domain you got from freenom. Once public hosted zone is created, you’ll be presented with 2 default record sets for your domain. In here, take note all of the 4 Nameservers (Type NS). 

8. Create another record sets for your domain, one with www name and one without it. All pointing to your Elastic IP you set to your EC2 instance. See screenshot below.

![1_9q-ERGrntV1aF10mU71qsg](https://user-images.githubusercontent.com/24837651/115149012-f6ea0f00-a059-11eb-89ba-150fac00e561.png)

9. Once you’ve have setup the 2 additional record sets, the last step is to just point your domain to use the Nameservers provided by Route53 service.

10. Finally, login to your Freenom account go to Services->My Domains. From here, choose the domain and click on Manage Domain. Then go to, Management Tools, then Nameservers. From here, select custom nameservers and just enter all the 4 nameservers and hit on the save button. Just give it a couple of minutes and you would now be able to access your app in your EC2 instance with the domain you choose.

## Step 2, product installation

NB: For this step you will need to have git installed, on AWS machines and other cloud services it is usually available out of the box, here is a guide on [how to install git on linux](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git). 

1. Run this command in the folder where you would like your files to be located:

`git clone https://github.com/SWENG-2021/VOTN-Facial-Recognition`

Alternatively, you could clone the repo to your local machine and use FTP, like filezilla, but this is out of scope of this guide. 

2. Go into the folder VOTN-Facial-Recognition and run the following command:

`sudo sh install.sh`

This should install the required libraries and other software. 

3. Configure nginx server: 

First run: 

`sudo rm /etc/nginx/sites-enabled/default` 

`sudo rm /etc/nginx/sites-available/default`

This will remove the default configuration. 

Now run: 

`sudo touch /etc/nginx/sites-available/yourdomain.com`

`sudo chown -R $USER:$USER /etc/nginx/sites-available/yourdomain.com`

This creates a new configuration file and changes its owner. 

Open the file you just created in nano or any other editor you like and paste this in:

`server {`

`listen 80;`

`server_name www.yourdomain.com yourdomain.com;`

`location / {`

`proxy_pass http://127.0.0.1:8000/;`

`}`

`}`

This is the server configuration (nginx proxy). 

Run:

`sudo ln -f -s /etc/nginx/sites-available/yourdomain.com /etc/nginx/sites-enabled/yourdomain.com`

`sudo service nginx restart`

## Step 3, setting up frame.io

1. Go to [frame.io developer website](https://developer.frame.io/) and log in

2. Click on "Developer tools" and choose "tokens". Here you will need to create a token for your account. Name it as you like and click "select all scopes", then click "submit". Important: copy the token after it was created and store it in secure place. If somebody gets your token, they will be able to do anything they like with your account, like deleting videos. 

3. Click on "Developer tools" and choose "webhooks". Click on "create webhook". Name it as you wish. For the url please specify: https://www.yourdomain.com/webhook. Select any team for which you would like the webhook to operate. If you want multiple teams, you will have to create multiple webhooks. Check only asset.ready. Click on "submit". When the webhook is created, copy its secret to a secure location. You will have access to the secret in the future in case you lose so do not worry. 

4. Click on "Developer tools" and choose "custom actions". Click on "create a custom action". Name it as you wish and describe it as you like. For the url please specify: https://www.yourdomain.com/addpicture. Select any team for which you would like the custom action to operate. If you want multiple teams, you will have to create multiple custom actions. For event specify "picture.added". Allow collaborators to have access. Click on "submit". When the custom action is created, copy its secret to a secure location. You will have access to the secret in the future in case you lose so do not worry. 

5. SSH into your server or connect by any other means (see step 2). Now go to root directory and go into etc folder (cd /etc). In this folder run: 

  `sudo nano environment`
  
Now, make sure not to change any entry that is already in the file. You will have to add 3 environment variables, like that:

`FRAME_IO_TOKEN="token"`

`SECRET="secret"`

`CUSTOM_ACTIONS_SECRET="custom_actions_secret"`

Here the strings token, secret and custom_actions_secret come from steps 2-4. Make sure not to mix them up. 


## Step 4, setting up SSL

To set up ssl you will have to run the following commands:

`sudo apt-get install software-properties-common`

`sudo add-apt-repository ppa:certbot/certbot`

`sudo apt-get update`

`sudo apt-get install python-certbot-nginx`

`sudo certbot --nginx`

This sets up an SSL certificate for your server. You might need to wait for sometime before the changes take place. 

## Step 5, testing
  
To test the system go into the folder where server.py is located. You need to run the following command: 

`sudo gunicorn server:app`

If this succeeds you will not see any error messages, now the webhook listener is active. Go into your user frame.io account, try uploading some videos and adding new pictures into the database. Check out the logs to see if there are any erros. 

Here is a [User Guide](https://github.com/SWENG-2021/VOTN-Facial-Recognition/blob/main/UserGuide.md).

## References

1. [Deploying python flask to AWS and installing SSL](https://medium.com/@samuel.ngigi/deploying-python-flask-to-aws-and-installing-ssl-1216b41f8511), a lot of information was copied from there, but we laid it out a bit differently to make it more applicable for our situation.

