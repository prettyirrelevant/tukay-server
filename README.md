# Tukay Server

This project was intended for the Chainlink Constellation Hackathon(yeah, I cannot complete it lol). More about the hackathon can be found [here](https://constellation-hackathon.devpost.com/).

It is an indexer built using Django Rest Framework. It moves from block to block listening for events emitted by certain contracts, parse the logs and stores them in a database which is then served to a client(React SPA) via RESTful API.

## Features
- [x] Index all events from the `Airdrop` contract
- [x] RESTFul endpoints to query all airdrops and claims.
- [ ] Index all events from the `Giveaway` contract.
- [ ] RESTFul endpoints to query all giveaways(regular, trivia, and activity)
- [ ] Index all events from the `Crowdfun` contract.
- [ ] RESTFul endpoints to query all crowdfunding activities.

## Status
Incomplete.

## Credits
Project name was inspired by a discussion or trend that happened on Twitter.