# VOTN-Facial-Recognition
The SWENG-2021 Project, Group 37: [Conor](https://github.com/conorlolynch), [Holly](https://github.com/hollymcevoy), [Barry](https://github.com/barryos112), [Michal](https://github.com/swiercm), [David](https://github.com/david-olowookere), [Pavel](https://github.com/cppavel). 

A facial recognition app integrated into frame.io workflow.

## Overview

An Ubuntu server, which is running on AWS (in our use-case) and receives webhooks from frame.io, when new videos are uploaded. It downloads the new videos, runs recognition on them and sends the results of the recognition back to frame.io (video description). It allows for new photos to be added in the recognition database via custom actions functionality. 

## How can I try it out?

Please view our [Getting Started Guide](https://github.com/SWENG-2021/VOTN-Facial-Recognition/blob/main/GettingStarted.md) and [User Guide](https://github.com/SWENG-2021/VOTN-Facial-Recognition/blob/main/UserGuide.md).

## How can I contribute to the project? 

The project was developed as part of the Software Engineering module, our team took in 3rd year (Conor, Michal) and in 2nd year (Barry, David, Holly, Pavel). Feel free to reach out to us if you have any ideas for further development. If this project was added as one of the choices for the next year Software Engineering module and you have happened to choose it, here is a list of improvements we were thinking of, but did not have enough time to deliver:

1. Create docs not only for AWS, but for other popular cloud platforms such as GCloud and Azure. Think about how this app could be changed to work with Google's App Engine infrastructure. 
2. Create a user interface to allow for better control over which pictures are added where. 
3. Allow users to set who they want to detect in particular videos to speed up recognition. For example, if we know that this footage cannot contain people from French rugby team, there is no need to search for them.
4. Automate the installation process further, see [Getting Started Guide](https://github.com/SWENG-2021/VOTN-Facial-Recognition/blob/main/GettingStarted.md) and think of ways you can make it easier for the user. 

## How to report a bug?

Feel free to open an issue.

