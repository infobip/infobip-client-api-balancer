# Infobip client API balancer

## Description

Infobip client API balancer balances your Infobip REST API calls. It gives your service security that it will be able to access Infobip REST API even if one Infobip's data center goes down or there is an ISP routes issue.

Infobip client API balancer balances API calls to multiple datacenters seamlesly and without any configuration needed.

* comes precofigured for your convenince
* works out of the box
* uses the best DC optionf for your cenvenience
* automatic retry on any error
* based on proven [HAProxy](https://www.haproxy.org/)

## Usage

### As sidecar

#### 1. Run infobip-client-api-balancer as docker container:

	docker run --name=infobip-client-api-balancer \
		-p 7070:7070 \
		-p 7443:7443 \
		-p 7182:7182 \
		-e "ENDPOINTS_AUTHORIZATION=App <API Key>" \
		-v /path/to/data/:/tmp/infobip-client-api-balancer/
		-d mstipanov/infobip-client-api-balancer:latest

#### 2. Point your app to the proxy:
	
Instead of pointing your app to https://api.infobip.com, point it to http://127.0.0.1:7070


## How To

### Obtain the API Key

	POST settings/1/accounts/_/api-keys HTTP/1.1
	Host: api.infobip.com
	Authorization: Basic <echo -n 'username:password' | base64>
	Content-Type: application/json
	Accept: application/json
	
	{
	    "name": "Client API balancer",
	    "permissions": [
	      "/client/v1/balancer"
	    ],
	    "validTo": "2100-01-01T00:00:00.000+0000"
	}	

**This API Key is restricted only to use with Client Balancer API and has low value as it cen't be used to consume other Infobip services!**

More instructions here: [Create and manage your API keys](https://dev.infobip.com/settings/create-and-manage-api-key)


### Use a custom https certificate
	
Create your own haproxy.pem and run the docker container like this:

	docker run --name=infobip-client-api-balancer \
		-p 7070:7070 \
		-p 7443:7443 \
		-p 7182:7182 \
		-e "ENDPOINTS_AUTHORIZATION=App <API Key>" \
		-v /path/to/data/:/tmp/infobip-client-api-balancer/
		-v /path/to/haproxy.pem:/usr/local/etc/haproxy/cert/haproxy.pem \
		-d mstipanov/infobip-client-api-balancer:latest
	

##Repositories

* [Github](https://github.com/infobip/infobip-client-api-balancer) 
* [Dockethub](https://hub.docker.com/r/mstipanov/infobip-client-api-balancer) 
