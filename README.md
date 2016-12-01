# Tournament DB

## Overview
This project implements a Postgresql database and Python module for managing a [Swiss-system tournament](https://en.wikipedia.org/wiki/Swiss-system_tournament).

## Installation

This repository contains a Vagrant VM, which should be downloaded and instantiated; as such, it is necessasry to install [Vagrant](http://vagrantup.com/) and [VirtualBox](https://www.virtualbox.org/).

Once these tools are installed, and the repository is cloned, the following instructions can be used to run the project.

## Usage

### Run the VM

1. `$ cd /path/to/tournament-db/vagrant`
2. `$ vagrant up`
3. `$ vagrant ssh`

You should be presented with the prompt for the virtual machine, and you will be able to create a `tournament` database via `psql`.

### Create a Database

1. `vagrant@vagrant-ubuntu-trusty-32:~$ psql`
2. `vagrant=> CREATE DATABASE tournament;`
3. `vagrant=> \c tournament`
3. `vagrant=> \i /vagrant/tournament/tournament.sql`

This command will create two tables and five views.

### Run the Test Cases

Lastly, quit `psql` and check that the database is functioning correctly by running the associated test cases:

1. `vagrant=> \q`
2. `vagrant@vagrant-ubuntu-trusty-32:~$ python /vagrant/tournament/tournament_tests.py`

All ten cases should pass.