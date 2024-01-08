# NFL Daily Fantasy Sports Lineup Creator
### Video Demo: https://youtu.be/NwyFMzN7VB4
A website that allows users to select a lineup for daily fantasy sports, while seeing advanced player stats and lineup characteristics. These lineups are added to a database that can be viewed and exported to a .csv file.
## Build Page
#### Summary
This page allows the user to select players to a lineup on the left part of the page from an internal csv database, which is viualised On the right side of the page using the Datatables CSS package.

#### Lineup section
This section has an empty template of the acceptable lineup structure for daily fantasy sports, with the correct number of the required positions. When the user clicks on each position within the lineup, it becomes highlighted and begins listening for the user to select a player from the Datatable. It filters the Datatable to only show players that are available for selection for this position, and removes any currently selected players from the Datatable to prevent duplicate selections. Once a player is selected, the name and relevant data is visualised in the player box.

To help with the user experience, each player that is selected has a colour code for its Position column and its Game Info column, making it clear when you have multiple players from the same game and what position each player is at a glance.

There are also some data fields at the bottom of the lineup, showing advanced lineup characteristics that are updated as players are selected. One of these, the total salary box, must be smaller than 50,000 for it to be a valid lineup. To help visualise this for the user, the box is highlighted green when it is below 50,000 and highlighted red when it goes above it.

There is an add lineup button beneath the lineup section, which adds the lineup to a SQL database, so long as it is valid. If it is invalid, the user is shown a html page with an error message describing why the lineup was invalid.

#### Datatable section

The right side of the page visualised the csv database using the Databales CSS add-in.

This add-in was selected as it provides a user-friendly table of the dataset, allowing for scrolling and has a built-in search bar.

The default number of items has been increased to show 100 items on the initial viewing of the page, to help the user experience.

As players are selected and the total salary increases, the available players are highlighted in red text if selecting them would cause the lineup to exceed the salary limit.

## Lineups Page

This page visualises the lineup database that is updated with each lineup that the user creates. It shows two tables, one with the names of the players and one with the ID's of the players. The ID's of the players is what is needed to upload the lineups to daily fantasy websites.

There are some interactive buttons on this page:

- *Reset*: This resets the lineups database, removing all previously created lineups.
- *Remove*: This button is next to each lineup and can be used to remove the lineups one at a time. this removes lineups from both tables and updates automatically.
- *Export to CSV*: This allows the user to export the ID's table to a .csv file that can be uploaded straight to daily fantasy sports websites.

On the right side of the page, there is a table showing the percentage ownership of each player. this updates automatically and shows the total percentage of lineups that each player appears in. this helps the user see their exposure to each player.

## Database and backend

The backend of this website is hosted in python using Flask. The database is built using SQLite3, and contains two tables: one is the table of names in the lineups, and one is the table of ID's.