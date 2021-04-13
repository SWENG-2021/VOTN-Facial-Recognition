# VOTN-Facial-Recognition
The SWENG-2021 Project, Group 37: [Conor](https://github.com/conorlolynch), [Holly](https://github.com/hollymcevoy), [Barry](https://github.com/barryos112), [Michal](https://github.com/swiercm), [David](https://github.com/david-olowookere), [Pavel](https://github.com/cppavel). 

A facial recognition app integrated into frame.io workflow.

## Overview

An Ubuntu server, which is running on AWS (in our use-case) and receives webhooks from frame.io, when new videos are uploaded. It downloads the new videos, runs recognition on them and sends the results of the recognition back to frame.io (video description). 

## Prerequisites
`opencv-python`\
`datetime`

## How to use
To detect faces in a still image:\
py recognition.py image.png i

To detect faces in a video (mp4 or avi):\
py recognition.py video.mp4 v 

