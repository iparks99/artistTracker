# artistTracker

This is my personal tool for notifying me whenever an artist releases new music.

## Installation

Download the source code for this repo.

## Usage

You must create a `spotify.config` and an `artists.json` file in the directory with your downloaded `main.py`.

Your `spotify.config` file will contain your client ID and client secret for use by Spotipy. You can obtain these by [registering your developer app](https://developer.spotify.com/documentation/general/guides/app-settings/#register-your-app). The config should be in JSON format and look like:
```json
{
  "SPOTIPY_CLIENT_ID": "YOUR ID",
  "SPOTIPY_CLIENT_SECRET": "YOUR SECRET"
}
```
This file is not necessary if these values are already set in your environment, but you will get a warning if this file cannot be found.

To set up your `artists.json`, find some artists' Spotify IDs using their [search tool](https://open.spotify.com/search). The artist's ID is in the page URL following the '/artist/'. Next, add an entry in this JSON file for each artist you want to follow. It should look like this:
```json
{
  "spotify:artist:ARTIST_ID": [],
  ...
}
```
an example being:
```json
{
  "spotify:artist:0YhUSm86okLWldQVwJkLlP": [],
  "spotify:artist:38SKxCyfrmNWqWunb9wGHP": []
}
```
This would follow [Bad Suns](https://open.spotify.com/artist/0YhUSm86okLWldQVwJkLlP) (first line) and [Good Kid](https://open.spotify.com/artist/38SKxCyfrmNWqWunb9wGHP) (second line).

The square brackets in each line will be updated with each of their albums as you run this script.

### Unix
On Unix systems you can [set a cron job](https://www.unixmen.com/add-cron-jobs-linux-unix/) to run `main.py` as frequently as you like.
### MacOS
MacOS can also use cron jobs, or you may use [launchd](https://developer.apple.com/library/archive/documentation/MacOSX/Conceptual/BPSystemStartup/Chapters/ScheduledJobs.html) to schedule jobs to run this Python script.
### Windows
On Windows you can use a [batch script](https://www.tutorialspoint.com/batch_script/index.htm) in the startup folder to run this Python script on [startup](https://www.computerhope.com/issues/ch000322.htm). Alternatively, you can set a job in the [task scheduler](https://www.windowscentral.com/how-create-automated-task-using-task-scheduler-windows-10).

## Contributing
Feel free to make pull requests or contact me to request features. I have some ideas for improvement so stay tuned.