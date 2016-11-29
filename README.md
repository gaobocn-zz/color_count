# CS 5356 Final Project Count Color of a Image

**This README is copied from [Chris Wang](https://github.com/mw866/one-and-done/blob/master/README.md) (mw866@cornell.edu).**

Description: An API based on Flask, Gunicorn and NGINX

Usage: http://images.chriswang.tech/api/num_colors?src=<imageurl>

Example: http://images.chriswang.tech/api/num_colors?src=https://www.wikipedia.org/portal/wikipedia.org/assets/img/Wikipedia-logo-v2@2x.png

Remember to build the runtime cache: $siege -t1m --concurrent=20 -b -i --file=./output/chris/siege_urls.txt

Logs files:
* NGINX: tail -f /var/log/nginx/error.log

* Gunicorn: tail -f /var/log/gunicorn/error.log

## Architecture
* DNS: AWS Route 53

* Reverse Proxy & Load Balancer (x1 VM): NGINX

* Web Server (x3 VM): Gunicorn

* Web Framework: Flask

## Requirements
* https://docs.google.com/document/d/1oog1sbBdm-d6KSmLjhbHjAUD8XDtdojVWpyFNwk-Fj8/edit#heading=h.5ec0zrrtnk5v

## References

### ImageMagick

* ImageMagick with Python Example: https://github.com/jinpark/imageresizer

* ImageMagick Wand API Documentations: http://docs.wand-py.org/en/0.2.4/index.html

### Flask with Gunicorn
* Flask Applications with Gunicorn and Nginx on Ubuntu 16.04: https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-gunicorn-and-nginx-on-ubuntu-16-04

* Flask Logging: http://flask.pocoo.org/docs/0.11/errorhandling/

* Gunicorn config: http://docs.gunicorn.org/en/stable/settings.html#server-socket

 *Gunicorn accept Nginx forwarding: http://docs.gunicorn.org/en/stable/deploy.html

* UFW config: https://help.ubuntu.com/community/UFW

### NGINX

* NGINX Load Balancing config: https://www.nginx.com/resources/admin-guide/load-balancer/

### Vagrant
* Vagrant Network config:
https://www.safaribooksonline.com/library/view/vagrant-up-and/9781449336103/ch04.html
https://www.vagrantup.com/docs/virtualbox/networking.html

* VirtualBox Internal Network: https://www.virtualbox.org/manual/ch06.html#network_internal

### AWS  EC2

* Launch EC2 using AWSCLI: http://docs.aws.amazon.com/cli/latest/userguide/cli-ec2-launch.html

* AWSCLI Autocomplete: http://docs.aws.amazon.com/cli/latest/userguide/cli-command-completion.html

* AWS CLI Output Format: http://docs.aws.amazon.com/cli/latest/userguide/controlling-output.html

* EC2 Public IP Addressing: ttp://docs.aws.amazon.com/AWSEC2/latest/UserGuide/using-instance-addressing.html#differences

### AWS Route 53

* Routing Traffic to an Amazon EC2 Instance: http://docs.aws.amazon.com/Route53/latest/DeveloperGuide/routing-to-ec2-instance.html

## Troubleshooting

### Nginx

* Writing the NGINX Debugging Log to a File: https://www.nginx.com/resources/admin-guide/debug/#error_log_file

* Test new NGINX config: $sudo nginx -t && sudo service nginx restart

* See log in real time: $tail -f file-name.log

### Gunicorn

* ImportError: No module named wsgi: Run within /vagrant/

* Does not receive from NGINX: --bind 0.0.0.0:8000

## Troubleshooting Vagrant/Linux
* Network testing: Vagrant by default creates multiple interfaces, hence use ping -I <specific hostonly/private interface> to avoid confusion.

* Network interface config: /etc/network/interfaces

* .1 address cannot be used because of conflicts with host machine's vboxnet1 interface


### AWS
* "An error occurred (InvalidParameterValue) when calling the RunInstances operation: Address 192.168.0.2 is in subnet's reserved address range": The first four IP addresses and the last IP address in each subnet CIDR block are not available for you to use, and cannot be assigned to an instance: http://docs.aws.amazon.com/AmazonVPC/latest/UserGuide/VPC_Subnets.html

* No Public IP Address for SSH: Enable Auto-assign Public IP in VPC Console

* ConnectTimeout: HTTPSConnectionPool(host='s3.amazonaws.com', port=443): (a) Enable HTTP & HTTPS in Inbound ACL (b) Increase the timeout in requests.get (http://docs.python-requests.org/en/master/user/quickstart/#timeouts)

* Change Computer Name in Ubuntu: https://aws.amazon.com/premiumsupport/knowledge-center/linux-static-hostname/

## Performances
### Siege command used by Load Test script
$siege -t1m --concurrent=3 -b -i --file=./output/chris/siege_urls.txt --log=./output/chris/siege.log --user-agent=Magic Browser


### Parameters can be tuned
Gunicorn: --worker 3
Python Requests: requests.get(timeout = 0.01)

### Benchmark Results:

http://images-aws.afeld.me/api/num_colors?src=https://www.wikipedia.org/portal/wikipedia.org/assets/img/Wikipedia-logo-v2@2x.png
Transactions:		         353 hits
Availability:		      100.00 %
Elapsed time:		       59.94 secs
Data transferred:	        0.00 MB
Response time:		        0.51 secs
Transaction rate:	        5.89 trans/sec
Throughput:		        0.00 MB/sec
Concurrency:		        2.98
Successful transactions:         353
Failed transactions:	           0
Longest transaction:	        0.84
Shortest transaction:	        0.36


### Reference Results
 EC2 instance $siege --time 10s https://s3.amazonaws.com/startup-systems-final-images/6461517483.jpg
Transactions:		          82 hits
Availability:		      100.00 %
Elapsed time:		        9.32 secs
Data transferred:	        9.49 MB
Response time:		        0.91 secs
Transaction rate:	        8.80 trans/sec
Throughput:		        1.02 MB/sec
Concurrency:		        8.03
Successful transactions:          82
Failed transactions:	           0
Longest transaction:	        1.28
Shortest transaction:	        0.69
