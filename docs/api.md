# API
After starting, a RESTful API is available on port 27467.
This can be used to update which TV shows you would like to keep track of,
and to list the episodes that have been downloaded.
This API requires Basic Auth, the username is "argosd" and you can
choose your own password in the settings file you'll create during installation.

This document describes the API endpoints and how you can interact with them.

## /shows
### GET
```json
[
  {
    "id": 1,
    "title": "Show title",
    "follow_from_season": 1,
    "follow_from_episode": 1,
    "minimum_quality": 720,
    "wait_minutes_for_better_quality": 1440
  },
  {...}
]
```
Calling this endpoint returns a list of shows that are being tracked.

### POST
Calling this endpoints add a new show to the list.
The following parameters are accepted:

Parameter | Description
--------- | -----------
**title** | The name of the show
**follow_from_season** | The season you want to start following this show from
**follow_from_episode** | The episode number you want to start following from  
**minimum_quality** | The minimum quality an episode of this show may be  
**wait_minutes_for_better_quality** | (optional) The maximum amount of minutes you want to wait for a better quality of an episode

Return code on success: HTTP 201 Created.

## /shows/[id]
### GET
```json
{
  "id": 1,
  "title": "Show title",
  "follow_from_season": 1,
  "follow_from_episode": 1,
  "minimum_quality": 720,
  "wait_minutes_for_better_quality": 1440
}
```
Returns the stored information about a specific show.

### DELETE
Deletes a specific show.  
Return code on success: HTTP 204 No Content.

### PUT
Updates a specific show. Accepts the same parameters as a POST to /shows.

## /episodes
### GET
```json
[
  {
    "id": 1,
    "show": 1,
    "link": "http://example.com/torrents/link.torrent",
    "season": 1,
    "episode": 1,
    "quality": 720,
    "is_downloaded": true,
    "created_at": 1473967268
  },
  {...}
]
```
Returns a list of all episodes that have been downloaded and added to a torrentclient.
