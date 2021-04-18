## Getting Started Guide

## Prerequisites

You should have an Ubuntu Linux server, to which you have access either directly or through ssh client. Our suggestion is using AWS, as this was initially specified by our client and the whole system was tested on such infrastructure. If you are not using AWS, the guide will still be very useful to you, though some parts of it will be not applicable. 

We suggest using a free-tier AWS EC2 instance for testing, you easily create such instance in 3-4 minutes, after you registered on AWS. Make sure to choose options which are eligible for tier, otherwise you will have to pay for the resources you use. There is a lot of guides on how to create an EC2 instance on AWS, if you have trouble you can have a look at this one, for example, [Amazon EC2 Basics & Instances Tutorial](https://www.youtube.com/watch?v=iHX-jtKIVNA). 

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

## Step 2, setting up frame.io

## Step 3, product installation

## Step 4, setting up SSL

## Step 5, testing
  

## References

1. [Deploying python flask to AWS and installing SSL](https://medium.com/@samuel.ngigi/deploying-python-flask-to-aws-and-installing-ssl-1216b41f8511), a lot of information was copied from there, but we laid it out a bit differently to make it more applicable for our situation.

