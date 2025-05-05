# hltv-api
An unofficial python flask api for popular CS2 website hltv.org.

# Installation
**Prerequisites:** Python 3.x (check with `python --version` or `python3 --version`)

```bash
git clone https://github.com/M3MONs/hltv-api.git
cd hltv-api
pip install -r requirements.txt
python app.py
```

# Examples

## Top teams (ranking)
```http
GET /api/v1/teams/rankings
```
Returns the HLTV or VALVE team ranking.
![ranking](https://github.com/user-attachments/assets/829c924d-7730-468b-be57-75586fb242b2)


## Team Search
```http
GET /api/v1/teams/search/<name>
```
Searches for a team by name.

## Team Profile
```http
GET /api/v1/teams/<id>/<team_name>
```
Returns the team profile.

## Team matches
```http
GET /api/v1/teams/<id>/matches
GET /api/v1/teams/<id>/matches/<offset>
```
Returns a list of team matches (optionally with an offset).

## Results
```http
GET /api/v1/results/
GET /api/v1/results/<offset>
```
Returns the results of HLTV matches.
![results](https://github.com/user-attachments/assets/020eb6fb-8c11-409d-a2d6-5685d5a44385)


## Featured Results
```http
GET /api/v1/results/featured
```
Returns featured results.
![results_featured](https://github.com/user-attachments/assets/cc3b7740-6045-4401-83c7-515043b2b794)


## Upcoming matches
```http
GET /api/v1/matches/upcoming
```
Returns upcoming matches.

## Match details
```http
GET /api/v1/matches/<id>/<match_name>
```
Returns details of the selected match.

## Player Search
```http
GET /api/v1/players/search/<name>
```
Searches for a player by name.

## Player Profile
```http
GET /api/v1/players/<id>/<player_name>
```
Returns the player profile.
