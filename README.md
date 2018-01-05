# ThrowingSchedule

Reads a throwing schedule csv file and sends a daily notification describing the throwing plan. The program is called every day at 10am through an Amazon Web Services EC2 instance.

## Pushbullet

This program uses the Pushbullet API. Pushbullet is a mobile app and browser extension used to send link or messages between devices. Explore Pushbullet [here](https://www.pushbullet.com/).

## How to use

To add a user to the system, add their name, Pushbullet API token, and info parameter (0 - no info, 1 - only throwing info, 2 - full info) to the [PushConfig](PushConfig.csv) file. The Pushbullet API token can be created by going to the "Access Tokens" section in your Pushbullet [settings page](https://www.pushbullet.com/#settings). Next, add your schedule csv to the [Schedules](Schedules/) wtih the name "(Name) - Throwing Schdule.csv", and your work is done. 
