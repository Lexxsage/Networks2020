in terminal do
sudo iptables -F
sudo iptables -A INPUT -i eth0 -p tcp --dport 22 -j ACCEPT
sudo iptables -A INPUT -i eth0 -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
sudo iptables -A INPUT -i eth0 -j DROP

when try to

ssh -L 8070:www.google.com:22 <hostname>
ssh -L 8080:ccfit.nsu.ru:22 <hostname>
ssh -L 8090:localhost:22 <hostname>

w - look your pts/number
to kill:
pkill -9 -t pts/number
