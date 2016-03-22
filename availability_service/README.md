#MOP

1. Install node from nodejs.org
2. `npm install -g forever`
3. `sudo cp availabilityd /etc/init.d` 
4. `sudo chmod a+x /etc/init.d/availabilityd`
5. `sudo update-rc.d availabilityd defaults`
6. Start the service using `/etc/init.d/availabilityd start`
7. Service will be listening in the port 8816
