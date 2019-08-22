# NFLTop100-API
Django REST API for the top 100 NFL players of the year

Admin: [https://nfltop100.herokuapp.com/admin](https://nfltop100.herokuapp.com/admin)  
Root: [https://nfltop100.herokuapp.com/api/top100](https://nfltop100.herokuapp.com/api/top100)

- Note: Only admin users have access to full CRUD functionalities  
- Note: All ids are integers > 0  

## Endpoints:
Example: [https://nfltop100.herokuapp.com/api/top100/players/?team=1&position=5](https://nfltop100.herokuapp.com/api/top100/players/?team=1&position=5)

Endpoint to view teams: */teams* - [https://nfltop100.herokuapp.com/api/top100/teams](https://nfltop100.herokuapp.com/api/top100/teams)  
Endpoint to view specific team: */teams/{team_id}*  
Endpoint to filter teams that have players in the top 100: */teams/?assigned_only=1*  

Endpoint to view positions: */positions* - [https://nfltop100.herokuapp.com/api/top100/positions](https://nfltop100.herokuapp.com/api/top100/positions)  
Endpoint to view specific position: */positions/{position_id}*  
Endpoint to filter positions that have players in the top 100: */positions/?assigned_only=1*  

Endpoint to view players: */players* - [https://nfltop100.herokuapp.com/api/top100/players](https://nfltop100.herokuapp.com/api/top100/players)  
Endpoint to view specific player: */players/{player_id}*  
Endpoint to filter players playing for a specific team: */players/?team={team_id}*  
Endpoint to filter players playing a specific position: */players/?position={position_id}*  
Endpoint to filter players playing at specific teams and specific positions: */players/?team={team\_id}&position={position_id}*